import os
import re

import pandas as pd

from logger import logger

from .include_tex import dict_func
from .row_parser import parse_row

def make_tex(df_data, RussianName, x):
    tex_list = []
    # Начинаем собирать tex файл
    desc_func = dict_func.get(RussianName,'')
    #df_data = df_data.drop(df_data[df_data['Категория (group)'] != 'status'].index)
    df_data = df_data[df_data['Категория (group)'].isin(['status', 'control'])] # оставляем только строки статуса и управления
    if df_data.empty:
        return []

    for index, row in df_data.iterrows():
        row_parsed = parse_row(row)
        first = RussianName.replace('x', str(x)) + '/ ' + row_parsed[0] + ': ' + row_parsed[1].replace('x', str(x))
        if 'Индикация поведения' in row_parsed[1] or 'Индикация исправности' in row_parsed[1]: # Здесь исключаем МЭК сигналы Beh и Health из списка
            continue

        tex_list.append(
        '\centering ' + first + 
        ' & \centering ' + row_parsed[2].replace('x', str(x)) + 
        ' & \centering ' + row_parsed[3] + 
        ' & \centering ' + row_parsed[4] +  
        ' & \centering ' + row_parsed[5] + 
        ' & \centering ' + row_parsed[6] +
        ' & \centering ' + row_parsed[7] + 
        ' & \centering ' + row_parsed[8] +  
        ' & \centering \\arraybackslash ' + row_parsed[9] + r' \\' + '\n'                       
        )
        tex_list.append('\hline'+ '\n')
    return tex_list

def collect_df(list_of_tuples):
    all_tex_string = []
    for work_tuple in list_of_tuples:
        path_to = work_tuple[0]
        funcs = work_tuple[1]
        full_path = path_to + '/_xlsx/funcs/'
        part_full_path = path_to + '/_xlsx/'
# проверяем путь к функциям, если функция одна то просто func, если нужно две такие же, то func(2)
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                i = 1
        else:
            temp_path = path_to + '/_xlsx/'
            folders_funcs = [f for f in os.listdir(temp_path) if os.path.isdir(os.path.join(temp_path, f))]
            filtered_folders = [folder for folder in folders_funcs if 'funcs' in folder]
            match = re.search(r'\((\d+)\)', filtered_folders[0])
            if match:
                i = int(match.group(1))
                full_path = part_full_path+filtered_folders[0]+'/'
                #print(part_full_path+filtered_folders[0])

        for x in range(1, i+1): # прогоняем сколько надо функций, в самих функциях произойдет замены x на значение x цикла
             for func in funcs:
                t = full_path + func + '.xlsx'
                if os.path.isfile(t):
                    print('OK>',t)
                    df_data = pd.read_excel(t, sheet_name='Signals')
                    df_info = pd.read_excel(t, sheet_name='Info')
                    # добавляем генерацию нескольких устройств с порядковыми номерами 1,2 и тд
                    # Считываем инфо
                    IEC61850Name = '*empty*'
                    RussianName = '*empty*'
                    for index, row in df_info.iterrows():
                        if row['Parameter'] == 'RussianName':
                            RussianName = row['Value']
                        if row['Parameter'] == 'IEC61850Name':
                            IEC61850Name = row['Value'] 
                    func_tex_list = make_tex(df_data, RussianName, x)
                    if func_tex_list:
                        all_tex_string += func_tex_list
                else:
                    logger.warning(f"В папке {t} нет файла, которые указан в теге ===s файла tex")

    return all_tex_string    