from bs4 import BeautifulSoup
import re
from crawler.authors.crawler_faculty import CrawlerFaculty
from language.language_converter import CyrillicLatin

ETF_PERSONNEL_URL = "https://www.etf.bg.ac.rs/sr/katedre/katedra-za-racunarsku-tehniku-i-informatiku"
ETF_DEPARTMENT = "katedra za racunarsku tehniku i informatiku"
ETF_FACULTY_NAME = "elektrotehnicki fakultet"
REGEX_NAME = re.compile("(?<=>)(?:\s*)([\w .]+)(?:\s*)")


class CrawlerEtf(CrawlerFaculty):
    def __init__(self):
        super().__init__(ETF_FACULTY_NAME, ETF_PERSONNEL_URL)

    def parse_specific(self, soup: BeautifulSoup):
        personnel_names = []
        for body in soup.find_all("div", {"class": "strana-body"}):
            for list_personnel in body.find_all("ul"):
                for list_item in list_personnel.find_all('a', href=True):
                    personnel_name = REGEX_NAME.search(str(list_item)).group(1)
                    personnel_name = "" if personnel_name is None else personnel_name.strip()
                    if personnel_name != '':
                        personnel_names.append(personnel_name)

        personnel_names = list(map(CyrillicLatin.convert_serb_latin_to_latin,
                               map(CyrillicLatin.convert_serbian_cyrillic_to_serbian_latin,
                                   personnel_names)))
        departments = [ETF_DEPARTMENT] * len(personnel_names)
        return departments, personnel_names


if __name__ == "__main__":
    authors = CrawlerEtf().parse()
    for author in authors:
        print(author)
    print(authors.__len__())
