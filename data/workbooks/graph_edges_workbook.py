from openpyxl import Workbook
from data.author import Author
from data.graph_edge import GraphEdge
from utilities.global_setup import DATA_PATH
GRAPH_EDGES_FILE_NAME = DATA_PATH + r"\work\graph_edges.xlsx"
GRAPH_EDGES_SHEET = "Veze"


class GraphEdgesWorkbook:
    def __init__(self):
        self.work_book = Workbook()
        self.work_book.remove(self.work_book.active)
        self.sheet = self.work_book.create_sheet(GRAPH_EDGES_SHEET)
        GraphEdge.write_headers_to_sheet(self.sheet)
        self.row = 2

    def save_graph_edge(self, graph_edge: GraphEdge):
        graph_edge.write_to_sheet(self.sheet, self.row)
        self.row += 1

    def save(self):
        self.work_book.save(GRAPH_EDGES_FILE_NAME)
