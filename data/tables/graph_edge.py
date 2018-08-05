from openpyxl.worksheet import worksheet


class GraphEdge:
    def __init__(self, author1: str, author2: str):
        self._author1 = author1
        self._author2 = author2

    @property
    def author1(self):
        return self._author1

    @author1.setter
    def author1(self, value):
        self._author1 = value

    @property
    def author2(self):
        return self._author2

    @author2.setter
    def author2(self, value):
        self._author2 = value

    COLUMN_IDX_AUTHOR1_NAME = 1
    COLUMN_IDX_AUTHOR2_NAME = 2
    COLUMN_AUTHOR1_NAME = "Source"
    COLUMN_AUTHOR2_NAME = "Target"

    @staticmethod
    def write_headers_to_sheet(sheet: worksheet):
        sheet.cell(1, GraphEdge.COLUMN_IDX_AUTHOR1_NAME).value = GraphEdge.COLUMN_AUTHOR1_NAME
        sheet.cell(1, GraphEdge.COLUMN_IDX_AUTHOR2_NAME).value = GraphEdge.COLUMN_AUTHOR2_NAME

    def write_to_sheet(self, sheet: worksheet, row: int):
        sheet.cell(row, GraphEdge.COLUMN_IDX_AUTHOR1_NAME).value = self.author1
        sheet.cell(row, GraphEdge.COLUMN_IDX_AUTHOR2_NAME).value = self.author2
