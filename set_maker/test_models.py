from docxtpl import DocxTemplate
from models.BinModule import BinModule
from models.BinInput import BinInput

from general import general_data


from inputs import input1, input2, input3, input4
# Создаем модуль и добавляем входы
module = BinModule()
module.add_input(input1)
module.add_input(input2)
module.add_input(input3)
module.add_input(input4)

# Получаем словарь для использования в шаблоне Jinja
module_dict = module.to_dict()

# Выводим словарь
#import pprint
#pprint.pprint(module_dict)
#print(module_dict)
# Загрузка шаблона .docx
doc = DocxTemplate('bu1.docx')
#doc = DocxTemplate('templ.docx')

# Заполнение шаблона данными
context = {
    "general_data": general_data,
    "module_dict": module_dict,
    }
doc.render(context)

# Сохранение документа
doc.save('output.docx')