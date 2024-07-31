import os
import pandas as pd
from logger import logger
from .row_parser import parse_row

def df_finder(ln, path):
    path = path + '/_xlsx/'
    folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    #print(ln, '===++>>>', folders)
    
    # Получить список всех файлов в указанной директории
    files = os.listdir(path+folders[0])
    # Отфильтровать только файлы с расширением .xlsx
    xlsx_files = [file for file in files if file.endswith(".xlsx")]
    if not xlsx_files:
        logger.warning(f'По пути {path+folders[0]} отсутствуют файлы описания функции .xlsx')
        return (['noxlsx',], False)

    #print(xlsx_files)

    tex_str = []
    isInfo = False
    if ln+'.xlsx' in xlsx_files:
        df = pd.read_excel(path+folders[0]+'/'+ln+'.xlsx')

        for index, row in df.iterrows():
            row_done, isInfoStr = parse_row(row)
            if isInfoStr:
                isInfo = True
            if not row_done:
                continue
            temp = f'\centering {row_done[0]} & \centering {row_done[1]} & \centering {row_done[2]} & \centering {row_done[3]} & \centering\\arraybackslash {row_done[4]} \\\\'
            tex_str.append(temp)
            tex_str.append('\hline')
    else:
        return (['noxlsx',], False)
    if not tex_str:
        insred = '\\textcolor{red}{ПУСТАЯ ФУНКЦИЯ!!!}'
        err = f'\centering {insred} & \centering {ln} & \centering -- & \centering -- & \centering\\arraybackslash -- \\\\'
        logger.warning(f'Пустая функция {ln}')
        return ([err,], False)   
    return (tex_str, isInfo)