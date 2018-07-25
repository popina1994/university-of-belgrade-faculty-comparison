from crawler.authors.crawler_etf import CrawlerEtf
from crawler.authors.crawler_matf import CrawlerMatf
from crawler.authors.crawler_fon import CrawlerFon
from data.workbooks.authors_workbook import AuthorsWorkbook

if __name__ == "__main__":
    faculties = [CrawlerMatf(), CrawlerEtf(), CrawlerFon()]
    authorsWorkBook = AuthorsWorkbook()
    for faculty in faculties:
        authors = faculty.parse()
        for author in authors:
            print(author)
        print(authors.__len__())
        authorsWorkBook.save_authors(authors, faculty.faculty_name)
    authorsWorkBook.save()
