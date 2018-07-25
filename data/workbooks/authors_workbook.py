from openpyxl import Workbook

AUTHORS_FILE_NAME = "authors.xlsx"


class AuthorsWorkbook:
    def __init__(self):
        self.work_book = Workbook()

    def save_authors(self, authors, faculty_name):
        work_sheet = self.work_book.create_sheet(faculty_name)
        work_sheet.title = faculty_name
        for row, author in enumerate(authors, start=1):
            work_sheet.cell(row, 1).value = author.first_name
            work_sheet.cell(row, 2).value = author.last_name
            work_sheet.cell(row, 3).value = author.department
            work_sheet.cell(row, 4).value = author.faculty

    def save(self):
        self.work_book.save(AUTHORS_FILE_NAME)
