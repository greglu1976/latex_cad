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

from dropdowns import add_formatted_dropdown2

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

table_settings = (Inches(0.28), Inches(1.23), Inches(0.9), Inches(0.4), Inches(1.6), Inches(0.55), Inches(0.45), Inches(0.9), Inches(1.05))  #задаем ширину столбцов таблицы вывода репортов

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
################################ ТАБЛИЦА ДЛЯ РЕГИСТРАЦИИ ##############################
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
























#
# НОВАЯ ТАБЛИЦА MMS СТО
#
table_reports_new = (Inches(4), Inches(3), Inches(1), Inches(0.5), Inches(0.5), Inches(0.5), Inches(2), Inches(1))  #задаем ширину столбцов таблицы вывода репортов

def add_table_reports_new(doc): # новая таблица исходящих отчетов
    table = doc.add_table(rows=2, cols=8)

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Информационный сигнал'
    hdr_cells[2].text = 'КТ'
    hdr_cells[3].text = 'ЦУС'
    hdr_cells[4].text = 'РДУ'
    hdr_cells[5].text = 'РАС'
    hdr_cells[6].text = 'Отображение в ИМ'
    for i in range(0,8):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    set_vertical_cell_direction(hdr_cells[3], 'btLr') # к 4 столбцу применяем вертикальное выранивание
    set_vertical_cell_direction(hdr_cells[4], 'btLr') # к 5 столбцу применяем вертикальное выранивание
    set_vertical_cell_direction(hdr_cells[5], 'btLr') # к 6 столбцу применяем вертикальное выранивание

    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    # p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # p.runs[0].font.size = Pt(10)

    hdr_cells = table.rows[1].cells # вторая строка заголовка таблицы
    hdr_cells[0].text = 'Наименование'
    hdr_cells[1].text = 'Статус'
    hdr_cells[6].text = 'DO'
    hdr_cells[7].text = 'DA'

    set_repeat_table_header(table.rows[1])  # повторение заголовка на след странице
    for i in range(0,8):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой


    # формируем финальный заголок слияниями ячеек
    table.cell(0, 0).merge(table.cell(0, 1))
    table.cell(0, 2).merge(table.cell(1, 2))
    table.cell(0, 3).merge(table.cell(1, 3))
    table.cell(0, 4).merge(table.cell(1, 4))
    table.cell(0, 5).merge(table.cell(1, 5))
    table.cell(0, 6).merge(table.cell(0, 7))

    #table.style = 'Сетка таблицы51'
    table.allow_autofit = False

    for row in table.rows:
        for idx, width in enumerate(table_reports_new):
            row.cells[idx].width = width
    #add_row_table_reports(table, ('','','','','','')) # добавляем пустую строчку, чтобы двойное подчеркивание сохранить
    return table

def add_row_table_reports_new(table, tuple2Add):  # Добавляем строку со значениями в Таблицу выходных сигналов
    row = table.add_row()

    '''
    leng=len(table.rows)
    if (leng==3):
        # если это первая строчка, то сверху делаем двойную черту
        row_cells = table.rows[2].cells
        for i in range(0, 8):
            set_cell_border(row_cells[i], top={"val": "double"})
'''
    for idx in range(0, 8):
        row.cells[idx].text = str(tuple2Add[idx])
        row.cells[idx].width = table_reports_new[idx]
        set_cell_vertical_alignment(row.cells[idx], align="center")
    row.cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст Нумерованный'
    row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[1].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    row.cells[2].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    row.cells[3].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[4].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    row.cells[4].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[5].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    row.cells[5].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[6].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[6].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[7].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    row.cells[7].paragraphs[0].style = 'ДОК Таблица Текст'

    return table

def add_spec_row_table_reports_new(table, tuple2Add):  # Добавляем особую строку со значениями в Таблицу выходных сигналов
    row = table.add_row()
    leng = len(table.rows)
    if (leng == 3):
        # если это первая строчка, то сверху делаем двойную черту
        row_cells = table.rows[2].cells
        for i in range(0, 8):
            set_cell_border(row_cells[i], top={"val": "double"})
    row.cells[0].text = str(tuple2Add[0])
    row.cells[0].width = table_reports_new[0]
    set_cell_vertical_alignment(row.cells[0], align="center")
    row.cells[1].text = str(tuple2Add[1])
    row.cells[1].width = table_reports_new[1]
    set_cell_vertical_alignment(row.cells[1], align="center")

    for idx in range(0, 8):
        row.cells[idx].paragraphs[0].style = 'ДОК Таблица Текст'

    table.cell(leng-1, 1).merge(table.cell(leng-1, 7))
    # заливка особой строки - там где имя набора данных
    shading_elm1 = parse_xml(r'<w:shd {} w:fill="D9D9D9"/>'.format(nsdecls('w')))
    table.cell(leng - 1, 0)._tc.get_or_add_tcPr().append(shading_elm1)
    shading_elm2 = parse_xml(r'<w:shd {} w:fill="D9D9D9"/>'.format(nsdecls('w')))
    table.cell(leng - 1, 1)._tc.get_or_add_tcPr().append(shading_elm2)




#
# ТАБЛИЦЫ ДЛЯ ОТЧЕТА по уставкам
#

# по параметрам функций
table_sg_sw = (Inches(2), Inches(7), Inches(3), Inches(2))  #задаем ширину столбцов
def add_table_sg_sw(doc): # таблица программных переключателей
    table = doc.add_table(rows=1, cols=4)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Наименование параметра'
    hdr_cells[1].text = 'Пояснение'
    hdr_cells[2].text = 'Состояния программного переключателя'
    hdr_cells[3].text = 'Состояние программного переключателя по умолчанию'
    for i in range(0,4):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице


    table.style = 'Сетка таблицы51'
    table.allow_autofit = False
    for row in table.rows:
        for idx, width in enumerate(table_sg_sw):
            row.cells[idx].width = width
    return table

