import os, sys
import pandas as pd
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ..models.BinInput import BinInput
from ..models.BinModule import BinModule, BinModules

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
            #print("В папке нет подходящих файлов.")
            continue

        # Датафрейм для объединения листов Signals
        signals_df = pd.DataFrame()
        signals_df['descriptionFunc'] = '' 

        # Список значений RussianName из листов Info
        russian_name = 'Не указано'
        descriptionFB = 'Не указано'
        weight_fb = 10000


        # Обработка каждого файла
        for file in xlsx_files:
            file_path = os.path.join(path_to_folder, file)
            #print(file_path)
            descriptionFunc = 'Не указано'
            weight_func = 10000           
            # Чтение файла
            xls = pd.ExcelFile(file_path)

            info_sheet = pd.read_excel(xls, sheet_name='Info', header=None)  # Без заголовка
            for index, row in info_sheet.iterrows():
                if row[0] == 'DescriptionFunc':
                    descriptionFunc = row[1]  # Значение во втором столбце 
                if row[0] == 'WeightFunc':
                    weight_func = row[1]  # Значение во втором столбце                     

            # Обработка листов Signals
            if 'Signals' in xls.sheet_names:
                signals_sheet = pd.read_excel(xls, sheet_name='Signals')
                signals_sheet['descriptionFunc'] = descriptionFunc 
                signals_sheet['WeightFunc'] = weight_func 
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
                    if row[0] == 'WeightFB':
                        weight_fb = row[1]  # Значение во втором столбце                        

    # Проверка значений RussianName
    #RussianName = russian_names[0] if russian_names and all(name == russian_names[0] for name in russian_names) else 'ошибка'

        # Создаем маску для фильтрации
        mask = signals_df['Категория (group)'] == 'setting'
        # Создаем новый DataFrame с копией отфильтрованных данных
        filtered_df = signals_df[mask].copy()
        filtered_df['RussianNameFB'] = russian_name
        filtered_df['descriptionFB'] = descriptionFB
        filtered_df['WeightFB'] = weight_fb

        # Объединяем данные из текущей папки с общим датафреймом
        total_signals_df = pd.concat([total_signals_df, filtered_df], ignore_index=True)
    #sorted_df =  total_signals_df.sort_values(by=['WeightFB', 'WeightFunc'], ascending=[True, True])   
    #print(sorted_df)
    #sorted_df.to_excel('sorted_df.xlsx', index=False, engine='openpyxl')
    return total_signals_df


def make_list_settings(df):
    # Разбиение датафрейма на список датафреймов по полю RussianNameFB
    grouped_dfs = [group for _, group in df.groupby('RussianNameFB')] # Разбиваем по ФБ
    # Отсортировать список grouped_dfs по первой ячейке столбца WeightFB
    grouped_dfs = sorted(grouped_dfs, key=lambda df: df['WeightFB'].iloc[0])
    modules = BinModules('РЗА')
    for i, group_df in enumerate(grouped_dfs):
        grouped_df = [group for _, group in group_df.groupby('NodeName (рус)')]
        # Отсортировать список grouped_df по первой ячейке столбца WeightFunc
        grouped_df = sorted(grouped_df, key=lambda df: df['WeightFunc'].iloc[0])
        #print(grouped_df)
        module = BinModule(inserted_in_slot='-', type=group_df.iloc[0]['descriptionFB'] +' (' + group_df.iloc[0]['RussianNameFB'] + ')')
        for j, func_df in enumerate(grouped_df):
            #print(f"Датафрейм {j + 1}:")
            #print(func_df)
            #print()

            properties = {}
            for index, row in func_df.iterrows():
                unit_temp = row[8]
                low_val = row[9]
                high_val = row[10]
                step_temp = row[11]
                default_temp = row[12]
                if unit_temp == 'мс':
                    unit_temp = 'с'
                    low_val = low_val/1000
                    high_val = high_val/1000
                    step_temp = step_temp/1000
                    default_temp = default_temp/1000
                # Определяем количество знаков после запятой в step_temp
                decimal_places = str(step_temp).split('.')[-1]  # Находим часть после точки
                num_decimal_places = len(decimal_places) if '.' in str(step_temp) else 0

                # Определяем форматирование с нужным количеством знаков
                low_val = f"{low_val:.{num_decimal_places}f}".replace('.', ',')
                high_val = f"{high_val:.{num_decimal_places}f}".replace('.', ',')
                step_temp = f"{step_temp:.{num_decimal_places}f}".replace('.', ',')
                default_temp = f"{default_temp:.{num_decimal_places}f}".replace('.', ',')
                # Меняем елочки <<>>
                desc_temp = row[3]
                desc_temp = desc_temp.replace("<<", "'")
                desc_temp = desc_temp.replace(">>", "'")                
                
                value_range = low_val + '...' + high_val
                name_in_fsu = row[5]
                if 'SGF' in name_in_fsu:
                    result = {}
                    # Разбиваем строку по шаблону "цифра - значение"
                    input_str = row[6]
                    pairs = []
                    current_pair = ''
                    
                    # Разбираем строку с учетом возможных запятых в значениях
                    for i, char in enumerate(input_str):
                        current_pair += char
                        if char == ',' and any(next_char.isdigit() for next_char in input_str[i+1:i+3]):
                            pairs.append(current_pair.rstrip(',').strip())
                            current_pair = ''
                    if current_pair:
                        pairs.append(current_pair.strip())

                    print('====pairs>', pairs)

                    for pair in pairs:
                        if '-' in pair:
                            key, value = pair.split('-', 1)
                            result[key.strip()] = value.strip()

                    default_temp = result.get(default_temp)  # выставляем значение по умолчанию
                    value_range = "\n".join(f"{key} = {value}" for key, value in result.items())





                properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
                    'description': desc_temp,  # 
                    'name_in_software': row[4],  # 
                    'name_in_fsu': name_in_fsu,  # 
                    'value_range': value_range,  # 
                    'unit': unit_temp,  # 
                    'step': step_temp,  #                        
                    'default_value': default_temp,  # 
                    'setpoint': ' ',                                               
                }
            input_name = 'Общие уставки' if func_df.iloc[0]['descriptionFunc']=='Блок управления' else func_df.iloc[0]['descriptionFunc'] + ' (' + func_df.iloc[0]['NodeName (рус)'] + ')' 
            input = BinInput(properties, input_name)
            #print('================',input)
            module.add_input(input)
        #print(module)
        modules.add_module(module)
    #print(modules)
    
    return modules




if __name__=='__main__':
    paths = [r'H:\www\latex_cad\set_former\01. Разработка ФБ\01. ЛО ГЗ Т откл\_xlsx\funcs', r'H:\www\latex_cad\set_former\01. Разработка ФБ\17. ДЗТ 35\_xlsx\funcs']
    data = process_xlsx_files_settings(paths)
    #print(data)
    modules = make_list_settings(data)
    # Сохраняем датафрейм в Excel
    data.to_excel("output.xlsx", index=False)

    module_dict = modules.to_dict()
    #print(module_dict)
    with open('settings.json', 'w', encoding='utf-8') as json_file:
        json.dump(module_dict, json_file, ensure_ascii=False, indent=4)

