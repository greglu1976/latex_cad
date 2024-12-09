# заполнение шаблона данными

from docxtpl import DocxTemplate
from models.BinModule import BinModule, BinModules
from models.BinInput import BinInput

from general import general_data


from inputs import input1, input2, input3, input4
# Создаем модуль и добавляем входы
module1 = BinModule(inserted_in_slot='M1', type='B001')
module1.add_input(input1)
module1.add_input(input2)
module1.add_input(input3)
module1.add_input(input4)
module2 = BinModule(inserted_in_slot='M2', type='B002')
module2.add_input(input1)
module2.add_input(input2)
module2.add_input(input3)
module2.add_input(input4)

bin_modules = BinModules('test')
bin_modules.add_module(module1)
bin_modules.add_module(module2)

# Получаем словарь для использования в шаблоне Jinja
bin_inputs = bin_modules.to_dict()
#print(module_dict)
# Выводим словарь
#import pprint
#pprint.pprint(module_dict)
#print(module_dict)
# Загрузка шаблона .docx
doc = DocxTemplate('templ2.docx')
#doc = DocxTemplate('templ.docx')

# Заполнение шаблона данными
context = {
    "general_data": general_data,
    "bin_inputs": bin_inputs,
    "bin_outputs": bin_inputs,
    }
doc.render(context)

# Сохранение документа
doc.save('output.docx')