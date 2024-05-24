import os

import pandas as pd

from logger import logger

from .include_tex import dict_func
from .row_parser import parse_row


def make_tex(df_data, df_info):
    tex_list = []
    # Считываем инфо
    IEC61850Name = '*empty*'
    RussianName = '*empty*'
    for index, row in df_info.iterrows():
        if row['Parameter'] == 'RussianName':
            RussianName = row['Value']
        if row['Parameter'] == 'IEC61850Name':
            IEC61850Name = row['Value']  
    # Начинаем собирать tex файл
    desc_func = dict_func.get(RussianName,'')
    #df_data = df_data.drop(df_data[df_data['Категория (group)'] != 'status'].index)
    df_data = df_data[df_data['Категория (group)'].isin(['status', 'control'])] # оставляем только строки статуса и управления
    if df_data.empty:
        return []

    #(node_name, full_desc, short_desc, digital_input, digital_output, led, func_button, event_log, disturber, start_disturber)  
    for index, row in df_data.iterrows():
        row_parsed = parse_row(row)

        first = RussianName + '/ ' + row_parsed[0] + ': ' + row_parsed[1]

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



def collect_df(list_of_tuples):
    all_tex_string = []
    for work_tuple in list_of_tuples:
        path_to = work_tuple[0]
        funcs = work_tuple[1]
        full_path = path_to+'/_xlsx/funcs/'
        for func in funcs:
            t = full_path + func + '.xlsx'
            if os.path.isfile(t):
                #print('OK>',t)
                df_data = pd.read_excel(t, sheet_name='Signals')
                df_info = pd.read_excel(t, sheet_name='Info')
                func_tex_list = make_tex(df_data, df_info)
                if func_tex_list:
                    all_tex_string += func_tex_list
            else:
                logger.warning(f"В папке {t} нет файла, которые указан в теге ===s файла tex")
    return all_tex_string    