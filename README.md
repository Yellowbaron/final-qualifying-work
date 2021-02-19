<img src="https://img.shields.io/badge/version-0.9.1-yellow">

# final-qualifying-work
Automatic annotation of temporal information in Russian-language texts

## Technology
Парсер на основе правил. Написан на части проекта Natasha Yargy-парсере
<p>В каталоге /build/ архив с исполняемым файлом. В папку "input" загружаются целевые текстовые файлы, после запуска exe'шника они аннотируются и появляются в папке "outbut". Таковы были требования к ПО</p>
<a href="https://github.com/Yellowbaron/final-qualifying-work/blob/main/Graduation_work_P-41_Galimyanov_AF%20(1).pptx">Презентация к ВКР Graduation_work_P-41_Galimyanov_AF (1).pptx</a>

### Разметка основана на стандарте аннотирования TimeML

| Тип календарной единицы | Обозначение | Пример  | Запись значения примера| Комментарии |
| ------------- |:-------------:| -----:|:-------------:| -----:|
|    `Основные даты`               |
|     Год                                               |     0001, 0012, 0912,   2020…    |     1995 год            |     1995          |     Идентификатор года записывается   в четырехзначном формате.      |
|     Год до нашей эры                                  |                                  |     563 год до н.э      |     BC0563        |     Четырехзначный   формат записи идентификатора года            |
|     Месяц                                             |     01, 02, ..., 12.             |     январь 2001 года    |     2001-01       |     Идентификатор месяца   записывается в двузначном формате.        |
|     День (месяца)                                     |     01, 02, ..., 31.             |     3 января 2001       |     2001-01-03    |     Идентификатор числа месяца записывается в двузначном формате.    |
|     Неделя (года)                                     |     W01, W02, ..., W52 (53?).                         |     на [этой неделе]                   |     2001-W05      |     Год и номер недели   вычисляется по числу месяца в соответствии со стандартом ISO 86015                                                                                                                                                                                                            |
|     День недели                                       |     1, 2, 3, 4, 5, 6, 7.                              |     во [вторник]                       |     2001-W05-2    |     Идентификатор дня   недели записывается в однозначном формате, без нуля в начале: 1, 2, 3, 4, 5,   6, 7.                                                                                                                                                                                           |
|     Век                                               |     01, 02, ..., 20, ...   , 99                       |     XXII век                           |     21            |     Идентификатор века   записывается в двузначном формате. В соответствии с TimeML, ориентируемся не   на номер самого века, а на первые цифры входящих в него лет. (Хотя нулевые   годы входят в предыдущий век: строго говоря, 1900 год относится к 19 веку.)                                       |
|     Тысячелетие                                       |     0, 1, 2, 3, ..., 9                                |     3 тысячелетие                      |     2             |     Идентификаторы   тысячелетия: 0, 1, 2, 3... (ориентируемся на первые цифры входящих в него   лет). Число «9» соответствует десятому тысячелетию. Тысячелетия с номером   больше 10 в таком формате записать невозможно (т.е. двузначное число в этой   позиции интерпретируется как номер века)    |
|     Век до нашей эры                                  |                                                       |     5 век до н.э.                      |     BC5           |     NB четырехзначный   формат записи идентификатора года                                                                                                                                                                                                                                              |
|     Декада месяца года                                |     D1, D2, D3.                                       |     первая декада декабря   2000 г.    |     2000-12-D1    |     Декады начинаются с   1, 11 и 21 числа. Третья декада длится до конца месяца.                                                                                                                                                                                                                      |
|     Числа месяца,   оканчивающиеся на ноль            |     1, 2                                              |     двадцатые числа   месяца           |     2001-01-2     |     Выражения «десятые   (двадцатые) числа месяца». Естественно предполагать, что значение такого   выражения включает и само 10-е (20-е) число. (Такая запись возможна,   поскольку обычный формат записи числа месяца двузначный.)                                                                   |
|     Время года                                        |     весна — SP, лето —   SU, осень — FA, зима — WI    |     весной                             |     2001-SP       |     Календарное время   года (по три месяца).                                                                                                                                                                                                                                                          |
|     Зима                                              |                                                       |     зимой прошлого года                |     2000-WI       |     В качестве года для   датысезона «зима» берется год начала зимы (т.е. год, на который приходится   декабрь этой зимы).                                                                                                                                                                             |
|    `Часть календарной единицы (условно точная)`       |
|     Половина (первая, вторая)                         |     H1, H2            |                                                 |                         |     Записывается через   дефис после идентификатора интервала, чьей частью является.                                          |
|     Полугодие                                         |                       |     вторая половина года,   второе полугодие    |     2001-H2             |                                                                                                                               |
|     Половина века                                     |                       |     вторая половина XX   века                   |     19-H2               |                                                                                                                               |
|     Половина месяца                                   |                       |     первая половина   апреля                    |     2001-04-H1          |                                                                                                                               |
|     Половина недели                                   |                       |     вторая половина   недели                    |     2001-W05- H2        |                                                                                                                               |
|     Треть                                             |     T1, T2, T3        |     вторая треть XVIII   века                   |     17-T2               |                                                                                                                               |
|     Четверть (первая,   вторая, третья, четвёртая)    |     Q1, Q2, Q3, Q4    |                                                 |                         |                                                                                                                               |
|     Квартал                                           |                       |     II квартал 2005 года                        |     2005-Q2             |                                                                                                                               |
|    `Нечёткая фаза календарной единицы`                |
|     Начало/середина/конец   календарной единицы       |     START / MID / END |     середина недели                             |     2001-W05- MID       |     Записывается через   дефис после идентификатора интервала, чьей фазой является.                                           |
