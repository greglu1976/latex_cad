import os
import shutil

from logger import logger
from .df_process import df_finder

def process_path(path):
    work_path = path + '/_latex/'
    #print('work_path>>> ',work_path)
    # Получить список всех файлов в указанной директории
    files = os.listdir(work_path)
    # Отфильтровать только файлы с расширением .tex
    tex_files = [file for file in files if file.endswith(".tex")]

    if not tex_files:
        logger.warning(f'По пути {work_path} отсутствуют файлы описания функции .tex')
        return

    full_path = work_path + tex_files[0]
    is_inside = False
    is_passing = False
    tex_final = [] # сюда собирать будем выходной файл
    with open(full_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '%===t1' in line and not is_inside:
                is_inside = True
                tex_final.append(line) # Write the opening %===t1 tag

                custom_header = ''
                ln = ''
                parsed_line = line.split('>', 1)
                if len(parsed_line) == 2:
                    custom_header = parsed_line[1]
                    line = parsed_line[0]
                ln = line.split('*')[1].strip()

                str_work, isInfoStr = df_finder(ln, path)
                #print(isInfoStr)

                if str_work[0] != 'noxlsx':
                    is_passing = True
                    if custom_header != '': # проверяем нужен ли заголовок
                        tex_final.append("\\multicolumn{5}{|c|}{" + custom_header.strip('\n')  + "} \\\\"+"\n")
                        tex_final.append("\\hline\n")
                    if str_work:
                        for add_line in str_work:
                            tex_final.append(add_line + '\n')
                        if isInfoStr:
                            tex_final.append("\\multicolumn{5}{|l|}{" + "* - Для устройств с номинальным током 1 А (5 А)"  + "} \\\\"+"\n")
                else:
                    is_passing = False
                continue

            elif is_inside and '%===t1' in line:
                tex_final.append(line)  # Write the closing %===t1 tag
                is_inside = False
                continue
            elif is_inside and not is_passing:
                tex_final.append(line)
                continue
            elif is_inside and is_passing:
                continue            
            else:
                tex_final.append(line)
    
    out_name = tex_files[0].split('.')[0].strip()+'.bac'
    shutil.copy(full_path, work_path+out_name)

    with open(full_path, 'w', encoding='utf-8') as file:
        for line in tex_final:
            file.write(line)