# Собирает список входов из файлов описания хардваре

import os, sys
import copy

import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.BinInput import BinInput
from models.BinModule import BinModule, BinModules


def process_xlsx_files_binaries(path_to_hw_gen, path_to_hw_ied):
    # считаем файл описания хардваре
    #path_to_hw_gen = hw_parent_path / "00. Общее"
    xls = pd.ExcelFile(path_to_hw_ied / "hardware.xlsx")
    df_plates = pd.read_excel(xls, sheet_name='Платы', header=None)
    df_plates.fillna('*', inplace=True)
    #print(plates)

    #Собираем платы и слоты
    plates = []
    for index, row in df_plates.iterrows():
        if index == 0:  # Пропускаем первую строку (заголовок)
            continue
        plates.append((row[1], row[0]))
    # ищем уникальные типы плат
    types = []
    for plate in plates:
        types.append(plate[1])
    types = set(types)
    types = list(types)
    #print(types)

    # собираем словарь для каждого типа
    modules_inputs = []
    for type in types:
        #path_temp = path_to_hw_gen + f'\{type}.xlsx'
        path_temp = path_to_hw_gen.joinpath(f"{type}.xlsx")
        if os.path.exists(path_temp):
            xls = pd.ExcelFile(path_temp)
            sheet_names = xls.sheet_names
            
            #собираем входы
            module = BinModule(inserted_in_slot='-', type=type)
            for sheet_name in sheet_names:
                if 'Дискретный вход' in sheet_name:
                    df = xls.parse(sheet_name)
                    df.fillna(' ', inplace=True)
                    #print(sheet_name)

                    properties = {}
                    for index, row in df.iterrows():
                        step_temp = row[5]
                        default_temp = row[6]
                        value_range = row[3]

                        if '0' and '-' in value_range:
                            print(value_range)
                            step_temp = str(step_temp).split('.')[0]
                            default_temp = str(default_temp).split('.')[0]
                            value_range = value_range.strip()
                            #value_range = value_range.replace('-', '=').strip()
                            #value_range = value_range.replace(',', '\n')

                            result = {}
                            #print('====sfg>',value_range.split(',') )
                            for pair in value_range.split(','):
                                #print('====pair>', pair)
                                key, value = pair.split('-', 1)
                                result[key.strip()] = value.strip()
                            default_temp = result.get(default_temp) # выставляем значение по умолчанию
                            value_range = "\n".join(f"{key} = {value}" for key, value in result.items())
                            step_temp = '-'
                        elif step_temp!=' ' and step_temp!='*' and step_temp!='':
                            print('OK')
                            if step_temp>=1:
                                step_temp = str(step_temp).split('.',1)[0]
                                default_temp = str(default_temp).split('.',1)[0]
                                print('>>>',step_temp)

                            else:
                                #pass
                                decimal_places = str(step_temp).split('.')[-1]  # Получаем часть после точки
                                num_decimal_places = len(decimal_places)  # Количество знаков после запятой
                                # Форматируем default_temp с тем же количеством знаков после запятой
                                default_temp = f"{float(default_temp):.{num_decimal_places}f}"
                                # Заменяем точку на запятую в step_temp и default_temp
                                step_temp = str(step_temp).replace('.', ',')
                                default_temp = default_temp.replace('.', ',')


                        properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
                            'description': row[0],  # Используем текущий элемент списка signals
                            'name_in_software': '-' if row[1] == '*' else row[1],  # проверка и замена прямо в строке
                            'name_in_fsu': '-' if row[2] == '*' else row[2],  # проверка и замена прямо в строке
                            'value_range': value_range,
                            'unit': '-' if row[4] == '*' else row[4],  # проверка и замена прямо в строке
                            'step': step_temp,              
                            'default_value': default_temp,
                            'setpoint': row[7],                                               
                        }
                    input = BinInput(properties, sheet_name)
                    module.add_input(input)
            if len(module.inputs)>0:
                modules_inputs.append(module)
    #print(len(modules_inputs))

    modules_outputs = []
    for type in types:
        #path_temp = path_to_hw_gen + f'\{type}.xlsx'
        path_temp = path_to_hw_gen.joinpath(f"{type}.xlsx")
        if os.path.exists(path_temp):
            xls = pd.ExcelFile(path_temp)
            sheet_names = xls.sheet_names
            
            #собираем входы
            module = BinModule(inserted_in_slot='-', type=type)
            for sheet_name in sheet_names:
                if 'Реле' in sheet_name:
                    df = xls.parse(sheet_name)
                    df.fillna(' ', inplace=True)
                    #print(sheet_name)

                    properties = {}
                    for index, row in df.iterrows():
                        step_temp = row[5]
                        default_temp = row[6]
                        value_range = row[3]

                        if '0' and '-' in value_range:
                            print(value_range)
                            step_temp = str(step_temp).split('.')[0]
                            default_temp = str(default_temp).split('.')[0]
                            value_range = value_range.strip()
                            #value_range = value_range.replace('-', '=').strip()
                            #value_range = value_range.replace(',', '\n')

                            result = {}
                            #print('====sfg>',value_range.split(',') )
                            for pair in value_range.split(','):
                                #print('====pair>', pair)
                                key, value = pair.split('-', 1)
                                result[key.strip()] = value.strip()
                            default_temp = result.get(default_temp) # выставляем значение по умолчанию
                            value_range = "\n".join(f"{key} = {value}" for key, value in result.items())
                            step_temp = '-'
                        elif step_temp!=' ' and step_temp!='*' and step_temp!='':
                            print('OK')
                            if step_temp>=1:
                                step_temp = str(step_temp).split('.',1)[0]
                                default_temp = str(default_temp).split('.',1)[0]
                                print('>>>',step_temp)

                            else:
                                #pass
                                decimal_places = str(step_temp).split('.')[-1]  # Получаем часть после точки
                                num_decimal_places = len(decimal_places)  # Количество знаков после запятой
                                # Форматируем default_temp с тем же количеством знаков после запятой
                                default_temp = f"{float(default_temp):.{num_decimal_places}f}"
                                # Заменяем точку на запятую в step_temp и default_temp
                                step_temp = str(step_temp).replace('.', ',')
                                default_temp = default_temp.replace('.', ',')


                        properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
                            'description': row[0],  # Используем текущий элемент списка signals
                            'name_in_software': '-' if row[1] == '*' else row[1],  # проверка и замена прямо в строке
                            'name_in_fsu': '-' if row[2] == '*' else row[2],  # проверка и замена прямо в строке
                            'value_range': value_range,
                            'unit': '-' if row[4] == '*' else row[4],  # проверка и замена прямо в строке
                            'step': step_temp,              
                            'default_value': default_temp,
                            'setpoint': row[7],                                               
                        }
                    output = BinInput(properties, sheet_name)
                    module.add_input(output)
            if len(module.inputs)>0:
                modules_outputs.append(module)
    #print(len(modules_outputs))

    # Теперь в списках modules_inputs и modules_outputs образцы плат по типам
    # Нужно присвоить номер слота и собрать общий модуль

    #print(plates)
    input_modules_real = []
    output_modules_real = []
    for plate in plates:
        for module_input in modules_inputs:
            if module_input.get_type() == plate[1]:
                module_to_add = copy.deepcopy(module_input)
                module_to_add.set_slot(plate[0])
                input_modules_real.append(module_to_add)
        for module_output in modules_outputs:
            if module_output.get_type() == plate[1]:
                module_to_add = copy.deepcopy(module_output)
                module_to_add.set_slot(plate[0])
                output_modules_real.append(module_to_add)
    #print(len(input_modules_real))
    #print(len(output_modules_real))

    # собрали платы , теперь можно формировать устройство
    input_modules = BinModules('Inputs')
    for input_module_real in input_modules_real:
        input_modules.add_module(input_module_real)

    output_modules = BinModules('Outputs')
    for output_module_real in output_modules_real:
        output_modules.add_module(output_module_real)

    return input_modules, output_modules


