
from yargy import (
    rule,
    and_, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)

# Отправить era
# Неполный год - XXXX

Date = fact(
    'Date',
    ['era', 'millennium', 'century', 'year', 'month', 'day', 'week', 'dayweek', 'decade', 'season', 'half', 'third', 'quarter', 'place', 's']  # s - ые
)


class Date(Date):
    @property
    def obj(self):
        from extractors import Date
        return Date(self.era, self.millennium, self.century, self.year, self.month, self.day, self.week,
                    self.dayweek, self.decade, self.season, self.half, self.third, self.quarter, self.place, self.s)


# День недели
DAYWEEK = {
    'понедельник': 1,
    'пон': 1,
    'вторник': 2,
    'вт': 2,
    'среда': 3,
    'ср': 3,   # среднее:
    'четверг': 4,
    'чет': 4,  # чётность?
    'пятница': 5,
    'пят': 5,
    'суббота': 6,
    'суб': 6,
    'воскресенье': 7,
    'вос': 7
}

# Месяц (учтены стандартные сокращения)
MONTHS = {
    'январь': 1,
    'янв': 1,
    'февраль': 2,
    'фев': 2,
    'март': 3,
    'мар': 3,
    'апрель': 4,
    'апр': 4,
    'мая': 5,
    'май': 5,
    'июнь': 6,
    'июн': 6,
    'июль': 7,
    'июл': 7,
    'август': 8,
    'авг': 8,
    'сентябрь': 9,
    'сен': 9,
    'октябрь': 10,
    'двести': 10,
    'окт': 10,
    'ноябрь': 11,
    'ноя': 11,
    'декабрь': 12,
    'дек': 12
}

SEASONS = {
    'зима': 'WI',
    'зимой': 'WI',
    'весна': 'SP',
    'весной': 'SP',
    'лето': 'SU',
    'летом': 'SU',
    'осень': 'FA',
    'осенью': 'FA',
}

ERAS = {
    'до н.э.': 'BC',
    'до н. э.': 'BC',
    'до нашей эры': 'BC',
    'до р.х.': 'BC',
    'до р. х.': 'BC',
    'до рождества Христова': 'BC',
    'н.э.': 1,
    'н. э.': 1,
    'от р.х.': 1,
    'от р. х.': 1,
    'нашей эры': 1,
    'от Рождества Христова': 1,
    'до': 'BC',
    #'от': 1,
    #'н': 'BC',
    #'нашей': 1,
}
# ПОЛОВИНЫ (А ВРЕМЕНИ ГОДА МБ?)
HALF_DICT = {
    '1': 'H1',
    '2': 'H2',
    'последний': 'H2',
    'заключительный': 'H2',
}

THIRD_DICT = {
    '1': 'T1',
    '2': 'T2',
    '3': 'T3',
    'последний': 'T3',
    'заключительный': 'T3',
}

QUARTER_DICT = {
    '1': 'Q1',
    '2': 'Q2',
    '3': 'Q3',
    '4': 'Q4',
    'последний': 'Q4',
    'заключительный': 'Q4',
}

PLACES = {
    'начало': 'START',
    'середина': 'MID',
    'конец': 'END',
}

SDICT = {
    'ые': 1,
    'е': 1,
    'ых': 1,
    'х': 1,
    'число': 1,   # МОЖНО ЛИ? "Это будет двадцать первого числа" НО это относительная дата
}

