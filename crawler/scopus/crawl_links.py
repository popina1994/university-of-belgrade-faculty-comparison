import requests
from bs4 import BeautifulSoup
import openpyxl
from crawler.web_of_science.crawl_names import  AUTHORS_WOS_FILE_NAME
from data.author import Author
from language.language_converter import CyrillicLatin

SCOPUS_PATH = "https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&affilName=University+of+Belgrade&sid=8a5f928c9f2a3530c144238b9d2f5e02&sot=al&sdt=al&sl=74&s=AUTHLASTNAME%28{}%29+AND+AUTHFIRST%28{}%29+AND+AFFIL%28University+of+Belgrade%29&st1={}&st2={}&orcidId=&selectionPageSearch=anl&reselectAuthor=false&activeFlag=true&showDocument=false&resultsPerPage=20&offset=1&jtp=false&currentPage=1&previousSelectionCount=0&tooManySelections=false&previousResultCount=0&authSubject=LFSC&authSubject=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch=false&showFullList=false&authorPreferredName=&origin=searchauthorfreelookup&affiliationId=&txGid=855cc953ff2e66c64f5d95ddb748ce36"
AUTHORS_SCOPUS_FILE_NAME = r"C:\Users\popina\Dropbox\Fakultet\Master Thesis\Data\People\authors_scopus.xlsx"


def crawl_links(first_name: str, last_name: str, middle_name: str):
    path = SCOPUS_PATH.format(last_name, first_name, last_name, first_name)
    r = requests.get(path)
    r.encoding = "utf-8"
    data = r.text
    soup = BeautifulSoup(data)
    link = ""
    for results in soup.find_all("td", {"class": "authorResultsNamesCol col20"}):
        for full_name_a in results.find_all('a', href=True):
            full_name = full_name_a.string.strip()
            full_name = CyrillicLatin.convert_serb_latin_to_latin(
                            full_name.replace(".", "").replace(",", ""))
            sub_names = full_name.split(" ")
            middle_name_crawl = sub_names[-1] if sub_names.__len__() == 3 else ""
            print("middle_name" + middle_name)
            if (sub_names[0].lower() != last_name.lower()) or\
               (sub_names[1].lower() != first_name.lower()) or\
               ((middle_name != Author.MIDDLE_NAME_NOT_FOUND) and (middle_name_crawl != middle_name)):
                continue
            link = full_name_a['href']
            print(first_name + " " + last_name + " " + link)

    return link


def update_links():
    work_book = openpyxl.load_workbook(filename=AUTHORS_WOS_FILE_NAME)
    for sheet in work_book.worksheets:
        sheet.cell(1, Author.COLUMN_IDX_LINK).value = Author.COLUMN_LINK_NAME
        for row in range(2, sheet.max_row):
            first_name = sheet.cell(row, Author.COLUMN_IDX_FIRST_NAME).value
            last_name = sheet.cell(row, Author.COLUMN_IDX_LAST_NAME).value
            middle_names = sheet.cell(row, Author.COLUMN_IDX_MIDDLE_NAME).value
            middle_names = "" if middle_names is None else middle_names
            middle_names_sub = middle_names.split(",")
            cnt = 0
            for middle_name in middle_names_sub:
                link = crawl_links(first_name, last_name.replace(" ", "-"), middle_name)
                if cnt != 0:
                    link = sheet.cell(row, Author.COLUMN_IDX_LINK).value + "," + link
                sheet.cell(row, Author.COLUMN_IDX_LINK).value = link
                cnt += 1
    work_book.save(AUTHORS_SCOPUS_FILE_NAME)


if __name__ == "__main__":
    update_links()
