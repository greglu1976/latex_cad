
dict_default = {
    'Независимая': 'Не\-за\-ви\-симая',
    'Ненаправленная':  'Не\-на\-прав\-лен\-ная',
    'Направленность':  'На\-прав\-ленность',
    'Характеристика':  'Харак\-терис\-тика',
}

dict_func = {
    'ТЗ Т': '(технологические защиты трансформатора)',
    'ТЗНП':  '(токовая защита нулевой последовательности)',
    'ЛО ГЗоткл':  '(логика отключения при срабатывании отключающего контакта газового реле)',
    'ЛО ГЗсигн':  '(логика отключения при срабатывании сигнального контакта газового реле)',
}

long_table_header_desc = '\\begin{longtable}[l]{|>{\centering\\arraybackslash}m{0.3cm}|>{\centering\\arraybackslash}m{4cm}|>{\centering\\arraybackslash}m{1.7cm}|>{\centering\\arraybackslash}m{3cm}|>{\centering\\arraybackslash}m{1cm}|>{\centering\\arraybackslash}m{1.5cm}|>{\centering\\arraybackslash}m{1.6cm}|>{\centering\\arraybackslash}m{1.5cm}|}'

long_table_header = [
'\hline',
'\\rowcolor{gray!30}',
'№ & Параметр (Параметр на ИЧМ) & Обозначение на схеме & Значение/ Диапазон & Ед. изм. & Шаг & По умолчанию & Значение ' + r'\\',
'\hline',
'\endfirsthead',
'\caption{\emph{Продолжение\hfill\\vspace{-0.5\\baselineskip}}}' + r'\\',
'\hline',
'\\rowcolor{gray!30}',
'№ & Параметр (Параметр на ИЧМ) & Обозначение на схеме & Значение/ Диапазон & Ед. изм. & Шаг & По умолчанию & Значение ' + r'\\',
'\hline',
'\endhead',                       
'\hline',
'\endfoot',                       
'\hline',
'\endlastfoot'
]

