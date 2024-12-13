import os
import pandas as pd

from models.BinInput import BinInput
from models.BinModule import BinModule, BinModules

# Список исключений (файлы, которые не нужно обрабатывать)
exclude_files = ['control.xlsx', 'inputs.xlsx']

def process_xlsx_files_settings(file_paths):

    # Глобальный датафрейм для объединения всех Signals
    total_signals_df = pd.DataFrame()

    for path_to_folder in file_paths:

        # Список файлов для обработки
        xlsx_files = [file for file in os.listdir(path_to_folder) if file.endswith('.xlsx') and file not in exclude_files]

        # Проверка наличия файлов
        if not xlsx_files:
            print("В папке нет подходящих файлов.")
            continue

        # Датафрейм для объединения листов Signals
        signals_df = pd.DataFrame()
        signals_df['descriptionFunc'] = '' 

        # Список значений RussianName из листов Info
        russian_name = 'Не указано'
        descriptionFB = 'Не указано'


        # Обработка каждого файла
        for file in xlsx_files:
            file_path = os.path.join(path_to_folder, file)
            #print(file_path)
            descriptionFunc = 'Не указано'            
            # Чтение файла
            xls = pd.ExcelFile(file_path)

            info_sheet = pd.read_excel(xls, sheet_name='Info', header=None)  # Без заголовка
            for index, row in info_sheet.iterrows():
                if row[0] == 'DescriptionFunc':
                    descriptionFunc = row[1]  # Значение во втором столбце 
                    break

            # Обработка листов Signals
            if 'Signals' in xls.sheet_names:
                signals_sheet = pd.read_excel(xls, sheet_name='Signals')
                signals_sheet['descriptionFunc'] = descriptionFunc 
                #print('>>>>>>>>>>>>>>', descriptionFunc)
                signals_df = pd.concat([signals_df, signals_sheet], ignore_index=True)
            
            # Обработка листов Info
            if 'LLN0' in file_path:
                info_sheet = pd.read_excel(xls, sheet_name='Info', header=None)  # Без заголовка
                # Поиск строки, где первый столбец содержит "RussianName"
                for index, row in info_sheet.iterrows():
                    if row[0] == 'RussianName':
                        russian_name = row[1]  # Значение во втором столбце
                    if row[0] == 'DescriptionFB':
                        descriptionFB = row[1]  # Значение во втором столбце

    # Проверка значений RussianName
    #RussianName = russian_names[0] if russian_names and all(name == russian_names[0] for name in russian_names) else 'ошибка'

        # Создаем маску для фильтрации
        mask = signals_df['Категория (group)'] == 'setting'
        # Создаем новый DataFrame с копией отфильтрованных данных
        filtered_df = signals_df[mask].copy()
        filtered_df['RussianNameFB'] = russian_name
        filtered_df['descriptionFB'] = descriptionFB
      
        # Объединяем данные из текущей папки с общим датафреймом
        total_signals_df = pd.concat([total_signals_df, filtered_df], ignore_index=True)
    #print(total_signals_df)
    return total_signals_df


def make_list_settings(df):

    # Разбиение датафрейма на список датафреймов по полю RussianNameFB
    grouped_dfs = [group for _, group in df.groupby('RussianNameFB')] # Разбиваем по ФБ
    modules = BinModules('РЗА')
    for i, group_df in enumerate(grouped_dfs):
        grouped_df = [group for _, group in group_df.groupby('NodeName (рус)')]
        module = BinModule(inserted_in_slot='-', type=group_df.iloc[0]['RussianNameFB'])
        for j, func_df in enumerate(grouped_df):
            #print(f"Датафрейм {j + 1}:")
            #print(func_df)
            #print()

            properties = {}
            for index, row in func_df.iterrows():
                properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
                    'description': row[0],  # Используем текущий элемент списка signals
                    'name_in_software': '-' if row[1] == '*' else row[1],  # проверка и замена прямо в строке
                    'name_in_fsu': '-' if row[2] == '*' else row[2],  # проверка и замена прямо в строке
                    'value_range': '-' if row[3] == '*' else row[3],  # проверка и замена прямо в строке
                    'unit': '-' if row[4] == '*' else row[4],  # проверка и замена прямо в строке
                    'step': '-' if row[5] == '*' else row[5],  # проверка и замена прямо в строке                       
                    'default_value': '-' if row[6] == '*' else row[6],  # проверка и замена прямо в строке
                    'setpoint': row[7],                                               
                }
            input = BinInput(properties, func_df.iloc[0]['NodeName (рус)'])
            print('================',input)
            module.add_input(input)
        #print(module)
        #modules.add_module(module)
    #print(modules)
        




    return








if __name__=='__main__':
    paths = [r'H:\www\latex_cad\set_former\01. Разработка ФБ\01. ЛО ГЗ Т откл\_xlsx\funcs', r'H:\www\latex_cad\set_former\01. Разработка ФБ\17. ДЗТ 35\_xlsx\funcs']
    data = process_xlsx_files_settings(paths)
    #print(data)
    make_list_settings(data)
    # Сохраняем датафрейм в Excel
    data.to_excel("output.xlsx", index=False)

