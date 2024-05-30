# На вход получает пути к xlsx
# на выход отдает список строк для tex файла

import os

import logging

import pandas as pd

def generate_df(paths_to_funcs): # на вход список путей - на выходе датафрейм, собранный из xslx

    general_df = pd.DataFrame()

    logging.info('Сбор датафрейма из xlsx описаний функций...')
    for path in paths_to_funcs:
        for f in os.listdir(path):
            if f.endswith(".xlsx"):  # Проверка расширения и строки в названии файла
                path_to_f = os.path.join(path, f)
                excel = pd.ExcelFile(path_to_f)
                sheets = excel.sheet_names
                if 'TechInfo' in sheets: # проверка что тип листа таблиц ОП Чебоксары
                    logging.info(path_to_f)
                    statuses = pd.read_excel(excel, sheet_name='Status information', header=1)
                    controls = pd.read_excel(excel, sheet_name='Controls', header=1)
                    controls = controls.dropna(subset=['NodeName (рус)']) #.reset_index(drop=True) # дропаем строки с пустыми значениями в столбце NodeName
                    #statuses == pd.concat([statuses, controls], ignore_index=True) 
                    tech_info = pd.read_excel(excel, sheet_name='TechInfo', header=1) # здесь есть имя на кириллице ФБ и имя LD
                    russian_name = tech_info.loc[tech_info['Parameter'] == 'RussianName', 'Value'].values[0] # берем значение параметра RussianName - это имя ФБ в сигналах
                    statuses['RussianName'] = russian_name # добавляем столбце с наименованием ФБ в датабрэйм
                    controls['RussianName'] = russian_name # добавляем столбце с наименованием ФБ в датабрэйм
                    #statuses.to_excel(russian_name+'s.xlsx', index=False) для теста
                    #controls.to_excel(russian_name+'c.xlsx', index=False) для теста
                    general_df = pd.concat([general_df, controls], ignore_index=True)
                    general_df = pd.concat([general_df, statuses], ignore_index=True)
                    general_filtered = general_df.loc[general_df['type'] == 'BOOL']

    #general_filtered.to_excel('out.xlsx', index=False)
    logging.info('Датафрейм из xlsx собран...')
    return general_filtered
                    