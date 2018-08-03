from openpyxl import Workbook
from data.work import Work
from utilities.global_setup import DATA_PATH
WORKS_WOS_FILE_NAME = DATA_PATH + r"\Work\works_wos.xlsx"
WORKS_SCOPUS_FILE_NAME = DATA_PATH + r"\Work\works_scopus.xlsx"
WORKS_SHEET_NAME = "Radovi"


class WorksWorkbook:
    def __init__(self, is_wos: bool):
        self.work_book_name = WORKS_WOS_FILE_NAME if is_wos else WORKS_SCOPUS_FILE_NAME
        self.work_book = Workbook()
        self.work_book.remove(self.work_book.active)
        self.sheet = self.work_book.create_sheet(WORKS_SHEET_NAME)
        Work.write_headers_to_sheet(self.sheet)
        self.row = 2

    def save_work(self, work: Work):
        work.write_to_sheet(self.sheet, self.row)
        self.row += 1

    def save(self):
        self.work_book.save(self.work_book_name)
