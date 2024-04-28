# парсит xlsx от чебоксар
# выделяет типы лог узлов и сохраняет каждый в свой файл
# в exe еще не переведена - добавлена сортировка датафреймов функций перед выводом в эксел 23.04.24

import pandas as pd

from logger import logger
from get_df import get_df

logger.info("Запуск скрипта...")

df = get_df()

logger.info("Штатный останов скрипта...")




