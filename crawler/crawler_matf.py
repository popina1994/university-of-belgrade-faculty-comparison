from bs4 import BeautifulSoup
from language.language_converter import CyrillicLatin
import re
from crawler.crawler_faculty import CrawlerFaculty

MATF_PERSONNEL_URL = "http://www.racunarstvo.matf.bg.ac.rs/?content=zaposleni"
MATF_DEPARTMENT = "katedra za racunarstvo i informatiku"
MATF_FACULTY_NAME = "matematicki fakultet"
REGEX_NAME = re.compile("(?<=<br/>)(?:\s*)([\w ]+)(?:\s*)")


class CrawlerMatf(CrawlerFaculty):
    def __init__(self):
        super().__init__(MATF_FACULTY_NAME, MATF_PERSONNEL_URL)

    def parse_specific(self, soup: BeautifulSoup):
        personnel_names = []
        count_types = 0
        for list_personnel in soup.find_all("ul", {"class": "personnel"}):
            for list_item in list_personnel.find_all('a', href=True):
                personnel_name = REGEX_NAME.search(str(list_item)).group(1)
                personnel_name = "" if personnel_name is None else personnel_name.strip()
                if personnel_name != '':
                    personnel_names.append(personnel_name)
            count_types += 1
            if count_types == 5:
                break
        personnel_names = list(map(CyrillicLatin.convert_serb_latin_to_latin, personnel_names))
        departments = [MATF_DEPARTMENT] * len(personnel_names)
        return departments, personnel_names


if __name__ == "__main__":
    authors = CrawlerMatf().parse()
    for author in authors:
        print(author)
    print(authors.__len__())
