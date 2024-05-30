import os

from logger import logger
from .tex_parser import parse_to_tex

def handler_paths(paths, path_to_write):

    sum_tex = []
    for path in paths:
        
        if not os.path.isdir(path + '/_xlsx'):
            
            logger.warning(f'Функция по пути {path} не будет обработана, т.к. нет директории _xlsx')
        else:
            logger.info(f'Обрабатываем Функции по пути {path}')
            path = path + '/_xlsx'
            # Get the list of folders in the specified path
            folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            # берем первую если там несколько, считаем что она рабочая
            if not folders:
                logger.warning(f'Функция по пути {path} не будет обработана, т.к. нет директорий ФБ в _xlsx')
                continue

            work_folder = folders[0]
            #print(work_folder)
            path = path +'/'+ work_folder +'/'
            logger.info(f'Ищем описание функций в папке {path}')
            #print(path)
            # Get the list of all files in the specified path
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

            # Extract the names and extensions of the files
            file_info = [(os.path.splitext(f)[0], os.path.splitext(f)[1]) for f in files]

            # Print the names and extensions of the files
            #print("Names and extensions of all files in the specified path:")
            xslx_list = []
            for name, ext in file_info:
                if ext != '.xlsx': # смотрим только эксел файлы
                    continue
                if name == 'control' or name.startswith('~'): # control и временные файлы не нужны
                    continue
                #print(f"Name: {name}, Extension: {ext}")
                #print(path+name+ext)
                #tex_text = parse_to_tex(path+name+ext, name)
                xslx_list.append((path, name, ext))
            if xslx_list:
                sum_tex += parse_to_tex(xslx_list)
    with open(path_to_write+'/report.tex', 'w', encoding='utf-8') as f:
        for line in sum_tex:
            f.write(line + '\n')

