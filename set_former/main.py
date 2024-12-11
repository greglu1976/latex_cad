import os
import json

from signals import process_xlsx_files, make_list
from inputs import process_xlsx_files_inputs, make_list_inputs

# Укажите путь к корневой папке
path_to_fbs = r'H:\www\latex_cad\set_former\01. Разработка ФБ'

# Список для хранения путей к папкам, содержащим папку xlsx
xlsx_folders = []

# Рекурсивно проходим по всем папкам и подпапкам
for root, dirs, files in os.walk(path_to_fbs):
    # Проверяем, есть ли папка xlsx в текущей директории
    if '_xlsx' in dirs:
        # Если есть, добавляем полный путь в список
        path_to_xlsx = os.path.join(root, '_xlsx', 'funcs')
        xlsx_folders.append(path_to_xlsx)

# Выводим результат
print("Папки, содержащие папку 'xlsx':")
for folder in xlsx_folders:
    print(folder)

# обрабатываем папки с xlsx
df = process_xlsx_files(xlsx_folders) # получаем суммарный датафрейм со список сигналов status, которые BOOL
#print(df)

signals = make_list(df)

# Сохранение result_list в JSON-файл
with open('signals.json', 'w', encoding='utf-8') as json_file:
    json.dump(signals, json_file, ensure_ascii=False, indent=4)

df_inputs = process_xlsx_files_inputs(xlsx_folders)
inputs = make_list_inputs(df_inputs)

# Сохранение result_list в JSON-файл
with open('inputs.json', 'w', encoding='utf-8') as json_file:
    json.dump(inputs, json_file, ensure_ascii=False, indent=4)