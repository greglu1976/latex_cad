import hashlib
import pandas as pd
import os

from db_main import handle_df

def find_names(df):
    for index, row in df.iterrows():
        if row['61850_LN'] != '-':
            return row['61850_LN']
    return '_empty_'


def analize_dfs(dfs):
    df_info = pd.read_excel('1.xlsx', sheet_name='TechInfo', header=1)
    IEC61850Name = '*empty*'
    RussianName = '*empty*'
    for index, row in df_info.iterrows():
        if row['Parameter'] == 'RussianName':
            RussianName = row['Value']
        if row['Parameter'] == 'IEC61850Name':
            IEC61850Name = row['Value']        

    for df in dfs:
        # Создаем копию датафрейма
        df_copy = df.copy()
        df_copy.drop(columns=['61850_LN'], inplace=True)
        df_copy.drop(columns=['NodeName (рус)'], inplace=True)
        df_copy = df_copy.sort_values(by=["ShortDescription"], ascending=True)
        # Преобразовать датафрейм в строку
        df_string = df_copy.to_string(index=False)
        # Вычислить хэш-сумму
        df_hash = hashlib.sha256(df_string.encode('utf-8')).hexdigest()
        # собираем информационный датафрейм
        df_info_func = pd.DataFrame(columns=['Parameter', 'Value'])
        temp_df = pd.DataFrame([{'Parameter': 'RussianName', 'Value': RussianName}])
        df_info_func = pd.concat([df_info_func, temp_df], ignore_index=True)
        temp_df = pd.DataFrame([{'Parameter': 'IEC61850Name', 'Value': IEC61850Name}])
        df_info_func = pd.concat([df_info_func, temp_df], ignore_index=True)
        temp_df = pd.DataFrame([{'Parameter': 'Hash', 'Value': df_hash}])
        df_info_func = pd.concat([df_info_func, temp_df], ignore_index=True)
        print(df_info_func)

        if not os.path.exists(f'{IEC61850Name}'):
         # Если папки "out" нет, то создаем ее
            os.makedirs(f'{IEC61850Name}')
        # Создание объекта ExcelWriter
        df = df.sort_values(by=["FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)"], ascending=True)
        name = find_names(df)
        with pd.ExcelWriter(f'./{IEC61850Name}/{name}.xlsx') as writer:
            df.to_excel(writer, sheet_name=f'{name}', index=False)  # Сохранение второго DataFrame в Excel            
            df_info_func.to_excel(writer, sheet_name='Info', index=False)  # Сохранение первого DataFrame в Excel

        # Передаем в базу данных
        handle_df(IEC61850Name, RussianName, dfs)





