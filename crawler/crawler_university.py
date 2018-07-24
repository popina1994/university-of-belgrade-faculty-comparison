from crawler.crawler_etf import CrawlerEtf
from crawler.crawler_matf import CrawlerMatf

if __name__ == "__main__":
    faculties = [CrawlerMatf(), CrawlerEtf()]
    for faculty in faculties:
        professors = faculty.parse()
        for professor in professors:
            print(professor)
        print(professors.__len__())
