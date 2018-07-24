from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from utilities.global_setup import PROXY
import requests

TITLE_WORDS = ["dr", "mr", "ms", "doc.", "prof.", "as."]


class CrawlerFaculty(ABC):
    def __init__(self, home_page: str):
        self.home_page = home_page

    @abstractmethod
    def parse_specific(self, soup: BeautifulSoup):
        pass

    def parse(self):
        r = requests.get(self.home_page, proxies=PROXY)
        r.encoding = "utf-8"
        data = r.text
        soup = BeautifulSoup(data)
        personnel_names = self.parse_specific(soup)
        personnel_names_without_title = []
        for personnel_name in personnel_names:
            for title in TITLE_WORDS:
                personnel_name = personnel_name.replace(title + " ", "")
            personnel_names_without_title.append(personnel_name)
        return personnel_names_without_title
