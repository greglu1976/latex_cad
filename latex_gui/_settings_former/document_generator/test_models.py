# заполнение шаблона данными

from docxtpl import DocxTemplate

from relay import create_relay, create_binary, general_data, create_binary_outs, create_leds, create_fks, create_reg

from pathlib import Path

# Получаем текущий полный путь
current_path = Path.cwd()
# Поднимаемся на один уровень выше
parent_path = current_path.parent
# Формируем путь к папке templates
templates_path = parent_path / 'templates'
# Указываем путь к файлу origin.docx
doc_path = templates_path / 'templ2.docx'
doc = DocxTemplate(doc_path)

# забираем словарь РЗА
rza_funcs = create_relay()
bin_inputs = create_binary()
regs = create_reg()
outs = create_binary_outs()
leds = create_leds()
fks = create_fks()
#print(leds)
# Заполнение шаблона данными
context = {
    "general_data": general_data,
    "bin_inputs": bin_inputs,
    "bin_outputs": outs,
    "rza_funcs": rza_funcs,
    "regs": regs,
    "leds": leds,
    "fks": fks,    
    }
doc.render(context)

#doc_path2 = templates_path / 'output.docx'
# Сохранение документа
doc.save('output.docx')