table_sg_sw_new = (Inches(2), Inches(7), Inches(3))  #задаем ширину столбцов
def add_table_sg_sw_new(doc): # таблица программных переключателей
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Наименование'
    hdr_cells[1].text = 'Пояснение'
    hdr_cells[2].text = 'Состояния программного переключателя'

    for i in range(0,3):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице

    table.style = 'Сетка таблицы51'
    table.allow_autofit = False
    for row in table.rows:
        for idx, width in enumerate(table_sg_sw_new):
            row.cells[idx].width = width
    return table


def add_row_table_sg_sw(table, tuple2Add):  # Добавляем строку со значениями в Таблицу параметров
    row = table.add_row()
    #print('tuple=========', tuple2Add)
    for idx in range(0, 4):
        row.cells[idx].text = str(tuple2Add[idx])
        set_cell_vertical_alignment(row.cells[idx], align="center")
    row.cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[1].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[2].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[3].paragraphs[0].style = 'ДОК Таблица Текст'
    return table


# Добавить ряд в таблицу с курсивом
def add_row_table_sg_sw_new(table, tuple2Add):  # Добавляем строку со значениями в Таблицу параметров
    row = table.add_row()

    row.cells[0].text = str(tuple2Add[0])
    set_cell_vertical_alignment(row.cells[0], align="center")
    row.cells[1].text = str(tuple2Add[1])
    set_cell_vertical_alignment(row.cells[1], align="center")


    sg_vals = str(tuple2Add[2]).split('/')
    tt = row.cells[2].paragraphs[0]
    for i,sg_val in enumerate(sg_vals):
        if sg_val == str(tuple2Add[3]):
            tt.add_run(sg_val).italic=True 
        else:
            tt.add_run(sg_val)
        if not(i==len(sg_vals)-1): 
            tt.add_run(' / ')

    row.cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[1].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[2].paragraphs[0].style = 'ДОК Таблица Текст'

    return table



def add_row_table_sg_sw_empty(table, tuple2Add):  # отличия от обычной функции add_row_table_sg_sw - не ставит первый столбец как нумерованный текст
    row = table.add_row()
    for idx in range(0, 4):
        row.cells[idx].text = str(tuple2Add[idx])
        #row.cells[idx].width = table_sg_sw[idx]
        set_cell_vertical_alignment(row.cells[idx], align="center")
    row.cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст' # вот здесь отличие !!!!!
    row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[1].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[2].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[3].paragraphs[0].style = 'ДОК Таблица Текст'
    return table

def merge_table_sg_sw_header(table):
    num_row = len(table.rows)
    table.cell(num_row-1, 0).merge(table.cell(num_row-1, 3))
    text = table.cell(num_row-1, 0).text.replace('\n','')
    table.cell(num_row - 1, 0).text = text.strip()
    # после верхних манипуляций теряется стиль ячейки, прописываем его заново
    row = table.rows[num_row-1]
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст Строгий'
    return table


def merge_table_sg_sw_header_new(table):
    num_row = len(table.rows)
    table.cell(num_row-1, 0).merge(table.cell(num_row-1, 2))
    text = table.cell(num_row-1, 0).text.replace('\n','')
    table.cell(num_row - 1, 0).text = text.strip()
    # после верхних манипуляций теряется стиль ячейки, прописываем его заново
    row = table.rows[num_row-1]
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст Строгий'
    return table


'''
def add_row_table_sg_sw_final(table): # добавляем финальную строчку в таблицу
    row = table.add_row()
    table.cell(len(table.rows)-1, 0).merge(table.cell(len(table.rows)-1, 2))
    row.cells[0].text = '* - значение программного переключателя по умолчанию'
    set_cell_vertical_alignment(row.cells[0], align="center")
    row.cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст' # вот здесь отличие !!!!!
    return table

'''
    
######
###### ТАБЛИЦЫ ДЛЯ РАС
######

table_ras = (Inches(7), Inches(5), Inches(3))  #задаем ширину столбцов
def add_table_ras(doc): # таблица программных переключателей
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Сигнал функции устройства'
    hdr_cells[1].text = 'Обозначение сигнала'
    hdr_cells[2].text = 'Фаза'

    set_repeat_table_header(table.rows[0]) # повторение заголовка на след странице  
    for i in range(0,3):
        p = hdr_cells[i].paragraphs[0]
        p.style = 'ДОК Таблица Заголовок'
        set_cell_vertical_alignment(hdr_cells[i], align="center")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        set_cell_border(hdr_cells[i], bottom={"val": "double"}) # подчеркиваем заголовок двойной чертой

    table.style = 'Сетка таблицы51'
    table.allow_autofit = False
    for row in table.rows:
        for idx, width in enumerate(table_ras):
            row.cells[idx].width = width
    return table

def add_row_table_ras(table, tuple2Add):  # Добавляем строку со значениями
    row = table.add_row()

    for idx in range(0, 3):
        row.cells[idx].text = str(tuple2Add[idx])
        set_cell_vertical_alignment(row.cells[idx], align="center")
    row.cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[0].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[1].paragraphs[0].style = 'ДОК Таблица Текст'
    row.cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    row.cells[2].paragraphs[0].style = 'ДОК Таблица Текст'
    return table