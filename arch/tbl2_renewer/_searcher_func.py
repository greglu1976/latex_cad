# функция ищет в текущей папке файл general.tex - основной файл проекта latex
# затем собирает пути, где расположены описания функций и приложения
# пути к к функциям находятся в списке function_paths

import os
import re

import logging

def find_funcs(general_tex_name):
    with open(general_tex_name, 'r', encoding='utf-8') as file:
        inside_func_tag = False
        current_func = []
        function_paths = []
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
                            logging.info(f"Найден путь к функции: {path}")
            else:
                if line.strip() == "%===f":
                    inside_func_tag = True

    return function_paths
