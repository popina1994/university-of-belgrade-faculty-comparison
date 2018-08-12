from abc import ABC, abstractmethod

from data.tables.graph_edge import GraphEdge
from data.workbooks.authors_all_workbook import AuthorsAllWorkBook
from data.workbooks.graph_edges_workbook import GraphEdgesWorkbook
from data.workbooks.works_workbook import WorkTypes, WorksWorkbook


class CrawlerWorks(ABC):
    def __init__(self, work_book_type: WorkTypes):
        self.work_book_type = work_book_type
        self.list_authors = self.get_list_authors()
        list_name_authors = [author.id_name().lower() for author in self.list_authors]
        self.set_name_authors = set(list_name_authors)

    @abstractmethod
    def get_list_authors(self):
        pass

    def write_all_authors(self):
        work_book = AuthorsAllWorkBook(self.work_book_type)
        self.calculate_h_index()
        for author in self.list_authors:
            work_book.save_author(author)
        work_book.save()

    @abstractmethod
    def crawl_works(self, list_authors: list, work_book_type: WorkTypes):
        pass

    def crawl_work_all_authors(self):
        self.crawl_works(self.list_authors, self.work_book_type)

    def crawl_custom_authors(self, authors: list):
        self.crawl_works(authors, WorkTypes.TEMPORARY)

    def generate_graph_known_authors(self, work_book_type: WorkTypes, is_fraction: bool=False):
        work_book_works = WorksWorkbook(work_book_type, is_write=False)
        work_book_edges = GraphEdgesWorkbook(work_book_type, is_fraction)
        for row in work_book_works.load_sheet():
            author1 = row.author.lower()
            authors = row.authors.lower()
            authors_set = authors.split(",")
            for author2 in authors_set:
                if (author1 < author2) and (author2 in self.set_name_authors):
                    weight = 2 / (authors_set.__len__() * (authors_set.__len__() - 1)) if is_fraction else 1
                    edge = GraphEdge(author1, author2, weight)
                    work_book_edges.save_graph_edge(edge)
        work_book_edges.save()

    def load_citations(self):
        work_book_works = WorksWorkbook(self.work_book_type, is_write=False)
        authors_citations = {}
        dict_authors = {author.id_name(): author for author in self.list_authors}
        for idx, row in enumerate(work_book_works.load_sheet()):
            author = dict_authors[row.author]
            author_citations = authors_citations.get(author, [])
            num_citations = 0 if row.num_citations is None else int(row.num_citations)
            author_citations.append(num_citations)
            authors_citations[author] = author_citations
        return authors_citations

    def calculate_h_index(self):
        authors_citations = self.load_citations()
        author_h_index = {author: 0 for author in self.list_authors}
        for author in authors_citations.keys():
            author_citations = authors_citations[author]
            for h_index_cur in reversed(range(max(author_citations) + 1)):
                number_works = sum(num_citation >= h_index_cur for num_citation in author_citations)
                if number_works >= h_index_cur:
                    author_h_index[author] = h_index_cur
                    break
        for author in author_h_index.keys():
            author.h_index = author_h_index[author]

    def generate_graph_all_known_authors(self, is_fraction):
        self.generate_graph_known_authors(self.work_book_type, is_fraction)

    def generate_graph_known_authors_custom(self):
        self.generate_graph_known_authors(WorkTypes.TEMPORARY)




if __name__ == "__main__":
    pass
    #crawler = CrawlerLinksWos()
    #crawler.crawl_works()
    #crawler.generate_graph_known_authors()