class CyrillicLatin:
    SERBIAN_CYRILLIC_ALPHABET = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к',
                                 'л', 'љ', 'м', 'н', 'њ', 'о', 'п', 'р', 'с', 'т', 'ћ', 'у',
                                 'ф', 'х', 'ц', 'ч', 'џ', 'ш', 'А', 'Б', 'В', 'Г', 'Д', 'Ђ', 'Ђ',
                                 'Е', 'Ж', 'З', 'И', 'Ј', 'К', 'Л', 'Љ', 'М', 'Н', 'Њ', 'О',
                                 'П', 'Р', 'С', 'Т', 'Ћ', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Џ', 'Ш']
    SERBIAN_LATIN_ALPHABET = ['a', 'b', 'v', 'g', 'd', 'đ', 'e', 'ž', 'z', 'i', 'j', 'k',
                              'l', 'lj', 'm', 'n', 'nj', 'o', 'p', 'r', 's', 't', 'ć', 'u',
                              'f', 'h', 'c', 'č', 'dž', 'š', 'A', 'B', 'V', 'G', 'D', 'Đ', 'ð',
                              'E', 'Ž', 'Z', 'I', 'J', 'K', 'L', 'Lj', 'M', 'N', 'Nj', 'O',
                              'P', 'R', 'S', 'T', 'Ć', 'U', 'F', 'H', 'C', 'Č', 'Dž', 'Š']
    LATIN_ALPHABET = ['a', 'b', 'v', 'g', 'd', 'dj', 'e', 'z', 'z', 'i', 'j', 'k',
                      'l', 'lj', 'm', 'n', 'nj', 'o', 'p', 'r', 's', 't', 'c', 'u',
                      'f', 'h', 'c', 'c', 'dz', 's', 'A', 'B', 'V', 'G', 'D', 'Dj', 'Dj',
                      'E', 'Z', 'Z', 'I', 'J', 'K', 'L', 'Lj', 'M', 'N', 'Nj', 'O',
                      'P', 'R', 'S', 'T', 'C', 'U', 'F', 'H', 'C', 'C', 'Dz', 'S']
    #NASTY HACK: with 'ð', works because index returns the first apperance of an element.
    SERBIAN_CYRILLIC_SERBIAN_LATIN_ALPHABET = {}
    SERBIAN_LATIN_LATIN_ALPHABET = {}
    for letter in SERBIAN_CYRILLIC_ALPHABET:
        SERBIAN_CYRILLIC_SERBIAN_LATIN_ALPHABET[letter] = \
            SERBIAN_LATIN_ALPHABET[SERBIAN_CYRILLIC_ALPHABET.index(letter)]
    for letter in SERBIAN_LATIN_ALPHABET:
        SERBIAN_LATIN_LATIN_ALPHABET[letter] = \
            LATIN_ALPHABET[SERBIAN_LATIN_ALPHABET.index(letter)]

    @staticmethod
    def convert_serbian_cyrillic_to_serbian_latin(string: str):
        conv_str = ""
        if string is None:
            return conv_str
        for letter in string:
            latin_letter = CyrillicLatin.SERBIAN_CYRILLIC_SERBIAN_LATIN_ALPHABET.get(letter, letter)
            conv_str += latin_letter
        return conv_str

    @staticmethod
    def convert_serb_latin_to_latin(string):
        conv_str = ""
        if string is None:
            return conv_str
        for letter in string:
            latin_letter = CyrillicLatin.SERBIAN_LATIN_LATIN_ALPHABET.get(letter, letter)
            conv_str += latin_letter
        return conv_str


