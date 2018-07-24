from bs4 import BeautifulSoup
from language.language_converter import CyrillicLatin
import re
from crawler.crawler_faculty import CrawlerFaculty

MATF_PERSONNEL_URL = "http://www.racunarstvo.matf.bg.ac.rs/?content=zaposleni"
REGEX_NAME = re.compile("(?<=<br/>)(?:\s*)([\w ]+)(?:\s*)")


class CrawlerMatf(CrawlerFaculty):
    def __init__(self):
        super().__init__(MATF_PERSONNEL_URL)

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
        return list(map(CyrillicLatin.convert_serb_latin_to_latin, personnel_names))


if __name__ == "__main__":
    professors = CrawlerMatf().parse()
    for professor in professors:
        print(professor)
    print(professors.__len__())
