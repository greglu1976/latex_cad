import os

import shutil

from logger import logger
from df_process import df_finder

def process_path(path):
    work_path = path + '/_latex/'
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
                    tex_final.append("\\multicolumn{5}{|c|}{" + custom_header.strip('\n')  + "} \\\\"+"\n")
                    tex_final.append("\\hline\n")
                    line = line.split('>')[0]

                is_inside = True
                ln = line.split('*')[1].strip()
                str_work = df_finder(ln, path)
                if str_work:
                    for add_line in str_work:
                        tex_final.append(add_line + '\n')

            elif is_inside and '%===t1' in line:
                tex_final.append(line)  # Write the closing %===t1 tag
                is_inside = False
            elif is_inside:
                continue
            else:
                tex_final.append(line)
    
    out_name = tex_files[0].split('.')[0].strip()+'.bac'
    shutil.copy(full_path, work_path+out_name)

    with open(full_path, 'w', encoding='utf-8') as file:
        for line in tex_final:
            file.write(line)
