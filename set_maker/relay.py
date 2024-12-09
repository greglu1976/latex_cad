from models.BinInput import BinInput
from models.BinModule import BinModule, BinModules, Prot

from docxtpl import DocxTemplate
from general import general_data

def create_relay():
    properties = {
        'Status': {
            'description': 'Ввод функции в работу',
            'name_in_software': 'Ввод_функции',
            'name_in_fsu': 'SGF1',
            'value_range': '0 = Не предусмотрено\n1 = Предусмотрено',
            'unit': '-',
            'step': '1',
            'default_value': '0',
            'setpoint': '',
        },
        'Mode': {
            'description': 'Ток срабатывания',
            'name_in_software': 'Iср',
            'name_in_fsu': 'I>',
            'value_range': '(0,10…30,00)',
            'unit': 'о.е.',
            'step': '0,01',
            'default_value': '1,00',
            'setpoint': '',
        },    
    }

    input1 = BinInput(properties, 'Общие уставки')
    input2 = BinInput(properties, 'МТЗ 1 ступень')
    input3 = BinInput(properties, 'МТЗ 2 ступень')
    input4 = BinInput(properties, 'МТЗ 3 ступень')


    # Создаем функциональный блок  и добавляем входы(функции)
    module1 = BinModule(inserted_in_slot='-', type='Максимальная токовая защита (МТЗ)')
    module1.add_input(input1)
    module1.add_input(input2)
    module1.add_input(input3)
    module1.add_input(input4)
    module2 = BinModule(inserted_in_slot='-', type='Токовая защита нулевой последовательности (ТЗНП)')
    module2.add_input(input1)
    module2.add_input(input2)
    module2.add_input(input3)
    module2.add_input(input4)

    bin_modules = BinModules('РЗА')
    bin_modules.add_module(module1)
    bin_modules.add_module(module2)

    # Получаем словарь для использования в шаблоне Jinja
    module_dict = bin_modules.to_dict()

    return module_dict