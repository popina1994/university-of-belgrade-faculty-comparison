from openpyxl.worksheet import worksheet


class Work:
    def __init__(self, title: str, year: int, authors: str, doc_type: str, author: str = ""):
        self._author = author
        self._title = title
        self._year = year
        self._authors = authors
        self._doc_type = doc_type

    COLUMN_AUTHOR = "Glavni autor"
    COLUMN_TITLE = "Naslov"
    COLUMN_YEAR= "Godina"
    COLUMN_AUTHORS= "Autori"

    COLUMN_IDX_AUTHOR = 1
    COLUMN_IDX_TITLE = 2
    COLUMN_IDX_YEAR = 3
    COLUMN_IDX_AUTHORS = 4

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, value):
        self._authors = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def doc_type(self):
        return self._doc_type

    @doc_type.setter
    def doc_type(self, value):
        self._doc_type = value

    @staticmethod
    def write_headers_to_sheet(sheet: worksheet):
        sheet.cell(1, Work.COLUMN_IDX_AUTHOR).value = Work.COLUMN_AUTHOR
        sheet.cell(1, Work.COLUMN_IDX_TITLE).value = Work.COLUMN_TITLE
        sheet.cell(1, Work.COLUMN_IDX_YEAR).value = Work.COLUMN_YEAR
        sheet.cell(1, Work.COLUMN_IDX_AUTHORS).value = Work.COLUMN_AUTHORS

    def write_to_sheet(self, sheet: worksheet, row: int):
        sheet.cell(row, Work.COLUMN_IDX_AUTHOR).value = self.author
        sheet.cell(row, Work.COLUMN_IDX_TITLE).value = self.title
        sheet.cell(row, Work.COLUMN_IDX_YEAR).value = self.year
        sheet.cell(row, Work.COLUMN_IDX_AUTHORS).value = self.authors
