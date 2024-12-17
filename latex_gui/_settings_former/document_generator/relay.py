# Временное решение для тестирования устройства
#            !!! ДЛЯ ТЕСТИРОВАНИЯ !!!

import os, json, sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

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
    if os.path.exists('settings.json'):
        # Если файл существует, загружаем его содержимое в список
        with open('settings.json', 'r', encoding='utf-8') as json_file:
            bin_inputs = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        bin_inputs = ['Не определен файл',]
    return bin_inputs    


def create_binary():
        # Проверка существования файла bin_inputs.json
    if os.path.exists('bin_inputs.json'):
        # Если файл существует, загружаем его содержимое в список
        with open('bin_inputs.json', 'r', encoding='utf-8') as json_file:
            bin_inputs = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        bin_inputs = ['Не определен файл',]
    return bin_inputs

def create_binary_outs():
        # Проверка существования файла bin_outputs.json
    if os.path.exists('bin_outputs.json'):
        # Если файл существует, загружаем его содержимое в список
        with open('bin_outputs.json', 'r', encoding='utf-8') as json_file:
            bin_outputs = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        bin_outputs = ['Не определен файл',]
    return bin_outputs

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

# создаем функциональные клавиши
def create_fks():
    properties = {
        'Data': {},
    }

    fk1 = BinInput(properties, 'ФК 1')
    fk2 = BinInput(properties, 'ФК 2')
    fk3 = BinInput(properties, 'ФК 3')
    fk4 = BinInput(properties, 'ФК 4')


    # Создаем модуль и добавляем входы
    module1 = BinModule(inserted_in_slot='-', type='ЮНИТ-ИЧМ')
    module1.add_input(fk1)
    module1.add_input(fk2)
    module1.add_input(fk3)
    module1.add_input(fk4)

    module2 = BinModule(inserted_in_slot='-', type='Дополнительный модуль функциональных клавиш 1')
    module2.add_input(fk1)
    module2.add_input(fk2)
    module2.add_input(fk3)
    module2.add_input(fk4)

    bin_modules = BinModules('test')
    bin_modules.add_module(module1)
    bin_modules.add_module(module2)
    # Получаем словарь для использования в шаблоне Jinja
    bin_inputs = bin_modules.to_dict()
    return bin_inputs

def create_reg():
        # Проверка существования файла inputs.json
    if os.path.exists('signals.json'):
        # Если файл существует, загружаем его содержимое в список
        with open('signals.json', 'r', encoding='utf-8') as json_file:
            signals = json.load(json_file)
    else:
        # Если файл не существует, инициализируем список значением ['Не определен файл',]
        signals = ['Не определен файл',]

    # Создаем словарь properties в цикле
    properties = {}
    for index, signal in enumerate(signals):
        properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
            'name': signal,  # Используем текущий элемент списка signals
            'fsu': '-',
            'log': '-',
            'oscill_start': '-',
            'oscill_reg': '-'
        }

    #print(properties)

    input1 = BinInput(properties, 'Сигналы для регистрации')
    #input2 = BinInput(properties, 'Сигналы ФСУ')

    # Создаем функциональный блок  и добавляем входы(функции)
    module = BinModule(inserted_in_slot='-', type='Максимальная токовая защита (МТЗ)')
    module.add_input(input1)
    #module.add_input(input2)

    # Получаем словарь для использования в шаблоне Jinja
    module_dict = module.to_dict()

    return module_dict