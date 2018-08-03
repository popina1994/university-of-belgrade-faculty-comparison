from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from utilities.global_setup import PROXY, SELENIUM_CHROME_DRIVER_PATH
from data.author import Author
import requests

TITLE_WORDS = ["dr", "mr", "ms", "doc.", "prof.", "as."]


class CrawlerFaculty(ABC):
    def __init__(self, faculty_name: str, home_page: str, use_source: bool = False):
        self.faculty_name = faculty_name
        self.home_page = home_page
        self.use_source = use_source

    @abstractmethod
    def parse_specific(self, soup: BeautifulSoup):
        pass

    @staticmethod
    def extract_first_last_name(personnel_name: str):
        pos_sep = personnel_name.find(" ")
        return personnel_name[:pos_sep], personnel_name[pos_sep+1:]

    def parse(self):
        if self.use_source:
            driver = webdriver.Chrome(SELENIUM_CHROME_DRIVER_PATH)
            driver.get(self.home_page)
            data = driver.page_source
        else:
            r = requests.get(self.home_page, proxies=PROXY)
            r.encoding = "utf-8"
            data = r.text
        soup = BeautifulSoup(data)
        departments, personnel_names = self.parse_specific(soup)
        personnel_names_without_title = []
        for personnel_name in personnel_names:
            for title in TITLE_WORDS:
                personnel_name = personnel_name.replace(title + " ", "")
            personnel_names_without_title.append(personnel_name)

        authors = []
        for idx, personnel_name in enumerate(personnel_names_without_title):
            first_name, last_name = CrawlerFaculty.extra_first_last_name(personnel_name)
            author = Author(first_name, last_name, departments[idx], self.faculty_name)
            authors.append(author)
        return authors
