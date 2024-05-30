
import os
import re

import logging

from _searcher_apx import find_apx
from _searcher_func import find_funcs
from _generator import generate_df
from _generate_tex import generate_tex
from _prepare_df import prepare_df
from _changer_appendix import change_app_a

# Configure logging
logging.basicConfig(filename='tbl2_renewer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Запуск скрипта...")

file_name = "general.tex"

# Ищем, есть ли приложение А (по тэгу %===a1 в general.tex) 
path_to_app_a = find_apx(file_name)
if path_to_app_a!='':
    paths_to_funcs = find_funcs(file_name)
    if not paths_to_funcs:
        logging.error(f"Не найдено тегов %===f или путей для функций")
    else:
        df = generate_df(paths_to_funcs) # tex_list  список сигналов в формате tex
        dfs = prepare_df(df) # разбиение датафрейма на несколько по группам, dfs - список df
        tex = generate_tex(dfs) # генерация строк тех из списка датафреймов
        change_app_a(path_to_app_a, tex) # вносим измененные строчки в приложение А
 
logging.info("Останов скрипта...")