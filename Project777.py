#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from extractors import (DatesExtractor, NumeralExtractor)
from numeralClass import (
    NUMERALS, DOZEN, HUNDRED,
    THOUSAND, MILLION, BILLION, TRILLION
)
from yargy import (
    rule,
    and_, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)

import re
import os

def format(temporalExp):
    temporalVar = None

    # Перевод тысячелетий
    if temporalExp.millennium != None:
        if (temporalExp.half == None) and (temporalExp.third == None) and (temporalExp.quarter == None) and (temporalExp.place == None):
            temporalVar = '<date value=\"' + str(temporalExp.millennium)
        elif temporalExp.half != None: temporalVar = '<date value=\"' + str(temporalExp.millennium) + '-' + str(temporalExp.half)
        elif temporalExp.third != None: temporalVar = '<date value=\"' + str(temporalExp.millennium) + '-' + str(temporalExp.third)
        elif temporalExp.quarter != None: temporalVar = '<date value=\"' + str(temporalExp.millennium) + '-' + str(temporalExp.quarter)
        elif temporalExp.place != None: temporalVar = '<date value=\"' + str(temporalExp.millennium) + '-' + str(temporalExp.place)

    # Перевод веков
    if temporalExp.century != None:
        if (temporalExp.half == None) and (temporalExp.third == None) and (temporalExp.quarter == None) and (temporalExp.place == None):
            temporalVar = '<date value=\"' + str(temporalExp.century - 1)
        elif temporalExp.half != None: temporalVar = '<date value=\"' + str(temporalExp.century - 1) + '-' + str(temporalExp.half)
        elif temporalExp.third != None: temporalVar = '<date value=\"' + str(temporalExp.century - 1) + '-' + str(temporalExp.third)
        elif temporalExp.quarter != None: temporalVar = '<date value=\"' + str(temporalExp.century - 1) + '-' + str(temporalExp.quarter)
        elif temporalExp.place != None: temporalVar = '<date value=\"' + str(temporalExp.century - 1) + '-' + str(temporalExp.place)

    # Перевод годов
    if temporalVar == None:
        if temporalExp.year == None: temporalVar = '<date value=\"XXXX'
        elif (temporalExp.day == None) and (temporalExp.s != None):
            if str(temporalExp.year).isdigit() == True: temporalVar = '<date value=\"' + str(int(temporalExp.year) // 10)
            else: temporalVar = '<date value=\"XX' + str(temporalExp.year)[2:3]
        else: temporalVar = '<date value=\"' + str(temporalExp.year)

        #Заход на месяцы
        if (temporalExp.month != None) or (temporalExp.day != None) or (temporalExp.decade != None):
            if temporalExp.month == None: temporalVar = temporalVar  + '-' + 'XX'
            elif temporalExp.month < 10: temporalVar = temporalVar + '-0' +  str(int(temporalExp.month))
            else: temporalVar = temporalVar + '-' +  str(int(temporalExp.month))
            if (temporalExp.day != None) and (temporalExp.s == None):
                if int(temporalExp.day) < 10: temporalVar = temporalVar + '-' + '0' + str(int(temporalExp.day))
                else: temporalVar = temporalVar + '-' + str(int(temporalExp.day))
            if temporalExp.decade != None: temporalVar = temporalVar + '-' + 'D' + str(int(temporalExp.decade))
            if (temporalExp.day != None) and (temporalExp.s != None): temporalVar = temporalVar + '-' + str(int(temporalExp.day) // 10)

        # Заход на недели
        if (temporalExp.week != None) or (temporalExp.dayweek != None):
            if temporalExp.month == None: temporalVar = temporalVar + '-' + 'WXX'
            else: temporalVar = temporalVar + '-W' + str(int(temporalExp.month))
            if temporalExp.dayweek != None: temporalVar = temporalVar + '-' + str(int(temporalExp.dayweek))

        # Заход на время года
        if temporalExp.season != None: temporalVar = temporalVar + '-' + str(temporalExp.season)

        # Заход на часть или фазу календарной единицы
        if temporalExp.half != None: temporalVar = temporalVar + '-' + str(temporalExp.half)
        if temporalExp.third != None: temporalVar = temporalVar + '-' + str(temporalExp.third)
        if temporalExp.quarter != None: temporalVar = temporalVar + '-' + str(temporalExp.quarter)
        if temporalExp.place != None: temporalVar = temporalVar + '-' + str(temporalExp.place)

    return temporalVar



def tagging(input, output):
    numeralBack = []

    file = open(input, 'r', encoding="utf-8")
    text = ""

    for line in file:
        text += line

    endTag = '</date>'
    a = ""
    b = ""
    textT = text
    # Замена числительных
    extractor = NumeralExtractor(a)
    matches = extractor(text)
    changes = 0
    excess = 0
    for index, match in enumerate(matches):
        check = 0
        tempM = 0
        tempNT = 1
        tempT = 0
        tempH = 0
        tempD = 0
        tempNUM = 0
        subStrOld = textT[match.start:match.stop]
        if match.fact.million != None:
            tempM = int(str(match.fact.million))
            check = 1
        if match.fact.nthousand != None:
            tempNT = int(str(match.fact.nthousand))
            check = 1
        if match.fact.thousand != None:
            tempT = int(str(match.fact.thousand))
            check = 1
        if match.fact.hundred != None:
            tempH = int(str(match.fact.hundred))
            check = 1
        if match.fact.dozen != None:
            tempD = int(str(match.fact.dozen))
            check = 1
        if match.fact.num != None:
            tempNUM = int(str(match.fact.num))
            check = 1
        if check == 1:
            subStrNew = str(tempM + tempNT * tempT + tempH + tempD + tempNUM)
        elif check == 0:
            subStrNew = str(match.fact.plural)
        lenStrOld = len(subStrOld)
        ch = 0
        sh = ""
        if text.find(subStrOld) >= 0:
            i = text.find(subStrOld) - changes
            serviceNumeral = "$" * (lenStrOld - len(subStrNew) - 1)
            if serviceNumeral != "" and (lenStrOld - len(subStrNew)) >= 0:
                serviceNumeral = serviceNumeral + " "
            elif (lenStrOld - len(subStrNew)) < 0:
                textT = textT[:i] + "@" + textT[i:]
                ch = 1
            elif (lenStrOld - len(subStrNew)) == 1:
                sh = " "
            text = text[:i + excess] + serviceNumeral + subStrNew + sh + text[i + lenStrOld + excess:]
            if ch == 1:
                excess = excess + 1

    print(text)
    extractor = DatesExtractor(a)
    matches = extractor(text)
    textT2 = text
    serviceVar = 0
    # Технический момент (нужно переделать)
    # text = text.replace("В $", "$ В")
    # while text.find("В$") != -1:
    #     text = text.replace(" В$", "$ В")
    #
    # text = text.replace("$В ", "$ В")

    print(text)
    # Тэгирование
    pastEnd = 0
    for index, match in enumerate(matches):
        print(index, match.fact)
        if (match.fact.century != None) and (match.fact.year != None):
            match.fact.year = str(int(match.fact.century) - 1) + str(match.fact.year)[2:4]
            match.fact.century = None
        tag = format(match.fact) + '\">'

        lenghtTag = len(tag)
        if text[match.start - 2] == "$":
            rar = text.find("$", pastEnd, match.start)
            textT = textT[:rar + serviceVar] + tag + textT[rar + serviceVar:match.stop + serviceVar] + endTag + textT[
                                                                                                                match.stop + serviceVar:]
        else:
            textT = textT[:match.start + serviceVar] + tag + textT[
                                                             match.start + serviceVar:match.stop + serviceVar] + endTag + textT[
                                                                                                                          match.stop + serviceVar:]
        serviceVar = serviceVar + lenghtTag + len(endTag)
        pastEnd = match.stop

    textT = textT.replace("@", "")
    print(textT)

    outFile = open(output, 'w', encoding="utf-8")
    outFile.write(textT)
    file.close()
    outFile.close()


os.chdir("Input")
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        outputN = "../Output/" + os.path.join(name)
        tagging(os.path.join(name), outputN)
        print(os.path.join(name))