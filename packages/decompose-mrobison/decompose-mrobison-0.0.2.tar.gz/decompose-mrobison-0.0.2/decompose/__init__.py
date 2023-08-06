from unicodedata import normalize

charmap = {
        u'\N{Latin capital letter AE}': 'Ae',
        u'\N{Latin small letter ae}': 'ae',
        u'\N{Latin capital letter Eth}': 'D',
        u'\N{Latin small letter eth}': 'd',
        u'\N{Latin capital letter O with stroke}': 'O',
        u'\N{Latin small letter o with stroke}': 'o',
        u'\N{Latin capital letter Thorn}': 'Th',
        u'\N{Latin small letter thorn}': 'th',
        u'\N{Latin small letter sharp s}': 'ss',
        u'\N{Latin capital letter sharp s}': 'SS',
        u'\N{Latin capital letter D with stroke}': 'D',
        u'\N{Latin small letter d with stroke}': 'd',
        u'\N{Latin capital letter H with stroke}': 'H',
        u'\N{Latin small letter h with stroke}': 'h',
        u'\N{Latin small letter dotless i}': 'i',
        u'\N{Latin small letter kra}': 'k',
        u'\N{Latin capital letter L with stroke}': 'L',
        u'\N{Latin small letter l with stroke}': 'l',
        u'\N{Latin capital letter Eng}': 'N',
        u'\N{Latin small letter eng}': 'n',
        u'\N{Latin capital ligature OE}': 'Oe',
        u'\N{Latin small ligature oe}': 'oe',
        u'\N{Latin capital letter T with stroke}': 'T',
        u'\N{Latin small letter t with stroke}': 't',
}


def decompose(s: str):
    for k, v in charmap.items():
        s = s.replace(k, v)

    return normalize('NFKD', s).encode('ASCII', 'ignore').decode()
