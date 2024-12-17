import os
import pandas as pd

# Список исключений (файлы, которые нужно обрабатывать)
include_files = ['control.xlsx',]

def process_xlsx_files_controls(file_paths):

    # Глобальный датафрейм для объединения всех Signals
    total_signals_df = pd.DataFrame()

    for path_to_folder in file_paths:

        # Список файлов для обработки
        xlsx_files = [file for file in os.listdir(path_to_folder) if file.endswith('.xlsx') and file in include_files]

        # Проверка наличия файлов
        if not xlsx_files:
            #print("В папке нет подходящих файлов.")
            continue

        # Датафрейм для объединения листов Signals
        signals_df = pd.DataFrame()

        # Список значений RussianName из листов Info
        russian_names = []

        # Обработка каждого файла
        for file in xlsx_files:
            file_path = os.path.join(path_to_folder, file)
            
            # Чтение файла
            xls = pd.ExcelFile(file_path)
            
            # Обработка листов Signals
            if 'Signals' in xls.sheet_names:
                signals_sheet = pd.read_excel(xls, sheet_name='Signals')
                signals_df = pd.concat([signals_df, signals_sheet], ignore_index=True)
            
            # Обработка листов Info
            if 'Info' in xls.sheet_names:
                info_sheet = pd.read_excel(xls, sheet_name='Info', header=None)  # Без заголовка
                
                # Поиск строки, где первый столбец содержит "RussianName"
                for index, row in info_sheet.iterrows():
                    if row[0] == 'RussianName':
                        russian_name = row[1]  # Значение во втором столбце
                        russian_names.append(russian_name)
                        break  # Прерываем цикл, так как нашли нужное значение

        # Проверка значений RussianName
        RussianName = russian_names[0] if russian_names and all(name == russian_names[0] for name in russian_names) else 'ошибка'

        # Создаем маску для фильтрации
        mask = (signals_df['Note (Справочная информация)'] != 'исключить') & (signals_df['Категория (group)'] == 'control')
        # Создаем новый DataFrame с копией отфильтрованных данных
        filtered_df = signals_df[mask].copy()

        filtered_df['RussianNameFB'] = RussianName

        # Объединяем данные из текущей папки с общим датафреймом
        total_signals_df = pd.concat([total_signals_df, filtered_df], ignore_index=True)
    #print(total_signals_df)
    return total_signals_df


def make_list_controls(df):
    # Список для хранения результатов
    result_list = []
    # Итерация по строкам DataFrame
    for index, row in df.iterrows():
        # Сборка строки
        combined_string = (
            f"{row['ShortDescription']} "
        )
        # Добавление строки в список
        result_list.append(combined_string)
    result_set = set(result_list)
    result_list = list(result_set )    
    #print(result_list)
    return result_list



if __name__ == '__main__':
    file_paths = [r'H:\www\latex_cad\set_former\01. Разработка ФБ\01. ЛО ГЗ Т откл\_xlsx\funcs', r'H:\www\latex_cad\set_former\01. Разработка ФБ\17. ДЗТ 35\_xlsx\funcs',]
    df = process_xlsx_files_controls(file_paths)
    #print(df)
