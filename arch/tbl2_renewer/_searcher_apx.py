
import os
import re

import logging

def find_apx(general_tex_name):
    # Проверяем наличие файла в текущем каталоге
    if os.path.isfile(general_tex_name):
        with open(general_tex_name, 'r', encoding='utf-8') as file:
            inside_appendix_tag = False
            path=''
    # ИЩЕМ ПУТЬ К ПРИЛОЖЕНИЮ А
            for line in file:
                if inside_appendix_tag:
                    if line.strip() == "%===a1":
                        break
                    else:
                        if not line.strip().startswith('%'):
                            match = re.search(r'\\input{(.*?)/_latex', line)
                            if match:
                                path = match.group(1)
                                break
                else:
                    if line.strip() == "%===a1":
                        inside_appendix_tag = True

        # Выводим содержимое списка appenix_paths
        if path != '':
            logging.info(f"В файле '{general_tex_name}' найден тег %===a1, путь к приложению А: " + path)
        else:
            logging.error(f"В файле '{general_tex_name}' нет тега %===a1!")

    else:
        logging.error(f"Файл '{general_tex_name}' не найден в текущем каталоге")
    return path