from docx.shared import Cm, Inches
from docx.oxml.shared import OxmlElement, qn
from docx.shared import Pt
import docx
from docx import Document
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.table import _Cell
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

import os, sys
import json

from pathlib import Path

from .dropdowns import add_formatted_dropdown2

# Определяем корень проекта
root = Path(__file__).resolve().parents[1]
descriptions_path = root / "descriptions"
#descriptions_path = Path(r'H:\www\latex_cad\latex_gui\_settings_former\descriptions')
# Проверяем правильность пути
print('==============================================================', descriptions_path)

def set_vertical_cell_direction(cell: _Cell, direction: str):
    # direction: tbRl -- top to bottom, btLr -- bottom to top
    assert direction in ("tbRl", "btLr")
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    textDirection = OxmlElement('w:textDirection')
    textDirection.set(qn('w:val'), direction)  # btLr tbRl
    tcPr.append(textDirection)

def set_repeat_table_header(row):
    """ set repeat table row on every new page
    """
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), "true")
    trPr.append(tblHeader)
    return row

def set_cell_vertical_alignment(cell, align="center"):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcValign = OxmlElement('w:vAlign')
        tcValign.set(qn('w:val'), align)
        tcPr.append(tcValign)

def set_cell_border(cell: _Cell, **kwargs):
    """
    Set cell border
    Usage:

    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existnace, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))


####################################################################################
################################ ТАБЛИЦА ДЛЯ УСТАВОК ##############################
####################################################################################

table_settings = (Inches(0.28), Inches(1.23), Inches(0.9), Inches(0.5), Inches(1.5), Inches(0.55), Inches(0.45), Inches(0.9), Inches(1.05))  #задаем ширину столбцов таблицы вывода репортов

def add_table_settings(doc, unique_key): # новая таблица исходящих отчетов
    table = doc.add_table(rows=5, cols=9)
    table.style = 'Сетка таблицы51'
    table.allow_autofit = False

    # Устанавливаем фиксированный макет таблицы с правильным пространством имен
    table._tbl.xpath('./w:tblPr')[0].append(
        parse_xml(r'<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="fixed"/>')
    )
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№'
    hdr_cells[1].text = 'Описание'
    hdr_cells[2].text = 'Наименование'
    hdr_cells[4].text = 'Значение / Диапазон'
    hdr_cells[5].text = 'Ед. изм.'
    hdr_cells[6].text = 'Шаг'
    hdr_cells[7].text = 'Значение по умолчанию'
    hdr_cells[8].text = 'Уставка'
    for i in range(0,9):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    # p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # p.runs[0].font.size = Pt(10)

    hdr_cells = table.rows[1].cells # вторая строка заголовка таблицы
    hdr_cells[2].text = 'ПО'
    hdr_cells[3].text = 'ФСУ'
    hdr_cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # третья строка со служебными тегами
    hdr_cells = table.rows[2].cells
    #hdr_cells[2].text = '{%tr for param_name, param_data in input_value.properties.items() %}'
    tag = f'for param_name, param_data in {unique_key}.properties.items()'
    hdr_cells[2].text = '{%tr '+ tag + ' %}'
    # четвертая строка со служебными тегами
    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = '{{ loop.index }}'
    hdr_cells[1].text = '{{ param_data.description }}'
    hdr_cells[2].text = '{{ param_data.name_in_software }}'
    hdr_cells[3].text = '{{ param_data.name_in_fsu }}'    
    hdr_cells[4].text = '{{ param_data.value_range }}'
    hdr_cells[5].text = '{{ param_data.unit }}'
    hdr_cells[6].text = '{{ param_data.step }}'
    hdr_cells[7].text = '{{ param_data.default_value }}'
    hdr_cells[8].text = '{{ param_data.setpoint }}'

    hdr_cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[5].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[6].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[7].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # пятая строка со служебными тегами
    hdr_cells = table.rows[4].cells
    hdr_cells[0].text = '{%tr endfor %}'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,9):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        #set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    # формируем финальный заголок слияниями ячеек
    table.cell(0, 2).merge(table.cell(0, 3))
    table.cell(0, 0).merge(table.cell(1, 0))
    table.cell(0, 1).merge(table.cell(1, 1))
    table.cell(0, 4).merge(table.cell(1, 4))
    table.cell(0, 5).merge(table.cell(1, 5))
    table.cell(0, 6).merge(table.cell(1, 6))
    table.cell(0, 7).merge(table.cell(1, 7))
    table.cell(0, 8).merge(table.cell(1, 8))

    table.cell(2, 0).merge(table.cell(2, 8))
    table.cell(4, 0).merge(table.cell(4, 8))

    for row in table.rows:
        for idx, width in enumerate(table_settings):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table

####################################################################################
################################ КОНЕЦ ТАБЛИЦА ДЛЯ УСТАВОК #########################
####################################################################################

####################################################################################
################################ ТАБЛИЦА ДЛЯ РЕГИСТРАЦИИ ###########################
####################################################################################


table_reg = (Inches(4.5), Inches(1.5), Inches(1.6), Inches(1.6), Inches(1.6))  #задаем ширину столбцов таблицы вывода репортов

def add_table_reg(doc): # новая таблица исходящих отчетов
    table = doc.add_table(rows=5, cols=5)
    table.style = 'Стиль6'
    table.allow_autofit = False

    # Устанавливаем фиксированный макет таблицы с правильным пространством имен
    table._tbl.xpath('./w:tblPr')[0].append(
        parse_xml(r'<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="fixed"/>')
    )

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Параметр'
    hdr_cells[2].text = 'Журнал событий регистрация (Не выполняется /По переднему фронту/ По заднему фронту/ По любому изменению)'
    hdr_cells[3].text = 'Осциллограф Пуск (Не выполняется/ По переднему фронту/ По заднему фронту/ По любому изменению)'
    hdr_cells[4].text = 'Осциллограф регистрация (Выведено/ Введено)'
    for i in range(0,5):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице


    hdr_cells = table.rows[1].cells # вторая строка заголовка таблицы
    hdr_cells[0].text = 'Наименование'
    hdr_cells[1].text = 'Обозначение ФСУ'
    hdr_cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    hdr_cells = table.rows[2].cells
    tag = f'for param_name, param_data in regs.properties.items()'
    hdr_cells[2].text = '{%tr '+ tag + ' %}'

    # четвертая строка со служебными тегами
    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = '{{ param_data.name }}'
    hdr_cells[1].text = '{{ param_data.fsu }}'

    #hdr_cells[2].text = '{{ param_data.log }}'
    choices_start = ["Не выполняется", "По переднему фронту", "По заднему фронту", "По любому изменению"]
    par3 = hdr_cells[2].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par3,
        choices=choices_start,
        #alias= f"DropDown_{i}",
        #instruction_text=f"Выберите ",
    )
    hdr_cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    #hdr_cells[3].text = '{{ param_data.oscill_start }}'
    par2 = hdr_cells[3].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par2,
        choices=choices_start,
        #alias= f"DropDown_{i}",
        #instruction_text=f"Выберите ",
    )
    hdr_cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    #hdr_cells[4].text = '+'
    choices_reg = ["Выведено", "Введено"]
    par1 = hdr_cells[4].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par1,
        choices=choices_reg,
        #alias= f"DropDown_{i}",
        #instruction_text=f"Выберите ",
    )
    hdr_cells[4].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # пятая строка со служебными тегами
    hdr_cells = table.rows[4].cells
    hdr_cells[0].text = '{%tr endfor %}'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,5):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        #set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    # формируем финальный заголок слияниями ячеек
    table.cell(0, 0).merge(table.cell(0, 1))
    table.cell(0, 2).merge(table.cell(1, 2))
    table.cell(0, 3).merge(table.cell(1, 3))
    table.cell(0, 4).merge(table.cell(1, 4))

    table.cell(2, 0).merge(table.cell(2, 4))
    table.cell(4, 0).merge(table.cell(4, 4))

    for row in table.rows:
        for idx, width in enumerate(table_reg):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table    

####################################################################################
################################ КОНЕЦ ТАБЛИЦА ДЛЯ РЕГИСТРАЦИИ #####################
####################################################################################


####################################################################################
############################ ТАБЛИЦА ДЛЯ МАТРИЦЫ ВЫХОДНЫХ РЕЛЕ #####################
####################################################################################

table_mtrx_outs = (Inches(2), Inches(1.7), Inches(1.7), Inches(1.7), Inches(1.7), Inches(1.7))

def add_table_mtrx_outs(doc): # новая таблица исходящих отчетов
    table = doc.add_table(rows=5, cols=6)
    table.style = 'Стиль6'
    table.allow_autofit = False

    # Устанавливаем фиксированный макет таблицы с правильным пространством имен
    table._tbl.xpath('./w:tblPr')[0].append(
        parse_xml(r'<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="fixed"/>')
    )

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Выходное реле'
    hdr_cells[1].text = 'Назначенные сигналы'

    for i in range(0,6):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    hdr_cells = table.rows[1].cells # вторая строка заголовка таблицы
    hdr_cells[1].text = '1'
    hdr_cells[2].text = '2'
    hdr_cells[3].text = '3'
    hdr_cells[4].text = '4'
    hdr_cells[5].text = '5'    
    hdr_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[4].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_cells[5].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


    hdr_cells = table.rows[2].cells
    tag = f'for param_name, param_data in bin_outputs.inputs.items()'
    hdr_cells[2].text = '{%tr '+ tag + ' %}'

    # четвертая строка со служебными тегами
    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = '{{ param_data.name }}'

    # Проверка существования файла signals.json
    if os.path.exists(descriptions_path / 'signals.json'):
        # Если файл существует, загружаем его содержимое в список
        with open(descriptions_path / 'signals.json', 'r', encoding='utf-8') as json_file:
            choices_start = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        choices_start = ['Не определен файл',]

    #choices_start = ["Не выполняется", "По переднему фронту", "По заднему фронту", "По любому изменению"]
    par1 = hdr_cells[1].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par1,
        choices=choices_start,
        #alias= f"DropDown_{i}",
        #instruction_text=f"Выберите ",
    )
    hdr_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    par2 = hdr_cells[2].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par2,
        choices=choices_start,
    )
    hdr_cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    par3 = hdr_cells[3].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par3,
        choices=choices_start,
    )
    hdr_cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    par4 = hdr_cells[4].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par4,
        choices=choices_start,
    )
    hdr_cells[4].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    par5 = hdr_cells[5].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par5,
        choices=choices_start,
    )
    hdr_cells[5].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # пятая строка со служебными тегами
    hdr_cells = table.rows[4].cells
    hdr_cells[0].text = '{%tr endfor %}'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,6):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        #set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    # формируем финальный заголок слияниями ячеек
    table.cell(0, 0).merge(table.cell(1, 0))
    table.cell(0, 1).merge(table.cell(0, 5))

    table.cell(2, 0).merge(table.cell(2, 4))
    table.cell(4, 0).merge(table.cell(4, 4))

    for row in table.rows:
        for idx, width in enumerate(table_mtrx_outs):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table 

####################################################################################
############################ КОНЕЦ ТАБЛИЦА ДЛЯ МАТРИЦЫ ВЫХОДНЫХ РЕЛЕ ###############
####################################################################################


####################################################################################
############################ ТАБЛИЦА ДЛЯ МАТРИЦЫ ДИСКРЕТНЫХ ВХОДОВ ###############
####################################################################################

table_mtrx_ins = (Inches(2), Inches(4))

def add_table_mtrx_ins(doc): # новая таблица исходящих отчетов
    table = doc.add_table(rows=4, cols=2)
    table.style = 'Стиль6'
    table.allow_autofit = False

    # Устанавливаем фиксированный макет таблицы с правильным пространством имен
    table._tbl.xpath('./w:tblPr')[0].append(
        parse_xml(r'<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="fixed"/>')
    )

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Дискретный вход'
    hdr_cells[1].text = 'Назначенный сигнал'

    for i in range(0,2):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    hdr_cells = table.rows[1].cells
    tag = f'for param_name, param_data in bin_inputs.inputs.items()'
    hdr_cells[0].text = '{%tr '+ tag + ' %}'

    # четвертая строка со служебными тегами
    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = '{{ param_data.name }}'

    # Проверка существования файла inputs.json
    if os.path.exists(descriptions_path / 'inputs.json'):
        # Если файл существует, загружаем его содержимое в список
        with open(descriptions_path / 'inputs.json', 'r', encoding='utf-8') as json_file:
            choices_start = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        choices_start = ['Не определен файл',]

    #choices_start = ["Не выполняется", "По переднему фронту", "По заднему фронту", "По любому изменению"]
    par1 = hdr_cells[1].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par1,
        choices=choices_start,
    )
    hdr_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # пятая строка со служебными тегами
    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = '{%tr endfor %}'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,2):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        #set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    # формируем финальный заголок слияниями ячеек

    table.cell(1, 0).merge(table.cell(1, 1))
    table.cell(3, 0).merge(table.cell(3, 1))

    for row in table.rows:
        for idx, width in enumerate(table_mtrx_ins):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table 

####################################################################################
############################ КОНЕЦ ТАБЛИЦА ДЛЯ МАТРИЦЫ ДИСКРЕТНЫХ ВХОДОВ ###########
####################################################################################


####################################################################################
############################ ТАБЛИЦА ДЛЯ СВЕТОДИОДОВ ###############
####################################################################################

table_leds = (Inches(2), Inches(2), Inches(4))

def add_table_leds(doc): # новая таблица исходящих отчетов
    table = doc.add_table(rows=4, cols=3)
    table.style = 'Стиль6'
    table.allow_autofit = False

    # Устанавливаем фиксированный макет таблицы с правильным пространством имен
    table._tbl.xpath('./w:tblPr')[0].append(
        parse_xml(r'<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="fixed"/>')
    )

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Светодиод'
    hdr_cells[1].text = 'Режим работы'
    hdr_cells[2].text = 'Назначенный сигнал'    

    for i in range(0,3):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    hdr_cells = table.rows[1].cells
    tag = f'for param_name, param_data in leds.inputs.items()'
    hdr_cells[0].text = '{%tr '+ tag + ' %}'

    # четвертая строка со служебными тегами
    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = '{{ param_data.name }}'

    choices = ["С фиксацией", "Без фиксации"]
    par2 = hdr_cells[1].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par2,
        choices=choices,
        default='По умолчанию'
    )
    hdr_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


    # Проверка существования файла inputs.json
    if os.path.exists(descriptions_path / 'signals.json'):
        # Если файл существует, загружаем его содержимое в список
        with open(descriptions_path / 'signals.json', 'r', encoding='utf-8') as json_file:
            choices_start = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        choices_start = ['Не определен файл',]

    #choices_start = ["Не выполняется", "По переднему фронту", "По заднему фронту", "По любому изменению"]
    par1 = hdr_cells[2].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par1,
        choices=choices_start,
    )
    hdr_cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # пятая строка со служебными тегами
    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = '{%tr endfor %}'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,3):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        #set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    # формируем финальный заголок слияниями ячеек

    table.cell(1, 0).merge(table.cell(1, 2))
    table.cell(3, 0).merge(table.cell(3, 2))

    for row in table.rows:
        for idx, width in enumerate(table_leds):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table 

####################################################################################
############################ КОНЕЦ ТАБЛИЦА ДЛЯ СВЕТОДИОДОВ ###############
####################################################################################

####################################################################################
############################ ТАБЛИЦА ДЛЯ ФУНКЦИОНАЛЬНЫХ КЛАВИШ ###############
####################################################################################

table_fks = (Inches(2), Inches(4))

def add_table_fks(doc): # новая таблица исходящих отчетов
    table = doc.add_table(rows=4, cols=2)
    table.style = 'Стиль6'
    table.allow_autofit = False

    # Устанавливаем фиксированный макет таблицы с правильным пространством имен
    table._tbl.xpath('./w:tblPr')[0].append(
        parse_xml(r'<w:tblLayout xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="fixed"/>')
    )

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Функциональная клавиша'
    hdr_cells[1].text = 'Назначенный сигнал'

    for i in range(0,2):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    hdr_cells = table.rows[1].cells
    tag = f'for param_name, param_data in fks.inputs.items()'
    hdr_cells[0].text = '{%tr '+ tag + ' %}'

    # четвертая строка со служебными тегами
    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = '{{ param_data.name }}'

    # Проверка существования файла inputs.json
    if os.path.exists(descriptions_path / 'controls.json'):
        # Если файл существует, загружаем его содержимое в список
        with open(descriptions_path / 'controls.json', 'r', encoding='utf-8') as json_file:
            choices_start = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        choices_start = ['Не определен файл',]

    #choices_start = ["Не выполняется", "По переднему фронту", "По заднему фронту", "По любому изменению"]
    par1 = hdr_cells[1].paragraphs[0]
    add_formatted_dropdown2(
        paragraph=par1,
        choices=choices_start,
    )
    hdr_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # пятая строка со служебными тегами
    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = '{%tr endfor %}'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,2):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        #set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    # формируем финальный заголок слияниями ячеек

    table.cell(1, 0).merge(table.cell(1, 1))
    table.cell(3, 0).merge(table.cell(3, 1))

    for row in table.rows:
        for idx, width in enumerate(table_fks):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table 



