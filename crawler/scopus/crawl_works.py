import os
import shutil
import time

import bibtexparser
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from data.workbooks.graph_edges_workbook import GraphEdgesWorkbook
from data.workbooks.works_workbook import WorksWorkbook, WORKS_WOS_FILE_NAME, WORKS_SHEET_NAME
from utilities.global_setup import PROXY, SELENIUM_CHROME_DRIVER_PATH, DATA_PATH
from bibtexparser.bparser import BibTexParser
import requests
import re
import openpyxl
from crawler.scopus.crawl_links import get_list_authors
from data.author import Author
from data.work import Work
from data.graph_edge import GraphEdge
from selenium import webdriver
from bibtexparser.customization import homogenize_latex_encoding, convert_to_unicode

REGEX_AUTHOR_STRING = "author\s*=\s*\{[\w ,-.()]+\},"
DOWNLOAD_FILE_PATH = DATA_PATH + "\\Work\\scopus"
TIME_LIMIT_WAIT = 60
WOS_TEXT_CELL = "ISI/Web of Science"
WOS_JOURNAL_RANG_TEXT_CELL = "Rang časopisa"
WOS_JOURNAL_IMPACT_FACTOR_TEXT_CELL = "oblast  / impakt faktor"
NUM_WORKS_PER_PAGE = 10
LAST_YEAR = 2017


