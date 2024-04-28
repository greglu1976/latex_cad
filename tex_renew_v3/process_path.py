import os

from logger import logger
from df_process import df_finder

def process_path(path):
    work_path = path + '/_latex/'
    print(work_path)
    # Получить список всех файлов в указанной директории
    files = os.listdir(work_path)
    # Отфильтровать только файлы с расширением .tex
    tex_files = [file for file in files if file.endswith(".tex")]

    if not tex_files:
        logger.warning(f'По пути {work_path} отсутствуют файлы описания функции .tex')
        return

    full_path = work_path + tex_files[0]
    is_inside = False
    tex_final = [] # сюда собирать будем выходной файл
    with open(full_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '%===t1' in line and not is_inside:
                tex_final.append(line) # Write the opening %===t1 tag
                
                if '>' in line: # проверяем нужен ли заголовок
                    custom_header = line.split('>')[1]
                    print(custom_header)
                    #tex_final=add_str_custom_header(custom_header, tex_final)
                    line = line.split('>')[0]
                    print(line)

                is_inside = True
                ln = line.split('*')[1].strip()
                str_work = df_finder(ln, path)

                if not str_work:
                    for add_line in str_work:
                        tex_final.append(add_line)

            elif is_inside and '%===t1' in line:
                tex_final.append(line)  # Write the closing %===t1 tag
                is_inside = False
            elif is_inside:
                continue
            else:
                tex_final.append(line)
