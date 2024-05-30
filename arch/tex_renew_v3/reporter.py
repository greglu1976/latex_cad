import os
import re

from logger import logger

def handler_paths(paths):
    work_dirs = []
    for path in paths:
        if not os.path.isdir(path + '/_xlsx'):
            logger.warning(f'Функция по пути {path} не будет обработана, т.к. нет директории _xlsx')
            continue
        if not os.path.isdir(path + '/_latex'):
            logger.warning(f'Функция по пути {path} не будет обработана, т.к. нет директории _latex')
            continue
        work_dirs.append(path)
    return work_dirs

def find_paths(filename):
    function_paths = []
    # Проверяем наличие файла в текущем каталоге
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            inside_func_tag = False
            current_func = []
            fbpath=''
            isFoundFbPath = False
    # ИЩЕМ ПУТИ К ФУНКЦИЯМ
            for line in file:
                if 'fbpath' in line and not '%' in line and not isFoundFbPath:
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

    else:
        logger.error(f"Файл '{filename}' не найден в текущем каталоге")
    return function_paths