# Временное решение для тестирования устройства

from models.BinInput import BinInput
from models.BinModule import BinModule, BinModules

general_data = {
    'title_name_1': 'МИКРОПРОЦЕССОРНОЕ УСТРОЙСТВО',
    'title_name_2': 'ЗАЩИТЫ И АВТОМАТИКИ ТРАНСФОРМАТОРА',
    'title_name_3': '«ЮНИТ-М300-ДЗТ2»',
    'code': 'ЮТКБ.656122.609 БУ6',
    'terminal_name': 'ЮНИТ-М300-ДЗТ2'
}

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

def create_binary():
    properties = {
        'Status': {
            'description': 'Статус ДВ',
            'name_in_software': 'Статус',
            'name_in_fsu': '-',
            'value_range': '0 = Не активен\n1 = Активен',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
        'Mode': {
            'description': 'Режим работы ДВ',
            'name_in_software': 'Режим',
            'name_in_fsu': '-',
            'value_range': '0 = Не активен\n1 = Активен',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
        'Filtr_Time': {
            'description': 'Время фильтрации ДВ',
            'name_in_software': 'Время фильтрации',
            'name_in_fsu': '-',
            'value_range': '0...20',
            'unit': 'мс',
            'step': '1',
            'default_value': '20',
            'setpoint': '',
        },
            'Inversion': {
            'description': 'Режим инверсии ДВ',
            'name_in_software': 'Инверсия',
            'name_in_fsu': '-',
            'value_range': '0 = Не предусмотрено\n1 = Предусмотрено',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
            'Appointment': {
            'description': 'Назначение ДВ',
            'name_in_software': 'Описание',
            'name_in_fsu': '-',
            'value_range': '0...31',
            'unit': 'Символ',
            'step': '-',
            'default_value': '',
            'setpoint': '',
        },      
    }

    input1 = BinInput(properties, 'Дискретный вход 1')
    input2 = BinInput(properties, 'Дискретный вход 2')
    input3 = BinInput(properties, 'Дискретный вход 3')
    input4 = BinInput(properties, 'Дискретный вход 4')

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

    return bin_inputs


# создаем плату выходных реле
def create_binary_outs():
    properties = {
        'Status': {
            'description': 'Последняя поданная команда',
            'name_in_software': 'Статус',
            'name_in_fsu': '-',
            'value_range': 'Включено/Отключено',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
        'Mode': {
            'description': 'Режим работы реле',
            'name_in_software': 'Режим',
            'name_in_fsu': '-',
            'value_range': '0 = Выведено\n1 = Без фиксации\n2 = С фиксацией\n3 = Импульсный',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
        'Filtr_Time': {
            'description': 'Длительность импульса',
            'name_in_software': 'Дл. имп.',
            'name_in_fsu': 'Т1',
            'value_range': '(0,10…10,00)',
            'unit': 'с',
            'step': '0,01',
            'default_value': '1',
            'setpoint': '',
        },
            'Appointment': {
            'description': 'Назначение реле',
            'name_in_software': 'Описание',
            'name_in_fsu': '-',
            'value_range': '0...31',
            'unit': 'Символ',
            'step': '-',
            'default_value': '',
            'setpoint': '',
        },      
    }

    input1 = BinInput(properties, 'Реле 1')
    input2 = BinInput(properties, 'Реле 2')
    input3 = BinInput(properties, 'Реле 3')
    input4 = BinInput(properties, 'Реле 4')

    # Создаем модуль и добавляем входы
    module1 = BinModule(inserted_in_slot='M3', type='K001')
    module1.add_input(input1)
    module1.add_input(input2)
    module1.add_input(input3)
    module1.add_input(input4)
    module2 = BinModule(inserted_in_slot='M4', type='K002')
    module2.add_input(input1)
    module2.add_input(input2)
    module2.add_input(input3)
    module2.add_input(input4)

    bin_modules = BinModules('test')
    bin_modules.add_module(module1)
    bin_modules.add_module(module2)

    # Получаем словарь для использования в шаблоне Jinja
    bin_inputs = bin_modules.to_dict()

    return bin_inputs

# создаем светодиоды

def create_leds():
    properties = {
        'Data': {},
    }

    led1r = BinInput(properties, 'СД 1 (красный)')
    led1g = BinInput(properties, 'СД 1 (зеленый)')
    led2r = BinInput(properties, 'СД 2 (красный)')
    led2g = BinInput(properties, 'СД 2 (зеленый)')

    # Создаем модуль и добавляем входы
    module1 = BinModule(inserted_in_slot='-', type='ЮНИТ-ИЧМ')
    module1.add_input(led1r)
    module1.add_input(led1g)
    module1.add_input(led2r)
    module1.add_input(led2g)

    module2 = BinModule(inserted_in_slot='-', type='Дополнительный модуль светодиодов 1')
    module2.add_input(led1r)
    module2.add_input(led1g)
    module2.add_input(led2r)
    module2.add_input(led2g)

    bin_modules = BinModules('test')
    bin_modules.add_module(module1)
    bin_modules.add_module(module2)
    # Получаем словарь для использования в шаблоне Jinja
    bin_inputs = bin_modules.to_dict()
    return bin_inputs