import os
import pandas as pd

def process_xlsx_files(file_paths):
    """
    Функция для обработки списка путей к Excel-файлам.
    Возвращает суммарный датафрейм с добавленным столбцом RussianNameFB.
    """
    # Датафрейм для объединения листов Signals
    signals_df = pd.DataFrame()

    # Список значений RussianName из листов Info
    russian_names = []

    # Обработка каждого файла
    for file_path in file_paths:
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
    if russian_names:
        if all(name == russian_names[0] for name in russian_names):
            RussianName = russian_names[0]
        else:
            RussianName = 'ошибка'
    else:
        RussianName = 'ошибка'

    # Фильтрация строк
    filtered_df = signals_df.loc[
        (signals_df['Категория (group)'] == 'status') &  # Условие для 'Категория (group)'
        (signals_df['type'] == 'BOOL')                  # Условие для 'type'
    ]

    # Добавление столбца RussianNameFB
    filtered_df['RussianNameFB'] = RussianName

    return filtered_df, RussianName

# Пример использования функции
if __name__ == '__main__':
    # Указанный путь
    path_to_folder = r'H:\www\latex_cad\set_former\01. Разработка ФБ\01. ЛО ГЗ Т откл\_xlsx\funcs'

    # Список исключений (файлы, которые не нужно обрабатывать)
    exclude_files = ['control.xlsx', 'inputs.xlsx']

    # Список файлов для обработки
    xlsx_files = [os.path.join(path_to_folder, file) for file in os.listdir(path_to_folder) if file.endswith('.xlsx') and file not in exclude_files]

    # Проверка наличия файлов
    if not xlsx_files:
        print("В папке нет подходящих файлов.")
        exit()

    # Вызов функции
    result_df, russian_name = process_xlsx_files(xlsx_files)

    # Вывод результатов
    print("Объединенный датафрейм Signals:")
    print(result_df)

    print("\nЗначение RussianName:")
    print(russian_name)