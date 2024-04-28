# функция ищет в текущей папке файл general.tex - основной файл проекта latex
# затем собирает пути, где расположены описания функций и приложения
# пути к к функциям находятся в списке function_paths

import os
import re

import logging

from dir_renewer import renew_dir, xlsx_finder

# Configure logging
logging.basicConfig(filename='renew.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


file_name = "general.tex"
function_paths = []

# Проверяем наличие файла в текущем каталоге
if os.path.isfile(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        inside_func_tag = False
        current_func = []

# ИЩЕМ ПУТИ К ФУНКЦИЯМ
        for line in file:
            if inside_func_tag:
                if line.strip() == "%===f":
                    inside_func_tag = False
                else:
                    current_func.append(line.strip())
                    # Проверяем строку на наличие пути и добавляем его в список если найден и строка не начинается с %
                    if not line.strip().startswith('%'):
                        match = re.search(r'\\input{(.*?)/_latex', line)
                        if match:
                            path = match.group(1)
                            function_paths.append(path)
            else:
                if line.strip() == "%===f":
                    inside_func_tag = True


    # Выводим содержимое списка function_paths
    logging.info("Пуск скрипта")
    for path in function_paths:
        logging.info(path)
        #renew_dir(path)
        dfs = xlsx_finder(path)
        if dfs:
            renew_dir(path, dfs)


else:
    logging.error(f"Файл '{file_name}' не найден в текущем каталоге")