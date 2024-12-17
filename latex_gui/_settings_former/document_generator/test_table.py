# Создание шаблона разделов на основе шаблона origin.docx

from docxtpl import DocxTemplate
from tables import add_table_settings
from docx import Document

from add_sect_binaries import add_sect_binaries, add_sect_reg, add_sect_mtrx_outs, add_sect_mtrx_ins, add_sect_leds_leds, add_sect_fks
from docx_handler import add_new_section, add_new_section_landscape

from pathlib import Path

# Получаем текущий полный путь
current_path = Path.cwd()
# Поднимаемся на один уровень выше
parent_path = current_path.parent
# Формируем путь к папке templates
templates_path = parent_path / 'templates'
# Указываем путь к файлу origin.docx
doc_path = templates_path / 'origin.docx'
doc = Document(doc_path)

# Добавляем подразделы с дискр вх/вых в существующий раздел Конфигурация
add_sect_binaries(doc, 'Модули дискретных входов', 'bin_input')
add_sect_binaries(doc, 'Модули дискретных выходов', 'bin_output')

#============================== УСТАВКИ РЗА ==================================
add_new_section(doc) # Создаем раздел для РЗА
section_relay = doc.add_paragraph(f'УСТАВКИ РЗА')
section_relay.style = 'ДОК Заголовок 1'
# Вставляем шаблон таблицы для уставок РЗА
add_sect_binaries(doc, 'Группа уставок №1', 'rza_func')

#========================= РЕГИСТРАЦИЯ =======================================
add_new_section_landscape(doc) # Создаем раздел для регистрации
# Добавляем заголовок
section_reg = doc.add_paragraph('НАСТРОЙКА ПАРАМЕТРОВ РЕГИСТРАЦИИ')
section_reg.style = 'ДОК Заголовок 1'
add_sect_reg(doc)

#=================================МАТРИЦА ВЫХОДОВ ================================
add_new_section_landscape(doc) # Создаем раздел для матрицы вх/вых
# Добавляем заголовок
section_mtrx = doc.add_paragraph('ПАРАМЕТРИРОВАНИЕ ДИСКРЕТНЫХ ВХОДОВ И ВЫХОДНЫХ РЕЛЕ')
section_mtrx.style = 'ДОК Заголовок 1'

section_mtrx_ins = doc.add_paragraph('Дискретные входы')
section_mtrx_ins.style = 'ДОК Заголовок 2'
add_sect_mtrx_ins(doc)

section_mtrx = doc.add_paragraph('Выходные реле')
section_mtrx.style = 'ДОК Заголовок 2'
add_sect_mtrx_outs(doc)

#================================= НАСТРОЙКА СД И ФК ================================
add_new_section_landscape(doc) # Создаем раздел для матрицы вх/вых
# Добавляем заголовок РАЗДЕЛА
section_leds = doc.add_paragraph('НАСТРОЙКА СВЕТОДИОДОВ И ФУНКЦИОНАЛЬНЫХ КЛАВИШ')
section_leds.style = 'ДОК Заголовок 1'

# Подраздел описания светодиодов
section_leds_leds = doc.add_paragraph('Светодиоды')
section_leds_leds.style = 'ДОК Заголовок 2'
add_sect_leds_leds(doc)

# Подраздел описания функциональных клавиш
section_leds_fks = doc.add_paragraph('Функциональные клавиши')
section_leds_fks.style = 'ДОК Заголовок 2'
add_sect_fks(doc)

doc_path2 = templates_path / 'templ2.docx'
doc.save(doc_path2)