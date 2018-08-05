from enum import Enum, IntEnum

from openpyxl import Workbook
from data.tables.work_table.work import Work
from utilities.global_setup import DATA_PATH

WORKS_WOS_FILE_NAME = DATA_PATH + r"\Work\works_wos.xlsx"
WORKS_SCOPUS_FILE_NAME = DATA_PATH + r"\Work\works_scopus.xlsx"
WORKS_TEMP_FILE_NAME = DATA_PATH + r"\Work\works_temp.xlsx"

WORKS_FILE_NAME = [WORKS_WOS_FILE_NAME, WORKS_SCOPUS_FILE_NAME, WORKS_TEMP_FILE_NAME]
WORKS_TEMP_WORK_BOOK = WORKS_FILE_NAME.index(WORKS_TEMP_FILE_NAME)
WORKS_SHEET_NAME = "Radovi"


class WorkTypes(IntEnum):
    WOS = 0
    SCOPUS = 1
    TEMPORARY = 2


class WorksWorkbook:
    def __init__(self, work_book_type: WorkTypes):
        self.work_book_name = WORKS_FILE_NAME[work_book_type]
        self.work_book = Workbook()
        self.work_book.remove(self.work_book.active)
        self.sheet = self.work_book.create_sheet(WORKS_SHEET_NAME)
        self.row = 2

    def save_work(self, work: Work):
        work.write_to_sheet(self.sheet, self.row)
        if self.row == 2:
            work.write_headers_to_sheet(self.sheet)
        self.row += 1

    def save(self):
        self.work_book.save(self.work_book_name)
