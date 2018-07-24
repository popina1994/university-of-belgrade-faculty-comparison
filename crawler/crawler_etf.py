from bs4 import BeautifulSoup
import re
from crawler.crawler_faculty import CrawlerFaculty
from language.language_converter import CyrillicLatin

ETF_PERSONNEL_URL = "https://www.etf.bg.ac.rs/sr/katedre/katedra-za-racunarsku-tehniku-i-informatiku"
REGEX_NAME = re.compile("(?<=>)(?:\s*)([\w .]+)(?:\s*)")


class CrawlerEtf(CrawlerFaculty):
    def __init__(self):
        super().__init__(ETF_PERSONNEL_URL)

    def parse_specific(self, soup: BeautifulSoup):
        personnel_names = []
        for body in soup.find_all("div", {"class": "strana-body"}):
            for list_personnel in body.find_all("ul"):
                for list_item in list_personnel.find_all('a', href=True):
                    personnel_name = REGEX_NAME.search(str(list_item)).group(1)
                    personnel_name = "" if personnel_name is None else personnel_name.strip()
                    if personnel_name != '':
                        personnel_names.append(personnel_name)

        return list(map(CyrillicLatin.convert_serb_latin_to_latin,
                    map(CyrillicLatin.convert_serbian_cyrillic_to_serbian_latin, personnel_names)))


if __name__ == "__main__":
    professors = CrawlerEtf().parse()
    for professor in professors:
        print(professor)
    print(professors.__len__())
