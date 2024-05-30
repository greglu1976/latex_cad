# функция получает на вход путь к папке
# где содержатся xlsx файлы далее в папке _latex содержатся файлы проекта
# не возвращает ничего, просто обновляет файл .tex (в первом , котором нет символа '_')
# данными из таблиц xlsx

import os
import pandas as pd

import logging


from get_df_info import df_finder, get_ln_info
from get_strs import get_strs_from_df, add_str_custom_header
#from _funcs2 import get_t1_from_xls

def xlsx_finder(folder_path):
    files = get_files_list_by_extension(folder_path, ['.xlsx', ])
    for file in files:
        #print(file)
        #file_name = os.path.splitext(os.path.basename(file))[0]
        #file_ext = os.path.splitext(os.path.basename(file))[1]
        #directory_path = os.path.dirname(file)
        xl = pd.ExcelFile(file)
        df_list = []
        if 'TechInfo' in xl.sheet_names:
            logging.info(f"Найден файл xlsx конфигурации: {file}")
            #print('YES')
            #print(file)
            # header=1 потому что заголовки со второй строчки начинаются, первая строчка пустая
            df1 = pd.read_excel(file, index_col=None, sheet_name='Settings', header=1, dtype={'DigitalInput': str, 'DigitalOutput' : str, 'FunctionalButton' : str, 'LED' : str, 'MappingMask' : str})
            df2 = pd.read_excel(file, index_col=None, sheet_name='Status information', header=1, dtype={'DigitalInput': str, 'DigitalOutput': str, 'FunctionalButton' : str, 'LED' : str, 'MappingMask' : str})

            # Объединяем два датафрейма в один
            df = pd.concat([df1, df2], ignore_index=True)
            #print(df)
            grouped = df.groupby('NodeName (рус)')
            # Итерируемся по уникальным значениям 'Значение' и создаем датафреймы для каждой группы
            for value, group in grouped:
                df_list.append(group)
                get_ln_info(group)
            return df_list # df_list содержит все датафреймы 
    return []
         
def get_files_list_by_extension(folder_path, extensions):
    files_list = []

    for root, directories, files in os.walk(folder_path):
        for filename in files:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, filename)
                files_list.append(file_path)

    return files_list

def renew_dir(folder_path, dfs):
    files = get_files_list_by_extension(folder_path, ['.tex', ])

    for file in files:
        #print(file)
        file_name = os.path.splitext(os.path.basename(file))[0]
        file_ext = os.path.splitext(os.path.basename(file))[1]
        directory_path = os.path.dirname(file)
        #print(directory_path)
        
        if file_ext=='.tex' and not '_' in file_name:
            is_inside = False
            tex_final = [] # сюда собирать будем выходной файл

            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '%===t1' in line and not is_inside:
                        tex_final.append(line) # Write the opening %===t1 tag

                        if '>' in line: # проверяем нужен ли заголовок
                            custom_header = line.split('>')[1]
                            tex_final=add_str_custom_header(custom_header, tex_final)
                            line = line.split('>')[0]
                            

                        is_inside = True
                        ln_type = line.split('*')[1].strip()
                        df_work = df_finder(ln_type, dfs)
                        # Оставляем только строки, где значение в столбце "measure" равно "value"
                        
                        if not df_work.empty:
                            df_work = df_work.loc[df_work['Категория (group)'] == 'setting']
                            #print(df_work.info)
                            add_lines = get_strs_from_df(df_work)
                            for add_line in add_lines:
                                tex_final.append(add_line)

                    elif is_inside and '%===t1' in line:
                        tex_final.append(line)  # Write the closing %===t1 tag
                        is_inside = False
                    elif is_inside:
                        continue
                    else:
                        tex_final.append(line)
                        # Открыть файл для записи в кодировке UTF-8
                        
            old_file_path = os.path.join(directory_path, file_name  + file_ext)
            new_file_path = os.path.join(directory_path, file_name  + '.bac')

            if os.path.exists(new_file_path):
                os.remove(new_file_path)
                print(f"Deleted existing file at {new_file_path}")
                logging.info(f"Удаляем существующий файл: {new_file_path}")

            os.rename(old_file_path, new_file_path)           
            #final_name = os.path.join(directory_path, '~'+file_name+'.tex')
            with open(file, 'w', encoding='utf-8') as file:
                # Записать каждую строку из списка в файл
                for line in tex_final:
                    file.write(line)
            logging.info(f"Записываем файл: {file}")



# Пример использования функции
if __name__ == "__main__":
    folder_path = 'I:/Ivanovo/Документация ЮНИТ М300/Разработка/Схемы ФБ ЮНИТ-М3/Трансформатор/ИЭУ Т 35 кВ Россети/01. Разработка ФБ/05. МТЗ'
    #renew_dir(folder_path)
    