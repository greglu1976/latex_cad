import json

from .get_xls_paths import extract_paths

from .signals import process_xlsx_files, make_list, make_dict_reg
from .inputs import process_xlsx_files_inputs, make_list_inputs
from .controls import process_xlsx_files_controls, make_list_controls
from .settings import process_xlsx_files_settings, make_list_settings
from .get_inputs import process_xlsx_files_binaries, process_xlsx_files_fks_leds

# Укажите путь к файлу general.tex
#path_to_fbs = r'H:\www\latex_cad\set_former\01. Разработка ФБ'
def start_process(path_to_general):
    with open(path_to_general, 'r', encoding='utf-8') as file:
        content = file.read()
    xlsx_folders, path_to_hw_ied, path_to_hw_gen = extract_paths(content)

    print('>>>', path_to_hw_ied)
    print('>>>', path_to_hw_gen)

    # обрабатываем папки с xlsx
    df = process_xlsx_files(xlsx_folders) # получаем суммарный датафрейм со список сигналов status, которые BOOL
    signals = make_list(df)
    signals.sort()
    # Сохранение result_list в JSON-файл
    #with open('signals.json', 'w', encoding='utf-8') as json_file:
        #json.dump(signals, json_file, ensure_ascii=False, indent=4)

    reg_signals = make_dict_reg(df)


    df_inputs = process_xlsx_files_inputs(xlsx_folders)
    inputs = make_list_inputs(df_inputs)
    inputs.sort()
    # Сохранение result_list в JSON-файл
    #with open('inputs.json', 'w', encoding='utf-8') as json_file:
        #json.dump(inputs, json_file, ensure_ascii=False, indent=4)

    df_controls = process_xlsx_files_controls(xlsx_folders)
    controls = make_list_controls(df_controls)
    controls.sort()
    # Сохранение result_list в JSON-файл
    #with open('controls.json', 'w', encoding='utf-8') as json_file:
        #json.dump(controls, json_file, ensure_ascii=False, indent=4)

    df_settings = process_xlsx_files_settings(xlsx_folders)
    settings = make_list_settings(df_settings)
    settings = settings.to_dict()
    #settings.sort()
    # Сохранение result_list в JSON-файл
    #with open('settings.json', 'w', encoding='utf-8') as json_file:
        #json.dump(settings, json_file, ensure_ascii=False, indent=4)

    input_modules, output_modules = process_xlsx_files_binaries(path_to_hw_gen, path_to_hw_ied)
        # сохраняем в json
    #with open('bin_inputs.json', 'w', encoding='utf-8') as json_file:
        #json.dump(input_modules.to_dict(), json_file, ensure_ascii=False, indent=4)
        
    #with open('bin_outputs.json', 'w', encoding='utf-8') as json_file:
        #json.dump(output_modules.to_dict(), json_file, ensure_ascii=False, indent=4)

    led_modules, fk_modules = process_xlsx_files_fks_leds(path_to_hw_gen, path_to_hw_ied)

    return signals, inputs, controls, settings, input_modules, output_modules, path_to_hw_ied, led_modules, fk_modules, reg_signals