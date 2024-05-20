# функция ищет в текущей папке файл general.tex - основной файл проекта latex
# затем собирает пути, где расположены описания функций и приложения
# пути к к функциям находятся в списке function_paths
# 27/04/24 change reporter - add check '%' in fbpath, line 29

import os
import re
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from logger import logger
from .reporter import handler_paths, find_paths
from .process_path import process_path

def start_renew_tables(path):

    logger.info("Запуск скрипта обновления таблиц в РЭ")

    file_name = path + "/general.tex"

    function_paths = find_paths(file_name)
    logger.info('В файле general.tex руководства по эксплуатации обнаружены следующие пути к функциям')
    for path in function_paths:
        logger.info(path)

    work_func_paths = handler_paths(function_paths)
    for path in work_func_paths:
        logger.info(path)
        process_path(path)

    logger.info("Штатный останов скрипта обновления таблиц в РЭ")
    return 'ok'