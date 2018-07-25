from openpyxl import Workbook
from data.author import Author
AUTHORS_FILE_NAME = r"C:\Users\popina\Dropbox\Fakultet\Master Thesis\Data\People\authors.xlsx"


class AuthorsWorkbook:
    def __init__(self):
        self.work_book = Workbook()

    def save_authors(self, authors, faculty_name):
        work_sheet = self.work_book.create_sheet(faculty_name)
        work_sheet.title = faculty_name

        work_sheet.cell(1, 1).value = Author.COLUMN_FIRST_NAME
        work_sheet.cell(1, 2).value = Author.COLUMN_LAST_NAME
        work_sheet.cell(1, 3).value = Author.COLUMN_DEPARTMENT_NAME
        work_sheet.cell(1, 4).value = Author.COLUMN_FACULTY_NAME
        for row, author in enumerate(authors, start=2):
            work_sheet.cell(row, 1).value = author.first_name
            work_sheet.cell(row, 2).value = author.last_name
            work_sheet.cell(row, 3).value = author.department
            work_sheet.cell(row, 4).value = author.faculty

    def save(self):
        self.work_book.save(AUTHORS_FILE_NAME)
