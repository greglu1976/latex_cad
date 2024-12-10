import os

from finder2 import process_xlsx_files
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

df = process_xlsx_files(xlsx_folders)

print(df)