class CrawlerLinksScopus:
    idx_gen = 0

    def __init__(self):
        self.list_authors = get_list_authors()
        list_name_authors = [author.id_name().lower() for author in self.list_authors]
        self.set_name_authors = set(list_name_authors)
        self.cur_row = 1
        self.user_agent = UserAgent()

    @staticmethod
    def format_middle_name(middle_name: str):
        return "" if middle_name == "" else "%20" + middle_name

    @staticmethod
    def parse_bib_tex_file(path: str):
        bib_tex_parser = BibTexParser()
        bib_tex_parser.customization = convert_to_unicode
        with open(path, encoding="utf-8") as bib_tex_file:
            bib_database = bib_tex_parser.parse_file(bib_tex_file)
        return bib_database.entries

    @staticmethod
    def init_driver_for_works_by_author(download_dir):
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        os.makedirs(download_dir)
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(SELENIUM_CHROME_DRIVER_PATH, chrome_options=options)
        return driver

    @staticmethod
    def wait_and_click(driver, x_path):
        webdriver_wait = WebDriverWait(driver, TIME_LIMIT_WAIT).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, x_path)))
        time.sleep(1)
        element = driver.find_element_by_xpath(x_path)
        element.click()

    @staticmethod
    def crawl_works_author(author: Author):
        SELECT_BOX_X_PATH = '//*[@id="export_results"]/span'
        STUPID_POP_UP_X_PATH = '//*[@id="_pendo-close-guide_"]'
        RADIO_BUTTON_X_PATH = '//*[@id="exportList"]/li[5]'
        EXPORT_BUTTON_X_PATH = '//*[@id="exportTrigger"]'
        works = {}
        # TODO: Test for deleting existing/creating multiple
        download_dir = "{}\\{}_{}".format(DOWNLOAD_FILE_PATH, author.last_name, author.first_name)
        driver = CrawlerLinksScopus.init_driver_for_works_by_author(download_dir)
        works = []
        print(author.first_name + " " + author.last_name)
        first_download = True

        for path in author.link.split(","):
            path = path.strip()
            print(path)
            driver.get(path)
            CrawlerLinksScopus.wait_and_click(driver, SELECT_BOX_X_PATH)
            if first_download:
                CrawlerLinksScopus.wait_and_click(driver, STUPID_POP_UP_X_PATH)
                first_download = False
            CrawlerLinksScopus.wait_and_click(driver, RADIO_BUTTON_X_PATH)
            CrawlerLinksScopus.wait_and_click(driver, EXPORT_BUTTON_X_PATH)
        time.sleep(.3)
        for file in os.listdir(download_dir):
            works += CrawlerLinksScopus.parse_bib_tex_file(os.path.join(download_dir, file))
        return works

    def get_random_header(self):
        return {"User-Agent": self.user_agent.random}

    def crawl_wos_and_journal_links(self, first_name: str, last_name: str, middle_name:str, number_works: int):
        wos_links = []
        journal_links = []
        num_pages = -(-number_works // NUM_WORKS_PER_PAGE)
        for offset in range(0, num_pages):
            path = KOBSON_WOS.format(last_name, first_name, CrawlerLinksScopus.format_middle_name(middle_name), offset)
            links_to_crawl = NUM_WORKS_PER_PAGE if (offset < (num_pages - 1)) \
                                                else number_works - (num_pages - 1) * NUM_WORKS_PER_PAGE
            print(links_to_crawl)
            r = requests.get(path, headers=self.get_random_header())
            r.encoding = "utf-8"
            data = r.text
            soup = BeautifulSoup(data)
            for green_rows in soup.find_all("tr", {"class": "greenRow"}):
                for rCell in green_rows.find_all("td", {"class": "rCell"}):
                    wos_link_added = False
                    journal_link = None
                    for link in rCell.find_all("a", href=True):
                        if (not wos_link_added) and (WOS_TEXT_CELL.lower() == link.text.strip().lower()):
                            wos_links.append(link.get('href'))
                            wos_link_added = True
                        if WOS_JOURNAL_RANG_TEXT_CELL.lower() == link.text.strip().lower():
                            journal_link = KOBSON_SERVICE_ROOT.format(link.get('href'))
                    journal_links.append(journal_link)
                links_to_crawl -= 1
                if links_to_crawl == 0:
                    break

        return journal_links, wos_links

    def get_num_citations(self, wos_link: str):
        r = requests.get(wos_link, headers=self.get_random_header())
        r.encoding = "utf-8"
        data = r.text
        soup = BeautifulSoup(data)
        for citation_div in soup.find_all("div", {"class": "flex-row-partition1"}):
            for num_citation in citation_div.find_all("span", {"class": "large-number"}):
                return num_citation.text

    @staticmethod
    def find_offset_year(table, year: int):
        for row in table.find_all("tr"):
            row_header_elem = row.find("td", {"class": "first dblue"})
            if row_header_elem is not None:
                for offset, cell in enumerate(row.find_all("td", {"class": "dblue"})):
                    if cell.text == str(year):
                        return offset

    @staticmethod
    def get_impact_factor(soup: BeautifulSoup, is_five_year, year: int):
        skip_impact_factor = is_five_year
        skip_header = True
        for data_div in soup.find_all("div", {"class": "resultHolder"}):
            if skip_header:
                skip_header = False
                continue
            for table in data_div.find_all("table", {"class": "type categories results"}):
                if skip_impact_factor:
                    skip_impact_factor = False
                    continue
                offset = CrawlerLinksScopus.find_offset_year(table, year)
                if offset is None:
                    return None
                for row in table.find_all("tr"):
                    row_header_elem = row.find("td", {"class": "first lblue"})
                    row_header = "" if row_header_elem is None else row_header_elem.text
                    if row_header.lower() == WOS_JOURNAL_IMPACT_FACTOR_TEXT_CELL.lower():
                        return row.find_all("td", {"class": "lblue"})[offset].text

    def get_impact_factors(self, journal_link: str, year: int):
        if journal_link is None:
            return "", ""
        r = requests.get(journal_link, headers=self.get_random_header())
        r.encoding = "utf-8"
        data = r.text
        soup = BeautifulSoup(data)
        impact_factor_2017 = CrawlerLinksScopus.get_impact_factor(soup, False, year)
        impact_factor_2017 = "" if impact_factor_2017 is None else impact_factor_2017
        impact_factor5_2017 = CrawlerLinksScopus.get_impact_factor(soup, True, year)
        impact_factor5_2017 = "" if impact_factor5_2017 is None else impact_factor5_2017
        return impact_factor_2017, impact_factor5_2017

    def crawl_works(self):
        works_work_book = WorksWorkbook(is_wos=False)

        for author in self.list_authors:
            if author.link != "":
                works = CrawlerLinksScopus.crawl_works_author(author)
                '''
                journal_links, wos_links = self.crawl_wos_and_journal_links(
                                            author.first_name, author.last_name.replace(" ", "-"),
                                            author.middle_name, works.__len__())
                print("Number of works {}".format(works.__len__()))
                '''
                for work_id, work_bib in enumerate(works):
                    '''
                    impact_factor, impact_factor5 = self.get_impact_factors(journal_links[work_id], LAST_YEAR)
                    num_citations = self.get_num_citations(wos_links[work_id])
                    print("if{} if5{} num_cit {}".format(impact_factor, impact_factor5, num_citations))
                    '''
                    work = Work(title=work_bib["title"], authors=work_bib["author"].replace("-", " "),
                                year=work_bib["year"], doc_type=work_bib['document_type'],
                                author="{} {} {}".format(author.last_name, author.first_name, author.middle_name).strip(),
                                num_citations=0,
                                document_name=work_bib.get('journal', ""),
                                impact_factor=0, impact_factor5=0,
                                department=author.department, faculty=author.faculty)
                    works_work_book.save_work(work)
                    print(work_bib["title"])
            else:
                print("No works available")
        works_work_book.save()

    def generate_graph_known_authors(self):
        work_book_works = openpyxl.load_workbook(filename=WORKS_WOS_FILE_NAME)
        sheet = work_book_works[WORKS_SHEET_NAME]
        work_book_edges = GraphEdgesWorkbook()
        for row in range(2, sheet.max_row + 1):
            author1 = sheet.cell(row, Work.COLUMN_IDX_AUTHOR).value.lower()
            authors = sheet.cell(row, Work.COLUMN_IDX_AUTHORS).value.lower()
            for author2 in authors.split(","):
                if author2 in self.set_name_authors:
                    edge = GraphEdge(author1, author2)
                    work_book_edges.save_graph_edge(edge)
        work_book_edges.save()

    def generate_graph_authors(self):
        pass


if __name__ == "__main__":
    crawler = CrawlerLinksScopus()
    crawler.crawl_works()
    '''author = Author("Zoran", "Jovanovic", link=r'https://www.scopus.com/inward/authorDetails.uri?authorID=35752271100&partnerID=5ESL7QZV&md5=5fd29a5403fe3e4fd43d549feb2cd24f, https://www.scopus.com/inward/authorDetails.uri?authorID=56806526500&partnerID=5ESL7QZV&md5=8005150446cb614a87c214a079ef909b',
                    department='a', faculty='b')
    '''
