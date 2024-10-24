# функция ищет в текущей папке файл general.tex - основной файл проекта latex
# затем собирает пути, где расположены описания функций и приложения
# пути к к функциям находятся в списке function_paths

import os
import re

from logger import logger
from reporter import handler_paths

logger.info("Запуск скрипта...")

file_name = "general.tex"

with open(file_name, 'r' , encoding='utf-8') as file:
    for line in file:
        if 'manualpath' in line:
            parts = line.split('{')
            desired_content = parts[-1].strip()
            desired_content = desired_content.rstrip('}')
            #print("Содержимое вторых фигурных скобок в строке с подстрокой manualpath:", desired_content)

path_to_re = desired_content+file_name

function_paths = []

# Проверяем наличие файла в текущем каталоге
if os.path.isfile(path_to_re):
    with open(path_to_re, 'r', encoding='utf-8') as file:
        inside_func_tag = False
        current_func = []

        fbpath=''
        isFoundFbPath = False

# ИЩЕМ ПУТИ К ФУНКЦИЯМ
        for line in file:
            
            if 'fbpath' in line and not isFoundFbPath:
                isFoundFbPath = True
                fbparts = line.split('{')
                fb_content = fbparts[-1].strip()
                fbpath = fb_content.rstrip('}')

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
                            if '\\fbpath/' in path:
                                path = path.replace('\\fbpath/', '')
                            function_paths.append(fbpath+path)
            else:
                if line.strip() == "%===f":
                    inside_func_tag = True


    # Выводим содержимое списка function_paths
    logger.info('В файле general.tex руководства по эксплуатации обнаружены следующие пути к функциям')
    for path in function_paths:
        logger.info(path)

    handler_paths(function_paths)

else:
    logger.error(f"Файл '{file_name}' не найден в текущем каталоге")

logger.info("Штатный останов скрипта...")