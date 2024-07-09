import fitz  # Импортируем библиотеку PyMuPDF
import re
import os
import sys
import json

from logger import logger

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from .dict1 import abbrs
from .tex_strs import intro_strs, outro_strs

def get_abbrs(word_list):
    # оставляем только слова по шаблону - первые две бкувы заглавные - остальные любые
    new_word_list = []
    for word in word_list:
        cleaned_string = re.sub(r'^[\(]', '', word)
        cleaned_string = re.sub(r'[\)\»]*$', '', cleaned_string)
        cleaned_string = re.sub(r'\d+$', '', cleaned_string)
        if re.match('^[A-ZА-Я]{2}[A-Za-zА-Яа-я]*$', cleaned_string):
            new_word_list.append(cleaned_string)
    #print(new_word_list)
    abbrs = []
    for word in new_word_list:
        if len(word)<=7:
            abbrs.append(word)
    set_abbrs = set(abbrs)
    return list(set_abbrs)

def extract_words_from_pdf(pdf_path):
    words = []  # Создаем пустой список для слов
    inside_toa = False
    doc = fitz.open(pdf_path)  # Открываем PDF файл
    for page_number in range(doc.page_count):  # Перебираем все страницы
        page = doc.load_page(page_number)  # Загружаем страницу
        text = page.get_text("text")  # Получаем текст со страницы
        if 'Перечень принятых сокращений' in text:
            inside_toa = True
            continue
        if inside_toa and '<ABBRS>' in text:
            inside_toa = False
            words += text.split()  # Добавляем слова в список
            continue
        if inside_toa and not '<ABBRS>' in text:
            continue
        words += text.split()  # Добавляем слова в список
    return words  # Возвращаем список слов

#  переработаная функция для GUI
def replace_pdf_with_attrs_txt(path):
    path = os.path.normpath(path)
    base_path, file_name = os.path.split(path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    new_txt_filename ='toa_' + file_name_without_extension + '.tex'
    new_attrs_filename = 'attrs_' + file_name_without_extension + '.txt'
    new_doc_filename = file_name_without_extension + '.docx'
    new_txt_path = os.path.join(base_path, new_txt_filename)
    new_attrs_path = os.path.join(base_path, new_attrs_filename)
    new_doc_path = os.path.join(base_path, new_doc_filename)
    return (path, os.path.abspath(new_txt_path), os.path.abspath(new_attrs_path), os.path.abspath(new_doc_path))

def start_abbr(filepath):

    logger.info("Запуск скрипта обновления аббревиатур...")

    pdf_path = filepath+'/general.pdf'
    # Configure logging
    #logging.basicConfig(filename='abbrs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    #logging.info("Запуск скрипта поиска аббревиатур...")
    # Ищем файл со словарем
    path_to_dict = os.getcwd()+'/dictionary.json'
    if os.path.isfile(path_to_dict):
        with open(path_to_dict, 'r', encoding='utf-8') as file:
            data = json.load(file)
            #print('found dictionary.json')
            logger.info("Найден внешний словарь аббревиатур dictionary.json")
    else:
        # Использование словаря "abbrs" в случае отсутствия файла "dict.json"
        data = abbrs
        logger.warning("Не найден внешний словарь аббревиатур dictionary.json, будет использоваться пустой внутренний словарь!")


    #paths_to_pdfs = search_pdf()
    path_to_pdf = replace_pdf_with_attrs_txt(pdf_path)

    logger.info(f"Обработка {path_to_pdf[0]}")
    word_list = extract_words_from_pdf(path_to_pdf[0])

    # убираем повторяющиеся слова
    word_set = set(word_list)
    word_list = sorted(list(word_set))

    # вытаскиваем абревиатуры
    new_word_list = get_abbrs(word_list)

    # если список пустой возвращаемся
    if not new_word_list:
        logger.warning("Нет распознанных аббревиатур в текущем файле pdf...")
        return 'noabbrs'

    new_word_list = sorted(new_word_list)
    ####################################################
    # выведем список аббревиатур в файл !!! для сбора словаря - потом можно отключить
    # Имя файла, в который нужно сохранить список строк
    # file_path = "abbrs.txt"
    with open(path_to_pdf[2], 'w', encoding='utf-8') as file:
        for line in new_word_list:
            file.write(line + ', ')
    ####################################################

    used_keys = []
    tex_list = []
    doc_list = []

    for word in new_word_list:
        # Проверяем, встречается ли ключ словаря в списке слов и не использовался ли уже
        if word in data.keys() and word not in used_keys:
            used_keys.append(word)
            value = data[word]
            #value = value[0].lower() + value[1:] # с маленькой буквы ?
            # Формируем строку tex и добавляем ее в tex_list
            tex_list.append(f'{word} & -- & {value}; \\\\'+'\n')
            doc_list.append(f'{word} - {value}')

    # Меняем в последней строке ; на точку
    if tex_list:
            last_element_index = len(tex_list) - 1
            last_element = tex_list[last_element_index]
            updated_last_element = last_element.replace('; \\\\\n', '. \\\\\n')
            tex_list[last_element_index] = updated_last_element   

    '''
        for word in new_word_list:
            # Проверка вхождения ключа словаря в строку
            for key, value in data.items():
                if key == word and key not in used_keys:
                    #print(f"Ключ '{key}' найден в строке, соответствующее значение: '{value}'.")
                    used_keys.append(key)
                    tex_list.append(f'{key} & -- & {value} \\\\'+'\n')
    '''
    final_tex = intro_strs + tex_list + outro_strs

    # Открываем файл для записи в UTF-8
    with open(path_to_pdf[1], 'w', encoding='utf-8') as file:
        for line in final_tex:
            file.write(line)  # Добавляем символ новой строки после каждой строки


    logger.info("Останов скрипта поиска аббревиатур...")
    return 'ok'

