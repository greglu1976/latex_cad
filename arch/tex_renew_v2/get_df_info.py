# функция получает датафрейм и возвращает тупл
# (Тип ЛН, Имя функции, хэш)

import hashlib
import numpy as np
import pandas as pd

import logging

def df_checker(df):
    unique_vals = df['61850_TypeLN'].dropna().unique()
    if len(unique_vals) == 0:
        ln_type = np.nan
    elif len(unique_vals) > 1:
        ln_type = 'Error'
    else:
        ln_type = unique_vals[0]
    return ln_type

def get_ln_info(df):
    
    
    ln_type = df_checker(df)

    ln = df['NodeName (рус)'].iloc[0]

    # В подсчете хэша не учавствуют столбцы ниже, при этом столбцы 'DigitalInput', 'DigitalOutput', 'FunctionalButton', 'LED', 'MappingMask'
    # исключены из за того что при считывании эксел в датафрейм НЕ правильно интерпретируются 0 -> 0.0, в некоторых столбцах
    df_cleaned = df.drop(['Name GEB', 'NodeName (рус)', '61850_DataObjectName', '61850_Reference'], axis=1)  # Удаляем столбцы 'Name GEB' и 'NodeName (рус)'
    df_cleaned = df_cleaned.reindex(sorted(df.columns), axis=1)
    df_cleaned = df_cleaned.reset_index(drop=True)
    hash_value = hashlib.sha256(df_cleaned.to_string().encode()).hexdigest()
    
    # Создаем имя файла на основе значения столбца 'Значение'
    #file_name = f"{ln}{ln_type}.xlsx"
    # Сохраняем каждый датафрейм в отдельный Excel файл
    #df_cleaned.to_excel(file_name, index=False)
    #if ln_type == 'FBLLN0':
        #with open('test.txt', 'a') as file_test:
            #file_test.write(df_cleaned.to_string())
            #file_test.write('==============\n')


    logging.info('(Параметры логического узла) Тип ЛУ: '+ str(ln_type)+' ЛУ: '+str(ln)+' Хэш: '+str(hash_value))
    return (ln_type, ln, hash_value)


def df_finder(lntype_name, dfs):
        for df in dfs:
            ln_type = df_checker(df)
            if ln_type == lntype_name:
                return df
        return pd.DataFrame()