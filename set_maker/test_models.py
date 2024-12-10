# заполнение шаблона данными

from docxtpl import DocxTemplate
from models.BinModule import BinModule, BinModules
from models.BinInput import BinInput

from relay import create_relay, create_binary, general_data
from test_reg import create_reg

doc = DocxTemplate('templ2.docx')

# забираем словарь РЗА
rza_funcs = create_relay()
bin_inputs = create_binary()
regs = create_reg()
print(regs)
# Заполнение шаблона данными
context = {
    "general_data": general_data,
    "bin_inputs": bin_inputs,
    "bin_outputs": bin_inputs,
    "rza_funcs": rza_funcs,
    "regs": regs,
    }
doc.render(context)

# Сохранение документа
doc.save('output.docx')