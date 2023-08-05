import pandas as pd
from datetime import datetime
import logging
import numpy as np

logger = logging.getLogger("pyC")

class ChangeLog:
    def __init__(
            self, source_file, clone_file, log_sheet_name="Change Logs", ignore_headers=[], ignore_sheets=[],
            case_sensitive_ignore=False
    ):
        """

        :param source_file: Path of excel file.
        :param clone_file: Path of clone version of source file.
        :param log_sheet_name: (optional) (default="Change Logs") Name of sheet containing change logs
        :param ignore_headers: (optional) list of headers to be ignored for change log
        :param ignore_sheets: (optional) list of sheet names to be ignored for change log
        :param case_sensitive_ignore: (default=False) If True, ignore sheets & headers list's data will be matched with same case.
        """
        self.source_file = source_file
        self.clone_file = clone_file
        self.log_sheet_name = log_sheet_name
        self.ignore_headers = ignore_headers
        self.ignore_sheets = ignore_sheets
        self.ignore_sheets.append(self.log_sheet_name)
        self.case_senstive_ignore = case_sensitive_ignore
        self.update_ignore_list()
        self.headers_column = {}

    def update_ignore_list(self):
        # Making data inside igonre lists in lower only if case_sensitive_ignore is false, so that it will be later
        # used at the time of comparision
        logger.debug("Updating ignore lists")
        if self.case_senstive_ignore:
            return None
        if self.ignore_headers:
            self.ignore_headers = [header.lower() for header in self.ignore_headers]
            logger.debug("Headers ignore list updated.")
        if self.ignore_sheets:
            self.ignore_sheets = [sheet.lower() for sheet in self.ignore_sheets]
            logger.debug("Sheets ignore list updated.")

    def xlsxChangeLog(self):
        """
        Method to trigger all functionalities including checking changes and updating clone file
        :return:
        """
        # Main method which will do all things including check and updating logs
        source = pd.ExcelFile(self.source_file)
        clone = pd.ExcelFile(self.clone_file)
        source_sheets = source.sheet_names
        clone_sheets = clone.sheet_names
        sheets = self.get_sheets(source_sheets, clone_sheets)
        logs = self.get_change_logs(source, clone, sheets)
        self.update_change_logs(logs, clone)
        self.update_clone_file(source, clone, source_sheets)

    def get_sheets(self, source_sheets, clone_sheets):
        # method is used to get sheets which are not inside ignore list, also deals with case_sensitive functionality
        sheets = []
        for sheet in source_sheets:  # looping through sheets in source file
            if sheet in clone_sheets:  # if sheet is not already present in clone file than change log is skipped
                if self.ignore_sheets:  # if ignore_sheets doesn't have any values than sheet name is directly added in list
                    if self.case_senstive_ignore:  # if the name is case_sensitive then check for exact value
                        if sheet not in self.ignore_sheets:
                            sheets.append(sheet)
                    elif sheet.lower() not in self.ignore_sheets:  # if checking is not case sensitive than checking value
                        sheets.append(sheet)                       # in lower as ignore list is also converted to lower
                else:
                    sheets.append(sheet)
        logger.debug("Sheets Gathered after filtering ignored sheets.")
        return sheets

    def get_str_sheet(self, excel, sheet):
        columns = excel.parse(sheet).columns
        converters = {column: str for column in columns}
        data = excel.parse(sheet, converters=converters)
        return data

    def get_change_logs(self, source, clone, sheets):
        # method returns a list of change log with all data in correct column position
        logs = []
        for sheet in sheets:
            source_sht = self.get_str_sheet(source, sheet)
            clone_sht = self.get_str_sheet(clone, sheet)
            headers, new_headers, removed_headers = self.get_headers(source_sht, clone_sht, sheet)
            for header in new_headers:
                # adding new headers in change log list with appropriate values
                logs.append([
                    datetime.now().strftime("%d-%m-%Y %H:%M"),
                    sheet,
                    header,
                    1,
                    "-",
                    "(new header)"
                ])
            for header in removed_headers:
                # adding removed headers in change log list with appropriate values
                logs.append([
                    datetime.now().strftime("%d-%m-%Y %H:%M"),
                    sheet,
                    header,
                    1,
                    "(removed header)",
                    "-"
                ])
            for header in source_sht.columns.values.tolist():
                if header not in headers or header in new_headers or header in removed_headers:
                    source_sht = source_sht.drop(header, 1)
            for header in clone_sht.columns.values.tolist():
                if header not in headers or header in new_headers or header in removed_headers:
                    clone_sht = clone_sht.drop(header, 1)
            logs += self.find_changes(source_sht, clone_sht, sheet)
        logger.debug("Change logs gathered")
        return logs

    def get_headers(self, source_sht, clone_sht, sheetname):
        # return a list of headers which are to be considered for change log, along with it return 2 others list with
        # new headers and removed headers so the change log contain directly entry of changes headers instead of whole
        # columns. Logic is same like get_sheets method
        source_headers = source_sht.columns.values.tolist()
        clone_headers = clone_sht.columns.values.tolist()
        self.headers_column[sheetname] = []
        headers = []
        temp_headers = []
        new_headers = []
        removed_headers = []
        for header in source_headers:
            if not header:
                continue
            if self.ignore_headers:
                if self.case_senstive_ignore:
                    if header not in self.ignore_headers:
                        temp_headers.append(header)
                    else:
                        self.headers_column[sheetname].append(header)
                elif header.lower() not in self.ignore_headers:
                    temp_headers.append(header)
                else:
                    self.headers_column[sheetname].append(header)
            else:
                temp_headers.append(header)

        for header in temp_headers:
            if header not in clone_headers:
                new_headers.append(header)
            if "usecount" in header.lower():
                self.headers_column[sheetname].append(header)
            elif "testresult" in header.lower():
                self.headers_column[sheetname].append(header)
            headers.append(header)

        for header in clone_headers:
            if not header:
                continue
            if self.ignore_headers:
                if self.case_senstive_ignore:
                    if header not in self.ignore_headers:
                        if header not in source_headers:
                            removed_headers.append(header)
                elif header.lower() not in self.ignore_headers:
                    if header not in source_headers:
                        removed_headers.append(header)
            else:
                if header not in source_headers:
                    removed_headers.append(header)
        if not self.headers_column[sheetname]:
            del self.headers_column[sheetname]
        logger.debug(f"Headers gathered after filtering ignored headers for sheet: {sheetname}")
        return headers, new_headers, removed_headers

    def find_changes(self, source_sht, clone_sht, sheetname):
        # finding changes for a column(header) from source to clone
        changes = []
        source_sht.fillna("", inplace=True)
        clone_sht.fillna("", inplace=True)
        if not source_sht.index.equals(clone_sht.index):
            merged_source = source_sht.merge(clone_sht, indicator=True, how='outer')
            source_changes = merged_source[merged_source['_merge'] != 'both']
            del source_changes["_merge"]
            clone_list = clone_sht.values.tolist()
            clone_index = clone_sht.index.values.tolist()
            data_dic = {}
            data_add = []
            data_remove = {}
            remove_keys = []

            for data, i in zip(source_changes.values.tolist(), source_changes.index.values.tolist()):
                if i < len(source_sht):
                    if i not in data_dic:
                        data_dic[i] = [data, ""]
                        data_add.append(i)
                else:
                    if data in clone_list:
                        index = clone_index[clone_list.index(data)]
                        if index in data_dic:
                            data_dic[index][1] = data
                        else:
                            data_dic[index] = ["", data]
                        data_remove[index] = index
                        remove_keys.append(index)

            for num in data_add:
                if not remove_keys:
                    break
                if num < data_remove[remove_keys[0]]:
                    for dt in remove_keys:
                        data_remove[dt] += 1
                while num > data_remove[remove_keys[0]]:
                    for dt in remove_keys:
                        data_remove[dt] -= 1
                    remove_keys.remove(remove_keys[0])
                    if not remove_keys:
                        break

            for ind in data_remove:
                if data_remove[ind] != ind:
                    if data_remove[ind] not in data_dic:
                        data_dic[data_remove[ind]] = data_dic[ind]
                    else:
                        data_dic[data_remove[ind]][1] = data_dic[ind][1]
                    del data_dic[ind]

            for data in data_dic:
                changes.append([
                    datetime.now().strftime("%d-%m-%Y %H:%M"),
                    sheetname,
                    "-",
                    data + 2,
                    data_dic[data][1],
                    data_dic[data][0]
                ])
        return changes

    def update_change_logs(self, logs, clone):
        # Updates Chane Log sheet in log file
        logger.debug("Updating change log sheet...")
        df_ = clone.parse(self.log_sheet_name)
        df = df_.append(pd.DataFrame(logs, columns=df_.columns))
        self.changeLogDf = df
        logger.debug("Change logs sheet updated")

    def update_clone_file(self, source, clone, source_sheets):
        df_dic = {}
        for sheet in source_sheets:
            df = self.get_str_sheet(source, sheet)
            if sheet in self.headers_column:
                clone_df = self.get_str_sheet(clone, sheet)
                if clone_df.index.equals(df.index):
                    df[self.headers_column[sheet]] = clone_df[self.headers_column[sheet]]
                    logger.debug(f"{str(self.headers_column[sheet])} headers of sheet {sheet} remained unchanged.")
                else:
                    logger.debug(f"{sheet} sheet of clone and source files has different indices. Thus ignored headers are updated from source")
            df_dic[sheet] = df
        df_dic[self.log_sheet_name] = self.changeLogDf
        with pd.ExcelWriter(self.clone_file) as writer:
            for sheetname in df_dic:
                df_dic[sheetname].to_excel(writer, sheetname, index=False)
            writer.save()

    @staticmethod
    def Insert_row_(row_number, df, row_value):
        df1 = df[0:row_number]
        df2 = df[row_number:]
        df1.loc[row_number] = row_value
        df_result = pd.concat([df1, df2])
        df_result.index = [*range(df_result.shape[0])]
        return df_result