def process_xlsx_files_fks_leds(path_to_hw_gen, path_to_hw_ied):
    # считаем файл описания хардваре
    #path_to_hw_gen = hw_parent_path / "00. Общее"
    xls = pd.ExcelFile(path_to_hw_ied / "hardware.xlsx")
    df_hmi = pd.read_excel(xls, sheet_name='ИЧМ', header=None)
    df_hmi.fillna('*', inplace=True)
    #print(plates)

    #Собираем платы и слоты
    plates = []
    for index, row in df_hmi.iterrows():
        if index == 0:  # Пропускаем первую строку (заголовок)
            continue
        plates.append((index, row[0]))
    # ищем уникальные типы плат
    types = []
    for plate in plates:
        types.append(plate[1])
    types = set(types)
    types = list(types)
    #print(types)
    #print(plates)
    # собираем словарь для каждого типа
    modules_leds = []
    for type in types:
        path_temp = path_to_hw_gen.joinpath(f"{type}.xlsx")
        if os.path.exists(path_temp):
            xls = pd.ExcelFile(path_temp)
            sheet_names = xls.sheet_names

            #собираем светодиоды
            module = BinModule(inserted_in_slot='-', type=type)
            for sheet_name in sheet_names:
                if 'Светодиод' in sheet_name:
                    df = xls.parse(sheet_name)
                    df.fillna(' ', inplace=True)
                    #print(sheet_name)

                    properties = {}
                    for index, row in df.iterrows():
                        properties[f'Signal_N{index+1}'] = {}
                        input = BinInput(properties, sheet_name + ' (' +row[0]+')')
                        module.add_input(input)
            if len(module.inputs)>0:
                modules_leds.append(module)


    # собираем словарь для каждого типа
    modules_fks = []
    for type in types:
        path_temp = path_to_hw_gen.joinpath(f"{type}.xlsx")
        if os.path.exists(path_temp):
            xls = pd.ExcelFile(path_temp)
            sheet_names = xls.sheet_names

            #собираем светодиоды
            module = BinModule(inserted_in_slot='-', type=type)
            for sheet_name in sheet_names:
                if 'Функциональная клавиша' in sheet_name:
                    properties = {}
                    input = BinInput(properties, sheet_name)
                    module.add_input(input)
            if len(module.inputs)>0:
                modules_fks.append(module)


    # Теперь в списках modules_leds и modules_fks образцы плат по типам
    # Нужно присвоить номер слота и собрать общий модуль

        #print(plates)
    leds_modules_real = []
    fks_modules_real = []
    for plate in plates:
        for module_led in modules_leds:
            if module_led.get_type() == plate[1]:
                module_to_add = copy.deepcopy(module_led)
                mod_type = module_to_add.get_type()
                module_to_add.set_type(mod_type if plate[0]==1 else mod_type +' '+ str(plate[0]-1))
                leds_modules_real.append(module_to_add)
        for module_fk in modules_fks:
            if module_fk.get_type() == plate[1]:
                module_to_add = copy.deepcopy(module_fk)
                mod_type = module_to_add.get_type()
                module_to_add.set_type(mod_type if plate[0]==1 else mod_type +' '+ str(plate[0]-1))
                fks_modules_real.append(module_to_add)
    #print(len(leds_modules_real))
    #print(len(fks_modules_real))

    # собрали платы , теперь можно формировать устройство
    led_modules = BinModules('Leds')
    for led_module_real in leds_modules_real:
        led_modules.add_module(led_module_real)

    fk_modules = BinModules('Fks')
    for fk_module_real in fks_modules_real:
        fk_modules.add_module(fk_module_real)

    return led_modules, fk_modules