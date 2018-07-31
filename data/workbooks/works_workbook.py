from openpyxl import Workbook
from data.work import Work
from utilities.global_setup import DATA_PATH
WORKS_WOS_FILE_NAME = DATA_PATH + r"\Work\works_wos.xlsx"
WORKS_WOS_SHEET_NAME = "Radovi"


class WorksWorkbook:
    def __init__(self):
        self.work_book = Workbook()
        self.work_book.remove(self.work_book.active)
        self.sheet = self.work_book.create_sheet(WORKS_WOS_SHEET_NAME)
        Work.write_headers_to_sheet(self.sheet)
        self.row = 2

    def save_work(self, work: Work):
        work.write_to_sheet(self.sheet, self.row)
        self.row += 1

    def save(self):
        self.work_book.save(WORKS_WOS_FILE_NAME)
