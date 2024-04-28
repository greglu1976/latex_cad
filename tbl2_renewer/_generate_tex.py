# На вход получает датафрейм
# на выход отдает список строк для tex файла

import logging
import pandas as pd

def generate_tex(dfs): # на вход датафрейм - на выходе список строк дл тех
    logging.info('Сбор тех файла из df c атрибутами функций...')
    logging.info(f'В составе списка {str(len(dfs))} групп(-ы)') 

    # Создадим словарь, где ключами будут значения 'first', 'second', 'last', а значениями - сами датафреймы
    df_dict = {'SYS': pd.DataFrame(), 'PROT': pd.DataFrame(), 'NODATA': pd.DataFrame()}
    #   Заполним словарь с учетом значения 'order' в каждом датафрейме
    for df in dfs:
        order_value = df['Group'].iloc[0]
        df_dict[order_value] = df

    # Теперь отсортируем словарь по ключам в нужном порядке
    sorted_df_dict = {key: df_dict[key] for key in ['SYS', 'PROT', 'NODATA']}
    # Теперь вы можете итерировать по отсортированным датафреймам

    tex_include = []

    for key, df in sorted_df_dict.items():
        #print(f"Iterating over DataFrame with order: {key}")
        # Логика обработки данных в зависимости от ключа
        if key == 'SYS' and not df.empty:
            tex_include.append("\\multicolumn{9}{|c|}{" + "Системные сигналы"  + "} \\\\"+"\n")
            tex_include.append("\\hline\n")
        elif key == 'PROT' and not df.empty:
            tex_include.append("\\multicolumn{9}{|c|}{" + "Сигналы РЗА"  + "} \\\\"+"\n")
            tex_include.append("\\hline\n")
        elif key == 'NODATA' and not df.empty:
            tex_include.append("\\multicolumn{9}{|c|}{" + "Прочие сигналы"  + "} \\\\"+"\n")
            tex_include.append("\\hline\n")
        # Итерация по строкам и вывод каждой строки

        for index, row in df.iterrows():
            col_01 = row['RussianName']+'/' + row['NodeName (рус)']+':' + row['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)']
            col_02 = row['ShortDescription']
            col_03 = str(row['DigitalInput'])
            col_04 = str(row['DigitalOutput'])
            col_05 = str(row['LED'])
            col_06 = str(row['FunctionalButton'])
            col_07 = str(row['EventReg'])
            col_08 = '+'
            col_09 = '+'
            latex_str = ('\centering ' + col_01  + ' & \centering ' + col_02 + ' & \centering ' + col_03 + ' & \centering ' + col_04 + ' & \centering ' + col_05 + 
            ' & \centering ' + col_06 + ' & \centering ' + col_07 + ' & \centering ' + col_08 + ' & \\centering\\arraybackslash ' + col_09 + '\\\\'+'\n')
            tex_include.append(latex_str)
            tex_include.append("\\hline\n")

    return tex_include
