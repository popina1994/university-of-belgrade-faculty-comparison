from openpyxl.worksheet import worksheet

from data.tables.work_table.work import Work


class WorkWos(Work):
    COLUMN_IMPACT_FACTOR = "Impact factor 2017"
    COLUMN_IMPACT_FACTOR5 = "Impact factor 5 godina 2017"

    COLUMN_IDX_IMPACT_FACTOR = 7
    COLUMN_IDX_IMPACT_5FACTOR = 8

    def __init__(self, title: str, year: int, authors: str, doc_type: str, author: str = "", num_citations: int=0,
                 document_name: str="", impact_factor: str="", impact_factor5: str="",
                 department: str="", faculty: str=""):

        super().__init__(title, year, authors, doc_type, author, num_citations, document_name, department, faculty)
        self._impact_factor = impact_factor
        self._impact_factor5 = impact_factor5

    @property
    def impact_factor(self):
        return self._impact_factor

    @impact_factor.setter
    def impact_factor(self, value):
        self._impact_factor = value

    @property
    def impact_factor5(self):
        return self._impact_factor5

    @impact_factor5.setter
    def impact_factor5(self, value):
        self._impact_factor5 = value

    @staticmethod
    def write_headers_to_sheet(sheet: worksheet):
        Work.write_headers_to_sheet(sheet)
        sheet.cell(1, WorkWos.COLUMN_IDX_IMPACT_FACTOR).value = WorkWos.COLUMN_IMPACT_FACTOR
        sheet.cell(1, WorkWos.COLUMN_IDX_IMPACT_5FACTOR).value = WorkWos.COLUMN_IMPACT_FACTOR5

    def write_to_sheet(self, sheet: worksheet, row: int):
        super().write_to_sheet(sheet, row)
        sheet.cell(row, WorkWos.COLUMN_IDX_IMPACT_FACTOR).value = self.impact_factor
        sheet.cell(row, WorkWos.COLUMN_IDX_IMPACT_5FACTOR).value = self.impact_factor5

