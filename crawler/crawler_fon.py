from bs4 import BeautifulSoup
import requests
import re
from crawler.crawler_faculty import CrawlerFaculty

FON_PERSONNEL_URL = "http://www.fon.bg.ac.rs/o-fakultetu/organizacija/nastavnici/"
CS_DEPARTMENTS = set(["Катедра за информационе системе",
                      "Катедра за информационе технологије",
                      "Катедра за софтверско инжењерство"])
REGEX_DEPARTMENT = re.compile("(?<=class=\"teacher_department\">)(?:\s*)([\w .]+)(?:\s*)")

class CrawlerFon(CrawlerFaculty):
    def __init__(self):
        super().__init__(FON_PERSONNEL_URL, True)

    @staticmethod
    def is_computer_science(teacher_path):
        r = requests.get(teacher_path)
        r.encoding = "utf-8"
        data = r.text
        reg_search = REGEX_DEPARTMENT.search(data)
        department = None if reg_search is None else REGEX_DEPARTMENT.search(data).group(1)
        print(teacher_path)
        if department is not None:
            print(department)
        return department in CS_DEPARTMENTS

    def parse_specific(self, soup: BeautifulSoup):
        personnel_names = []
        for body in soup.find_all("table", {"class": "tabelanastavnika"}):
            for list_personnel in body.find_all("td"):
                for list_item in list_personnel.find_all('a', href=True):
                    personnel_path = list_item.get('href')
                    personnel_path = "" if personnel_path is None else personnel_path.strip()
                    if (personnel_path != '') and \
                            (CrawlerFon.is_computer_science(FON_PERSONNEL_URL + personnel_path)):
                        personnel_names.append(personnel_path)
        return [personnel_name.replace("-", " ") for personnel_name in personnel_names]


if __name__ == "__main__":
    professors = CrawlerFon().parse()
    for professor in professors:
        print(professor)
    print(professors.__len__())
