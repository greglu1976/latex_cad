import fitz
import pandas as pd
import os
import ezdxf

def extract_text_from_dxf(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    mtext = []
    for entity in doc.modelspace():
        if entity.dxftype() == 'MTEXT':
            mtext.append(entity.plain_text())
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(mtext))
        # Создание DataFrame
    df = pd.DataFrame(mtext, columns=['Строка'])
    df['Число повторений'] = df.groupby('Строка')['Строка'].transform('count')
    df = df.drop_duplicates()
    df.to_excel('_dxf.xlsx', index=False)

if os.path.isfile('1.pdf'):
# Открываем файл PDF
    pdf_document = fitz.open('1.pdf')
    # Получаем объект страницы
    page = pdf_document[0]
    # Получаем текст с первой страницы
    text = page.get_text()
    # Выводим текст с первой страницы
    with open('_pdf.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    word_list = text.split('\n')
    # Создание DataFrame
    df = pd.DataFrame(word_list, columns=['Строка'])
    # Подсчет количества повторений каждой строки
    df['Число повторений'] = df.groupby('Строка')['Строка'].transform('count')
    # Удаление дубликатов строк
    df = df.drop_duplicates()
    # Сохранение DataFrame в Excel
    df.to_excel('_pdf.xlsx', index=False)

if os.path.isfile('1.dxf'):
    # Пример использования
    input_file = '1.dxf'
    output_file = '_dxf.txt'
    extract_text_from_dxf(input_file, output_file)