# Нормализированные названия дня недели
DAYWEEK_NAME = dictionary(DAYWEEK).interpretation(
    Date.dayweek.normalized().custom(DAYWEEK.__getitem__)
)
# Нормализированные названия месяцев
MONTH_NAME = dictionary(MONTHS).interpretation(
    Date.month.normalized().custom(MONTHS.__getitem__)
)
# Численный месяц
MONTH = and_(
    gte(1),
    lte(12)
).interpretation(
    Date.month.custom(int)
)
# День численный
DAY = and_(
    gte(1),
    lte(31)
).interpretation(
    Date.day.custom(int)
)
# Обозначение года
YEAR_WORD = or_(
    rule('г', eq('.').optional()),
    rule(normalized('год'))
)
# Год (1000-2100)
YEAR = and_(
    gte(1000),
    lte(2100)
).interpretation(
    Date.year.custom(int)
)
# Короткий год (90-ый) XX
YEAR_SHORT = and_(
    length_eq(2),
    gte(0),
    lte(99)
).interpretation(
    Date.year.custom(lambda _: 'XX' + str(int(_)))
)
# Неделя
WEEK = and_(
    gte(1),
    lte(53)
).interpretation(
    Date.week.custom(int)
)
# Декада месяца
DECADE = and_(
    gte(1),
    lte(3)
).interpretation(
    Date.decade.custom(int)
)
# Время года
SEASON = dictionary(SEASONS).interpretation(
    Date.season.normalized().custom(SEASONS.__getitem__)
)
# Век
CENTURY = and_(
    gte(1),
    lte(99)   # И ВСЁ?
).interpretation(
    Date.century.custom(int)
)
# Тысячелетие
MILLENNIUM = and_(
    gte(1),   # В ФОРМАТАХ НАЧИНАЕТСЯ С НУЛЯ???
    lte(9)   # И ВСЁ?
).interpretation(
    Date.millennium.custom(int)
)
# Эра
ERA = dictionary(ERAS).interpretation(
    Date.era.custom(ERAS.__getitem__)
)

# Половина
HALF = dictionary(HALF_DICT).interpretation(
    Date.half.normalized().custom(HALF_DICT.__getitem__)
)

# Треть
THIRD = dictionary(THIRD_DICT).interpretation(
    Date.third.normalized().custom(THIRD_DICT.__getitem__)
)

# Четверть
QUARTER = dictionary(QUARTER_DICT).interpretation(
    Date.quarter.normalized().custom(QUARTER_DICT.__getitem__)
)

# Начало/середина/конец
PLACE = dictionary(PLACES).interpretation(
    Date.place.normalized().custom(PLACES.__getitem__)
)

S = dictionary(SDICT).interpretation(
    Date.s.normalized().custom(SDICT.__getitem__)
)

ERAR = or_(
    rule(
        ERA,
        'н',
        '.',
        'э',
        '.'
    ),
    rule(
        ERA,
        normalized('нашей'),
        normalized('эры'),
    ),
    rule(
        ERA,
        'р',
        '.',
        'х',
        '.'
    ),
    rule(
        ERA,
        normalized('рождество'),
        normalized('Христова'),
    )
    # 'до нашей эры': 'BC',
    # 'до р.х.': 'BC',
    # 'до р. х.': 'BC',
    # 'до рождества Христова': 'BC',
    # 'н.э.': 1,
    # 'н. э.': 1,
    # 'от р.х.': 1,
    # 'от р. х.': 1,
    # 'нашей эры': 1,
    # 'от Рождества Христова': 1,
)
DATE = or_(
#######
#
#   ФОРМАТЫ ЗАПИСИ ДЕНЬ - МЕСЯЦ - ГОД
#
######
    # dd.mm.yyyy или dd.mm.yy / dd-mm-yyyy или dd-mm-yy / dd/mm/yyyy or dd/mm/yy
    rule(
        DAY,
        or_(normalized('.'),
            normalized('-'),
            normalized('/')),
        or_(
            MONTH,
            MONTH_NAME
        ),
        or_(normalized('.'),
            normalized('-'),
            normalized('/')),
        or_(
            YEAR,
            YEAR_SHORT
        ),
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), normalized('ом').optional()),
        YEAR_WORD.optional()
    ),
    # yyyy-mm-dd  Другие ВАРИАНТЫ?????
    rule(
        YEAR,
        YEAR_WORD.optional(),
        '-',
        or_(
            MONTH,
            MONTH_NAME
        ),
        '-',
        DAY
    ),

