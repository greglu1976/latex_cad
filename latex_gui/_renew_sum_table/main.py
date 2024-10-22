# функция ищет в текущей папке файл general.tex - основной файл проекта latex
# затем собирает пути, где расположены описания функций и приложения
# пути к к функциям находятся в списке function_paths

import os

from logger import logger
from .get_xlsx_paths import get_xlsx_paths
from .collect_df import collect_df
from .parsers import parse_func_paths, parse_app_path
from .assembly_tex import assembly_tex

def start_renew_sum_table(path):

    logger.info("Запуск скрипта обновления таблицы всех сигналов устройства...")

    file_name = "general.tex"

    print(path +'/'+ file_name)
    # Проверяем наличие файла в текущем каталоге
    if os.path.isfile(path +'/'+ file_name):
        with open(path +'/'+ file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    else:
        logger.error(f"Файл '{file_name}' не найден в текущем каталоге")
        return ('error',f"Файл '{file_name}' не найден в текущем каталоге")

    function_paths = parse_func_paths(lines) # ищем пути к функциям

    app_path = parse_app_path(lines) # ищем путь к приложению А
    print('app_path ', app_path)

    # Выводим содержимое списка function_paths
    logger.info('В файле general.tex руководства по эксплуатации обнаружены следующие пути к функциям')
    for path in function_paths:
        logger.info(path)

    # ЗДЕСЬ НАДО СОБРАТЬ СПИСОК ОБЩИХ СИГНАЛОВ УСТРОЙСТВА!!!
    # В ВИДЕ TEX  
    general_signals = [] # здесь должно быть извлечение общих сигналов, сейчас просто пустой список

    #############################      
    xlsx_paths = get_xlsx_paths(function_paths) # собираем из тех файлов перечень необходимых функций в виде списка туплов [(path1, [list1]), (path2, [list2])]
    funcs_tex = collect_df(xlsx_paths) # принимаем tex файл куском таблицы по всем функциям

    # ++++++++++++++++TEST+++++++++++++++++++++++
    #with open('latex.txt', 'w') as file:
    #    for line in funcs_tex:
    #        file.write(line + "\n")
    # ++++++++++++++++TEST+++++++++++++++++++++++  
                
    if not general_signals and not funcs_tex: # проверяем, что нечем обновлять
        return ('error', 'Сформирован пустой список сигналов')

    # теперь у нас есть путь к файлу приложения, есть два списка сигналов - общий и по функциям
    # осталось пропарсить файл приложения, найти там тэг ===t2 и вставить после него сначала общие сигналы
    # потом сигналы по функциям, не забыть про заголовки
    # app_path
    # general_signals
    # funcs_tex
    final_tex = []
    if not general_signals:
        logger.warning('Не найдено ни одной строчки по статусам общих функций для суммарной таблицы.')
    else:
        final_tex.append('\multicolumn{9}{|c|}{Системные сигналы} \\\\'+'\n')
        final_tex.append('\hline'+'\n')
        final_tex += general_signals
    if not funcs_tex:
        logger.warning('Не найдено ни одной строчки по статусам функций защиты и автоматики для суммарной таблицы.')
    else:
        #final_tex.append('\multicolumn{9}{|c|}{Сигналы функциональной логики} \\\\'+'\n')
        #final_tex.append('\hline'+'\n')
        final_tex += funcs_tex        

    app1_file = assembly_tex(final_tex, app_path)
    if app1_file[0] == 'error': # обрабатываем ошибки
        return app1_file


    logger.info("Штатный останов скрипта обновления таблицы всех сигналов устройства...")
    return ('ok', '')