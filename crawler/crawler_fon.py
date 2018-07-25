from bs4 import BeautifulSoup
import requests
import re
from crawler.crawler_faculty import CrawlerFaculty
from language.language_converter import CyrillicLatin

FON_PERSONNEL_URL = "http://www.fon.bg.ac.rs/o-fakultetu/organizacija/nastavnici/"
CS_DEPARTMENTS = set(["Katedra za informacione sisteme",
                      "Katedra za informacione tehnologije",
                      "Katedra za softversko inzenjerstvo"])
FON_FACULTY_NAME = "fakultet organizacionih nauka"
REGEX_DEPARTMENT = re.compile("(?<=class=\"teacher_department\">)(?:\s*)([\w .]+)(?:\s*)")


class CrawlerFon(CrawlerFaculty):
    def __init__(self):
        super().__init__(FON_FACULTY_NAME, FON_PERSONNEL_URL, True)

    @staticmethod
    def parse_department(teacher_path):
        r = requests.get(teacher_path)
        r.encoding = "utf-8"
        data = r.text
        reg_search = REGEX_DEPARTMENT.search(data)
        department = "" if reg_search is None else REGEX_DEPARTMENT.search(data).group(1)
        return department

    def parse_specific(self, soup: BeautifulSoup):
        personnel_names = []
        departments = []
        for body in soup.find_all("table", {"class": "tabelanastavnika"}):
            for list_personnel in body.find_all("td"):
                for list_item in list_personnel.find_all('a', href=True):
                    personnel_path = list_item.get('href')
                    personnel_path = "" if personnel_path is None else personnel_path.strip()
                    department = CyrillicLatin.convert_serbian_cyrillic_to_serbian_latin(
                                    CrawlerFon.parse_department(FON_PERSONNEL_URL + personnel_path))
                    department = CyrillicLatin.convert_serb_latin_to_latin(department)
                    if (personnel_path != '') and (department in CS_DEPARTMENTS):
                        personnel_names.append(personnel_path)
                        departments.append(department)
        return departments, [personnel_name.replace("-", " ") for personnel_name in personnel_names]


if __name__ == "__main__":
    authors = CrawlerFon().parse()
    for author in authors:
        print(author)
    print(authors.__len__())
