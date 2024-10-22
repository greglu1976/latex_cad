import os
import re

import pandas as pd

from logger import logger

from .include_tex import dict_func
from .row_parser import parse_row_new

def generate_tex(df):
    tex_list=[]
    for index, row in df.iterrows():
        row_parsed = parse_row_new(row)
        if 'Индикация поведения' in row_parsed[1] or 'Индикация исправности' in row_parsed[1]: # Здесь исключаем МЭК сигналы Beh и Health из списка
            continue
        if row_parsed[0] == 'control':
            first = row_parsed[1]
        else:    
            first = row_parsed[10] + '/ ' + row_parsed[0] + ': ' + row_parsed[1]

        tex_list.append(
        '\centering ' + first + 
        ' & \centering ' + row_parsed[2] + 
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


def make_tex_all(all_dfs): # новые строки
    summ_df = pd.DataFrame()
    for tuple_df in all_dfs:
        RussianName = tuple_df[1].loc[tuple_df[1]['Parameter'] == 'RussianName', 'Value'].values[0] if 'RussianName' in tuple_df[1]['Parameter'].values else '*empty*'        
        df_data_temp = tuple_df[0]

        df_data_temp['RussianName'] = RussianName.replace('x', str(tuple_df[2]))
        df_data_temp['ShortDescription'] = df_data_temp['ShortDescription'].str.replace('x', str(tuple_df[2]))
        #df_data_temp['NodeName (рус)'] = df_data_temp['NodeName (рус)'].str.replace('x', str(tuple_df[2]))
        df_data_temp['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)'] = df_data_temp['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)'].str.replace('x', str(tuple_df[2]))

        df_data = df_data_temp[df_data_temp['Категория (group)'].isin(['status', 'control'])] # оставляем только строки статуса и управления
        summ_df = pd.concat([summ_df, df_data], ignore_index=True)
    if summ_df.empty:
        return []
################################################## ВЫШЕ СОБРАЛИ ОБЩИЙ ДАТАФРЕЙМ ################################
    tex_list = []
    #print(summ_df)
    df_ctrl = summ_df[summ_df['Категория (group)'].isin(['control'])]
    if not df_ctrl.empty:
        df_buttons = df_ctrl[df_ctrl['reserved1'] == 'button']
        df_switches = df_ctrl[df_ctrl['reserved1'] != 'button']
        if not df_switches.empty:
            tex_list.append('\multicolumn{9}{|c|}{Виртуальные ключи} \\\\'+'\n')
            tex_list.append('\hline'+'\n')
            tex_list +=generate_tex(df_switches)
        if not df_buttons.empty:
            df_buttons = df_buttons.drop_duplicates(subset=['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)'])
            tex_list.append('\multicolumn{9}{|c|}{Виртуальные кнопки} \\\\'+'\n')
            tex_list.append('\hline'+'\n')
            tex_list +=generate_tex(df_buttons)            
    df_status = summ_df[summ_df['Категория (group)'].isin(['status'])]
    if not df_status.empty:
        tex_list.append('\multicolumn{9}{|c|}{Сигналы функциональной логики} \\\\'+'\n')
        tex_list.append('\hline'+'\n')
        tex_list +=generate_tex(df_status)

    return tex_list

def collect_df(list_of_tuples):
    all_dfs = []# новые строки
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
                    #print('OK>',t)
                    df_data = pd.read_excel(t, sheet_name='Signals')
                    df_info = pd.read_excel(t, sheet_name='Info')
                    all_dfs.append((df_data, df_info, x))   # в этом списке туплов датафреймы по всем функциям  # новые строки   
                else:
                    logger.warning(f"В папке {t} нет файла, которые указан в теге ===s файла tex")

    all_tex_string_new = make_tex_all(all_dfs) # новые строки
    return all_tex_string_new                 
