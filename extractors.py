
from itertools import zip_longest

from yargy import Parser as YargyParser
from yargy.morph import MorphAnalyzer
from yargy.tokenizer import MorphTokenizer

from record import Record


#####
#
#  OBJS
#
#####


class Obj(Record):
    # default none values
    def __init__(self, *args, **kwargs):
        for key, value in zip_longest(self.__attributes__, args):
            self.__dict__[key] = value
        self.__dict__.update(kwargs)

    # but skip undef values in repr
    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(
            '{key}={value!r}'.format(
                key=_,
                value=getattr(self, _)
            )
            for _ in self.__attributes__
            if getattr(self, _)
        )
        return '{name}({args})'.format(
            name=name,
            args=args
        )

    def _repr_pretty_(self, printer, cycle):
        name = self.__class__.__name__
        if cycle:
            printer.text('{name}(...)'.format(name=name))
        else:
            printer.text('{name}('.format(name=name))

            pairs = []
            for key in self.__attributes__:
                value = getattr(self, key)
                if value:
                    pairs.append([key, value])

            size = len(pairs)
            if size:
                with printer.indent(4):
                    printer.break_()
                    for index, (key, value) in enumerate(pairs):
                        printer.text(key + '=')
                        printer.pretty(value)
                        if index < size - 1:
                            printer.text(',')
                            printer.break_()
                printer.break_()
            printer.text(')')

class Date(Obj):
    __attributes__ = ['era', 'millennium', 'century', 'year', 'month', 'day', 'week', 'dayweek', 'decade', 'season', 'half', 'third', 'quarter', 'place', 's']

class Numeral(Obj):
    __attributes__ = ['trillion', 'billion', 'million', 'nthousand', 'thousand', 'hundred', 'dozen', 'num', 'plural']


#######
#
#   EXTRACTOR
#
######


class Parser(YargyParser):
    def __init__(self, rule, morph):
        # wraps pymorphy subclass
        # add methods check_gram, normalized
        # uses parse method that is cached
        morph = MorphAnalyzer(morph)

        tokenizer = MorphTokenizer(morph=morph)
        YargyParser.__init__(self, rule, tokenizer=tokenizer)


class Match(Record):
    __attributes__ = ['start', 'stop', 'fact']


def adapt_match(match):
    start, stop = match.span
    fact = match.fact.obj
    return Match(start, stop, fact)


class Extractor:
    def __init__(self, rule, morph):
        self.parser = Parser(rule, morph)

    def __call__(self, text):
        for match in self.parser.findall(text):
            yield adapt_match(match)

    def find(self, text):
        match = self.parser.find(text)
        if match:
            return adapt_match(match)



class DatesExtractor(Extractor):
    def __init__(self, morph):
        from date import DATE
        Extractor.__init__(self, DATE, morph)
        

class NumeralExtractor(Extractor):
    def __init__(self, morph):
        from numeral import NUMERAL
        Extractor.__init__(self, NUMERAL, morph)


