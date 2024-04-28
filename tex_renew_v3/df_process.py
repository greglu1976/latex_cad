import os
import pandas as pd
from logger import logger
from row_parser import parse_row

def df_finder(ln, path):
    path = path + '/_xlsx/'
    if os.path.isdir(path):
        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        print(path+folders[0])
    else:
        logger.warning(f"Путь {path} указывает на файл, а не на директорию.")
        return []
    
    # Получить список всех файлов в указанной директории
    files = os.listdir(path+folders[0])
    # Отфильтровать только файлы с расширением .xlsx
    xlsx_files = [file for file in files if file.endswith(".xlsx")]
    if not xlsx_files:
        logger.warning(f'По пути {path+folders[0]} отсутствуют файлы описания функции .xlsx')
        return []

    print(xlsx_files)

    
    if ln+'.xlsx' in xlsx_files:
        tex_str = []
        df = pd.read_excel(path+folders[0]+'/'+ln+'.xlsx')

        for index, row in df.iterrows():
            print(parse_row(row))


    return []