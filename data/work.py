class Work:
    def __init__(self, name: str, year: int, authors: str, doc_type: str):
        self._name = name
        self._year = year
        self._authors = authors
        self._doc_type = doc_type

    COLUMN_AUTHOR = "Glavni autor"
    COLUMN_TITLE = "Naslov"
    COLUMN_YEAR= "Godina"
    COLUMN_AUTHORS= "Autori"

    COLUMN_IDX_AUTHOR = 1
    COLUMN_IDX_TITLE = 2
    COLUMN_IDX_YEAR = 3
    COLUMN_IDX_AUTHORS = 4

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, value):
        self._authors = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def doc_type(self):
        return self._doc_type

    @doc_type.setter
    def doc_type(self, value):
        self._doc_type = value
