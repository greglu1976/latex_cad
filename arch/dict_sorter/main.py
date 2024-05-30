import json

# Считываем словарь из файла dict1.json
with open('dictionary.json', 'r', encoding='utf-8') as file:
    dict1 = json.load(file)

# Сортируем словарь по ключам
sorted_dict = {k: dict1[k] for k in sorted(dict1)}

# Сохраняем отсортированный словарь в файл dict2.json
with open('_dictionary.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_dict, file, ensure_ascii=False, indent=4)

print("Словарь успешно отсортирован и сохранен в файл dict2.json")