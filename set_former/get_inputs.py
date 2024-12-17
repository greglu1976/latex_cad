# Собирает список входов из файлов описания хардваре

import os
import copy
import json

import pandas as pd
from pathlib import Path

from models.BinInput import BinInput
from models.BinModule import BinModule, BinModules

#path_to_hw = r'H:\www\latex_cad\set_former\hardwaretest'

#path_to_hw_gen = path_to_hw + r'\00. Общее'
#path_to_hw_ied = path_to_hw + r'\01. ЮНИТ-М3-ДЗТ2'

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
                        properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
                            'description': row[0],  # Используем текущий элемент списка signals
                            'name_in_software': '-' if row[1] == '*' else row[1],  # проверка и замена прямо в строке
                            'name_in_fsu': '-' if row[2] == '*' else row[2],  # проверка и замена прямо в строке
                            'value_range': '-' if row[3] == '*' else row[3],  # проверка и замена прямо в строке
                            'unit': '-' if row[4] == '*' else row[4],  # проверка и замена прямо в строке
                            'step': '-' if row[5] == '*' else row[5],  # проверка и замена прямо в строке                       
                            'default_value': '-' if row[6] == '*' else row[6],  # проверка и замена прямо в строке
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
                        properties[f'Signal_N{index+1}'] = {  # Добавляем новый ключ в словарь
                            'description': row[0],  # Используем текущий элемент списка signals
                            'name_in_software': '-' if row[1] == '*' else row[1],  # проверка и замена прямо в строке
                            'name_in_fsu': '-' if row[2] == '*' else row[2],  # проверка и замена прямо в строке
                            'value_range': '-' if row[3] == '*' else row[3],  # проверка и замена прямо в строке
                            'unit': '-' if row[4] == '*' else row[4],  # проверка и замена прямо в строке
                            'step': '-' if row[5] == '*' else row[5],  # проверка и замена прямо в строке                       
                            'default_value': '-' if row[6] == '*' else row[6],  # проверка и замена прямо в строке
                            'setpoint': row[7],                                               
                        }
                    output = BinInput(properties, sheet_name)
                    module.add_input(output)
            if len(module.inputs)>0:
                modules_outputs.append(module)
    #print(len(modules_outputs))

    # Теперь в списках modules_inputs и modules_outputs образцы плат по типам
    # Нужно присвоить номер слота и собрать общий модуль

    print(plates)
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
    print(len(input_modules_real))
    print(len(output_modules_real))

    # собрали платы , теперь можно формировать устройство
    input_modules = BinModules('Inputs')
    for input_module_real in input_modules_real:
        input_modules.add_module(input_module_real)

    output_modules = BinModules('Outputs')
    for output_module_real in output_modules_real:
        output_modules.add_module(output_module_real)

    return input_modules, output_modules