#######
#
#   ФОРМАТЫ ЗАПИСИ ГОДА
#
######


    # Год  НЕТУ 1930-е ибо это может быть что угодно, ЕСТ только со словом "годы"
    rule(
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Год короткий  ЗДЕСЬ НЕ ПОЛУЧИТЬСЯ с 30-е или получиться
    rule(
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR_SHORT,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        ERAR.optional(),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
    ),

#######
#
#   ФОРМАТЫ ЗАПИСИ СВЯЗАННЫЕ С МЕСЯЦОМ
#
######


    # День месяца
    rule(
        DAY,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        or_(normalized('день'),normalized('числах')).optional(),
        MONTH_NAME
    ),
    # Месяц года
    rule(
        PLACE.optional(),
        MONTH_NAME,
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD.optional(),
        PLACE.optional(),
        ERAR.optional()
    ),
    # День (месяца)
    rule(
        DAY,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        normalized('числах').optional(),
        MONTH_NAME,
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD.optional(),
        ERAR.optional()
    ),
    # Декада месяца НУЖНА ПОЛОВИНА?
    rule(
        DECADE,
        normalized('-').optional(),
        or_(normalized('ая').optional(), normalized('ей').optional(), normalized('ой').optional()),
        normalized('декада'),
        MONTH_NAME,
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional()),
        YEAR_WORD.optional(),
        ERAR.optional()
    ),


#######
#
#   ФОРМАТЫ ЗАПИСИ СВЯЗАННЫЕ С НЕДЕЛЕЙ
#
######


    # Неделя года (КАК????)
    rule(
        PLACE.optional(),
        WEEK,
        normalized('неделя'),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional()),
        YEAR_WORD.optional(),
        ERAR.optional()
    ),
    # Неделя года 2 (КАК????)
    # rule(
    #     WEEK,
    #     normalized('-').optional(),
    #     or_(normalized('ая').optional(), normalized('ой').optional()),
    #     normalized('неделя'),
    # ),
    # День недели (для теста) НУЖНО УЗНАТЬ КАК ПИСАТЬ
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        DAYWEEK_NAME,
    ),

#######
#
#   ФОРМАТЫ ЗАПИСИ ВЕК, ТЫСЯЧЕЛЕТИЕ
#
######


    # Век
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        CENTURY,
        normalized('-').optional(),
        or_(
            normalized('ого'),
            normalized('ый'),
        ).optional(),
        normalized('век'),
        ERAR.optional(),
    ),
    # ВЕК И ГОД
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        CENTURY,
        normalized('-').optional(),
        or_(
            normalized('ого'),
            normalized('ый'),
        ).optional(),
        normalized('век'),
        ERAR.optional(),
    ),
    # ВЕК И КОРОТКИЙ ГОД
    rule(
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR_SHORT,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        PLACE.optional(),
        CENTURY,
        normalized('-').optional(),
        or_(
            normalized('ого'),
            normalized('ый'),
        ).optional(),
        normalized('век'),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Тысячелетие
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        MILLENNIUM,
        normalized('тысячелетие'),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Тысячелетие 2
    rule(
        PLACE.optional(),
        MILLENNIUM,
        normalized('тысячелетие'),
        or_(
            normalized('в'),
            normalized('к'),
        ).optional(),
        PLACE.optional(),
        ERAR.optional(),
    ),


#######
#
#   ФОРМАТЫ ЗАПИСИ ЧАСТИ ЕДИНИЦЫ
#
######


# ПОЛОВИНЫ
    # ПОЛОВИНА ВЕКА
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        CENTURY,
        normalized('век'),
        ERAR.optional(),
    ),
    # ПОЛОВИНА Тысячелетие
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        MILLENNIUM,
        normalized('тысячелетие'),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Неделя года (КАК????)
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        PLACE.optional(),
        WEEK,
        normalized('неделя'),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional()),
        YEAR_WORD.optional(),
        ERAR.optional()
    ),
    # Неделя года 2 (КАК????)
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        WEEK,
        normalized('-').optional(),
        or_(normalized('ая').optional(), normalized('ой').optional()),
        normalized('неделя'),
    ),
    # Год  НЕТУ 1930-е ибо это может быть что угодно, ЕСТ только со словом "годы"
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Год короткий  ЗДЕСЬ НЕ ПОЛУЧИТЬСЯ с 30-е или получиться
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR_SHORT,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        ERAR.optional(),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
    ),
    # Месяц года
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        HALF,
        or_(
            normalized('половина'),
            normalized('полугодие')
        ),
        PLACE.optional(),
        MONTH_NAME,
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD.optional(),
        PLACE.optional(),
        ERAR.optional()
    ),

