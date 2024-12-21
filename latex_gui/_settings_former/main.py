import json, os

#from pathlib import Path

from .data_processor.main import start_process
from .document_generator.test_table import starter_test_table
from .document_generator.test_models import starter_test_models

def start_all_settings(path_to_general):
    file_name = path_to_general + "/general.tex"
    #print(path_to_general)
    signals, inputs, controls, settings, input_modules, output_modules, path_to_hw_ied, led_modules, fk_modules = start_process(file_name)

    # Определяем абсолютный путь к папке description
    #current_path = Path(__file__).resolve().parent
    #descriptions_path = current_path / "descriptions"
    #descriptions_path = current_path / 'descriptions'

    with open('signals.json', 'w', encoding='utf-8') as json_file:
        json.dump(signals, json_file, ensure_ascii=False, indent=4)
    with open('inputs.json', 'w', encoding='utf-8') as json_file:
        json.dump(inputs, json_file, ensure_ascii=False, indent=4)
    with open('controls.json', 'w', encoding='utf-8') as json_file:
        json.dump(controls, json_file, ensure_ascii=False, indent=4)
    with open('settings.json', 'w', encoding='utf-8') as json_file:
        json.dump(settings, json_file, ensure_ascii=False, indent=4)
    with open('bin_inputs.json', 'w', encoding='utf-8') as json_file:
        json.dump(input_modules.to_dict(), json_file, ensure_ascii=False, indent=4)
    with open('bin_outputs.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_modules.to_dict(), json_file, ensure_ascii=False, indent=4)
    with open('leds.json', 'w', encoding='utf-8') as json_file:
        json.dump(led_modules.to_dict(), json_file, ensure_ascii=False, indent=4)
    with open('fks.json', 'w', encoding='utf-8') as json_file:
        json.dump(fk_modules.to_dict(), json_file, ensure_ascii=False, indent=4)
    #templates_path = current_path / 'templates'
    #doc_path = templates_path / 'origin.docx'
    #doc_path2 = templates_path / 'templ2.docx'
    
    starter_test_table()
    starter_test_models(path_to_hw_ied)

    os.remove('signals.json')
    os.remove('inputs.json')
    os.remove('controls.json')
    os.remove('settings.json')
    os.remove('bin_inputs.json')
    os.remove('bin_outputs.json')
    os.remove('leds.json')
    os.remove('fks.json')    
    return 'ok'

if __name__=='__main__':
    name = 'general.tex'
    start_all_settings(name)