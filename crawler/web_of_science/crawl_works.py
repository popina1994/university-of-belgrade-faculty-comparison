from utilities.global_setup import PROXY
from bibtexparser.bparser import BibTexParser
import requests
import re
from openpyxl import Workbook
from crawler.web_of_science.crawl_names import get_list_authors
from utilities.global_setup import DATA_PATH
from data.author import Author
from data.work import Work

REGEX_AUTHOR_STRING = "author\s*=\s*\{[\w ,-.()]+\},"
KOBSON_WOS_BIBTEX = "http://kobson.nb.rs/aspx/wos/export.aspx?autor={}%20{}{}&samoar=&format=BibTeX"
WORKS_WOS_FILE_NAME = DATA_PATH + r"\Work\works_wos.xlsx"
WORKS_WOS_SHEET_NAME = "Radovi"


class CrawlerLinksWos:
    idx_gen = 0

    def __init__(self):
        self.list_authors = get_list_authors()
        self.set_authors = set(self.list_authors)
        self.work_book = Workbook()
        self.work_book.remove(self.work_book.active)
        works_sheet = self.work_book.create_sheet(WORKS_WOS_SHEET_NAME)
        works_sheet.title = WORKS_WOS_SHEET_NAME
        works_sheet.cell(1, Work.COLUMN_IDX_AUTHOR).value = Work.COLUMN_AUTHOR
        works_sheet.cell(1, Work.COLUMN_IDX_TITLE).value = Work.COLUMN_TITLE
        works_sheet.cell(1, Work.COLUMN_IDX_YEAR).value = Work.COLUMN_YEAR
        works_sheet.cell(1, Work.COLUMN_IDX_AUTHORS).value = Work.COLUMN_AUTHORS
        self.cur_row = 2

    @staticmethod
    def format_middle_name(middle_name: str):
        return "" if middle_name == "" else "%20" + middle_name

    @staticmethod
    def parse_bib_tex(bib_tex: str):
        bib_tex_parser = BibTexParser()
        bib_database = bib_tex_parser.parse(bib_tex)
        return bib_database.entries

    @staticmethod
    def crawl_works_author(first_name: str, last_name: str, middle_name: str):
        path = KOBSON_WOS_BIBTEX.format(last_name, first_name, CrawlerLinksWos.format_middle_name(middle_name))
        r = requests.get(path, proxies=PROXY)
        r.encoding = "utf-8"
        data = r.text
        data_structured = re.sub("(" + REGEX_AUTHOR_STRING + ")", r"{},\r\n\1".format(CrawlerLinksWos.idx_gen), data)
        CrawlerLinksWos.idx_gen += 1
        return path, CrawlerLinksWos.parse_bib_tex(data_structured)

    def add_work_to_table(self, first_name: str, last_name: str, middle_name: str,
                          title: str, authors: str, year: str):
        works_sheet = self.work_book[WORKS_WOS_SHEET_NAME]
        works_sheet.cell(self.cur_row, Work.COLUMN_IDX_AUTHOR).value = (first_name + " " + last_name + " " + middle_name).strip()
        works_sheet.cell(self.cur_row, Work.COLUMN_IDX_TITLE).value = title
        works_sheet.cell(self.cur_row, Work.COLUMN_IDX_YEAR).value = year
        works_sheet.cell(self.cur_row, Work.COLUMN_IDX_AUTHORS).value = authors
        self.cur_row += 1

    def crawl_works(self):
        for author in self.list_authors:
            print("{} {} {}".format(author.first_name, author.last_name, author.middle_name))
            if author.middle_name != Author.MIDDLE_NAME_NOT_FOUND:
                path, works = CrawlerLinksWos.crawl_works_author(author.first_name,
                                                                 author.last_name.replace(" ", "-"),
                                                                 author.middle_name)
                print("Number of works {}".format(works.__len__()))
                for work in works:
                    self.add_work_to_table(author.first_name, author.last_name, author.middle_name,
                                           work["title"], work["author"], work["year"])
                    print(work["title"])
            else:
                print("No works available")

        self.work_book.save(WORKS_WOS_FILE_NAME)


if __name__ == "__main__":
    '''
    data = """@ARTICLE{
year={2018},
author={Petrovic-Savic Suzana,Ristic Branko M,Jovanovic Zoran,Matic Aleksandar,Prodanovic Nikola S,Anwer Nabil,Qiao Lihong,Devedzic Goran B},
title={Parametric Model Variability of the Proximal Femoral Sculptural Shape},
journal={INTERNATIONAL JOURNAL OF PRECISION ENGINEERING AND MANUFACTURING},
volume={19},
number={7},
pages={1047-1054},
document_type={Article},
}
    """
    '''
    crawler = CrawlerLinksWos()
    crawler.crawl_works()
    #print(crawl_works_author("jovanovic", "zoran", ""))
    #print(parse_bib_tex(data))
