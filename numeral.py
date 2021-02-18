
from yargy import (
    rule,
    and_, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)
#from numeralClass import NUMERALS

Numeral = fact(
    'Numeral',
    ['trillion', 'billion', 'million', 'nthousand', 'thousand', 'hundred', 'dozen', 'num', 'plural']
)

class Numeral(Numeral):
    @property
    def obj(self):
        from extractors import Numeral
        return Numeral(self.trillion, self.billion, self.million, self.nthousand, self.thousand, self.hundred, self.dozen, self.num, self.plural)

NUMERALS = {
    'первый': 1,
    'первое': 1,
    'один': 1,
    'второй': 2,
    'два': 2,
    'третье': 3,
    'три': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'седьмой': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,



    'двухтысячный': 2000,



}

TRILLION = { 'триллион': 1000000000000 }

MILLION = { 'миллион': 1000000 }

BILLION = { 'миллиард': 1000000000 }

THOUSAND = { 'тысяча': 1000 }  # "Съедает даже "тыс"

HUNDRED = {
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
}

DOZEN = {
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
}

PLURAL = {
    #'первые': '1-ых',
    #'первых': '1-ых',
    'десятые': '10-ых',
    'десятых': '10-ых',
    'двадцатые': '20-ые',
    'двадцатых': '20-ых',
    'тридцатые': '30-ые',
    'тридцатых': '30-ых',
    'сороковые': '40-ые',
    'сороковых': '40-ых',
    'пятидесятые': '50-ые',
    'пятидесятых': '50-ых',
    'шестидесятые': '60-ые',
    'шестидесятых': '60-ых',
    'семидесятые': '70-ые',
    'семидесятых': '70-ых',
    'восьмидесятые': '80-ые',  # В ПЕРВЫХ ЧИСЛАХ МАЯ??????
    'восьмидесятых': '80-ых',
    'девяностые': '90-ые',
    'девяностых': '90-ых',
    'двухтысячные': '2000-ые',
    'двухтысячных': '20-ых',

    'I': '1',
    'II': '2',
    'III': '3',
    'IV': '4',
    'V': '5',
    'VI': '6',
    'VI': '7',
    'VIII': '8',
    'IX': '9',
    'X': '10',
    'XI': '11',
    'XII': '12',
    'XIII': '13',
    'XIV': '14',
    'XV': '15',
    'XVI': '16',
    'XVII': '17',
    'XVIII': '18',
    'XIX': '19',
    'XX': '20',
    'XXI': '21',
    'XXII': '22',
    'XXIII': '23',
    'XXIV': '24',
    'XXV': '25',
    'XXVI': '26',
    'XXVII': '27',
    'XXVIII': '28',
    'XXIX': '29',
    'XXX': '30',
    'XXXI': '31',
    'XXXII': '32',
    'XXXIII': '33',
    'XXXIV': '34',
    'XXXV': '35',
    'XXXVI': '36',
    'XXXVII': '37',
    'XXXVIII': '38',
    'XXXIX': '39',
    'XL': '40',

}

# ROMAN = {
#     'M': 1000,
#     'CM': 900,
#     'D': 500,
#     'CD': 400,
#     'C': 100,
#     'XC': 90,
#     'L': 50,
#     'XL': 40,
#     'X': 10,
#     'IX': 9,
#     'V': 5,
#     'IV': 4,
#     'I': 1,
# }

# Перевод числительных в числа (нет аналогов)
NUMERALS_n = dictionary(NUMERALS).interpretation(
    Numeral.num.normalized().custom(NUMERALS.__getitem__)
)
NUMERALS_d = dictionary(DOZEN).interpretation(
    Numeral.dozen.normalized().custom(DOZEN.__getitem__)

)
NUMERALS_h = dictionary(HUNDRED).interpretation(
    Numeral.hundred.normalized().custom(HUNDRED.__getitem__)
)
NUMERALS_nt = dictionary(NUMERALS).interpretation(
    Numeral.nthousand.normalized().custom(NUMERALS.__getitem__)
)
NUMERALS_t = dictionary(THOUSAND).interpretation(
    Numeral.thousand.normalized().custom(THOUSAND.__getitem__)
)
NUMERALS_m = dictionary(MILLION).interpretation(
    Numeral.million.normalized().custom(MILLION.__getitem__)
)
NUMERALS_b = dictionary(BILLION).interpretation(
    Numeral.billion.normalized().custom(BILLION.__getitem__)
)
NUMERALS_tl = dictionary(TRILLION).interpretation(
    Numeral.trillion.normalized().custom(TRILLION.__getitem__)
)

NUMERALS_p = dictionary(PLURAL).interpretation(
    Numeral.plural.custom(PLURAL.__getitem__)

)

NUMERAL = or_(
    # rule(
    #     NUMERALS_n,
    #     NUMERALS_tl
    # ),
    rule(
        NUMERALS_p
    ),
    rule(
        NUMERALS_m,
        NUMERALS_nt.optional(),
        NUMERALS_t,
        NUMERALS_h.optional(),
        NUMERALS_d.optional(),
        NUMERALS_n.optional()
    ),
    rule(
        NUMERALS_nt.optional(),
        NUMERALS_t,
        NUMERALS_h.optional(),
        NUMERALS_d.optional(),
        NUMERALS_n.optional()
    ),
    rule(
        NUMERALS_h,
        NUMERALS_d.optional(),
        NUMERALS_n.optional()
    ),
    rule(
        NUMERALS_d,
        NUMERALS_n.optional()
    ),
    rule(
        NUMERALS_n
    )
).interpretation(
    Numeral
)