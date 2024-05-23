# По принятому списку путей к функциям, ищем tex файлы и собираем из них реальные пути к xlsx файлам
# возвращаем назад список этих путей
import os

from logger import logger


def find_tex(function_path):
    """ Ищем есть ли tex файл и он один в папке """
    path = function_path +'/_latex/'
    tex_files = []
    if os.path.isdir(path):
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        logger.warning(f"Папка {path} не существует")
        return ['error', f'Папка {path} не существует']         
    if not files:
        logger.warning(f"В папке {path} нет файлов")
        return ['error', f'В папке {path} нет файлов']
    else:
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(file)
        if not tex_files:
            logger.warning(f"В папке {path} нет tex файла описания функции")
            return ['error', f'В папке {path} нет tex файла описания функции']
        if len(tex_files)>1:
            logger.warning(f"В папке {path} больше одного tex файла описания функции")
            return ['error', f'В папке {path} больше одного tex файла описания функции']          
    return tex_files


def get_func_names(path_to_tex):
    """ Ищем имена функции и файлов (так как они одинаковы) из файла tex описания функции """
    ''' здесь старая версия
    with open(path_to_tex, 'r', encoding='utf-8') as file:
        names_list = []
        for line in file:
            if '%===t1*' in line:
                print(path_to_tex, line)
                line_prep = line.split('*')[1]
                if '>' in line_prep:
                    names_list.append(line_prep.split('>')[0].strip())
                else:
                    names_list.append(line_prep.strip())
    print(path_to_tex, names_list)
    '''
    with open(path_to_tex, 'r', encoding='utf-8') as file:
        func_names = []
        for line in file:
            if '%===s' in line:
               line_prep = line.replace('%===s', '')
               line_prep = line_prep.replace('\n', '')
               line_prep = line_prep.replace(' ', '')               
               func_names = line_prep.split(',')
               break
        return func_names      

def get_xlsx_paths(function_paths):
    for function_path in function_paths:
        result = find_tex(function_path)
        if result[0] == 'error':
            continue
        func_names = get_func_names(function_path +'/_latex/'+ result[0])
    