# ТРЕТИ
    # ТРЕТЬ ВЕКА
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        THIRD,
        normalized('треть'),
        CENTURY,
        normalized('век'),
        ERAR.optional(),
    ),
    # ТРЕТЬ Тысячелетие
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        THIRD,
        normalized('треть'),
        MILLENNIUM,
        normalized('тысячелетие'),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Неделя года (КАК????)
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        THIRD,
        normalized('треть'),
        PLACE.optional(),
        WEEK,
        normalized('неделя'),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional()),
        YEAR_WORD.optional(),
        ERAR.optional()
    ),
    # Неделя года 2 (КАК????)
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        THIRD,
        normalized('треть'),
        WEEK,
        normalized('-').optional(),
        or_(normalized('ая').optional(), normalized('ой').optional()),
        normalized('неделя'),
    ),
    # Год  НЕТУ 1930-е ибо это может быть что угодно, ЕСТ только со словом "годы"
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        THIRD,
        normalized('треть'),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Год короткий  ЗДЕСЬ НЕ ПОЛУЧИТЬСЯ с 30-е или получиться
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        THIRD,
        normalized('треть'),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR_SHORT,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        ERAR.optional(),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
    ),
    # Месяц года
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        THIRD,
        normalized('треть'),
        PLACE.optional(),
        MONTH_NAME,
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD.optional(),
        PLACE.optional(),
        ERAR.optional()
    ),

# ЧЕТВЕРТИ
    # ЧЕТВЕРТЬ ВЕКА
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        CENTURY,
        normalized('век'),
        ERAR.optional(),
    ),
    # ПОЛОВИНА Тысячелетие
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        MILLENNIUM,
        normalized('тысячелетие'),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Неделя года (КАК????)
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        PLACE.optional(),
        WEEK,
        normalized('неделя'),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional()),
        YEAR_WORD.optional(),
        ERAR.optional()
    ),
    # Неделя года 2 (КАК????)
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        WEEK,
        normalized('-').optional(),
        or_(normalized('ая').optional(), normalized('ой').optional()),
        normalized('неделя'),
    ),
    # Год  НЕТУ 1930-е ибо это может быть что угодно, ЕСТ только со словом "годы"
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        ERAR.optional(),
    ),
    # Год короткий  ЗДЕСЬ НЕ ПОЛУЧИТЬСЯ с 30-е или получиться
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
        YEAR_SHORT,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD,
        ERAR.optional(),
        PLACE.optional(),
        SEASON.optional(),
        PLACE.optional(),
    ),
    # Месяц года
    rule(
        # or_(
        #     normalized('в'),
        #     normalized('к'),
        # ).optional(),
        PLACE.optional(),
        QUARTER,
        or_(
            normalized('четверть'),
            normalized('квартал')
        ),
        PLACE.optional(),
        MONTH_NAME,
        PLACE.optional(),
        YEAR,
        normalized('-').optional(),
        or_(normalized('ый').optional(), normalized('ого').optional(), S.optional()),
        YEAR_WORD.optional(),
        PLACE.optional(),
        ERAR.optional()
    ),


#######
#
#   ФОРМАТЫ ЗАПИСИ ЭРЫ
#
######





).interpretation(
    Date
)
