import json
from _get_abbrs.dict1 import abbrs


# Сохранение словаря с отступами
with open('dictionary.json', 'w', encoding='utf-8') as file:
    json.dump(abbrs, file, indent=4, ensure_ascii=False)