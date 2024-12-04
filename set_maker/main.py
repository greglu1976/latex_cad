from docxtpl import DocxTemplate

# Загрузка шаблона .docx
doc = DocxTemplate('bu1.docx')

# Данные для заполнения шаблона
context = {
    'title_name_1': 'МИКРОПРОЦЕССОРНОЕ УСТРОЙСТВО',
    'title_name_2': 'ЗАЩИТЫ И АВТОМАТИКИ ТРАНСФОРМАТОРА',
    'title_name_3': '«ЮНИТ-М300-ДЗТ2»',
    'code': 'ЮТКБ.656122.609 БУ6',
    'terminal_name': 'ЮНИТ-М300-ДЗТ2'
}

# Заполнение шаблона данными
doc.render(context)

# Сохранение документа
doc.save('output.docx')