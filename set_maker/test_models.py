# заполнение шаблона данными

from docxtpl import DocxTemplate
from models.BinModule import BinModule, BinModules
from models.BinInput import BinInput

from relay import create_relay, create_binary, general_data, create_binary_outs, create_leds, create_fks, create_reg

doc = DocxTemplate('templ2.docx')

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

# Сохранение документа
doc.save('output.docx')