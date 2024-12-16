#Собираем пути к функциям РЗА из файла general.tex РЭ 
import os
from pathlib import Path

def extract_paths(file_content):
    paths = []
    fbpath = None
    
    # Разбиваем файл на строки
    lines = file_content.split('\n')
    
    
    # Находим путь к описанию железа (не закомментированный)
    path_to_hw_ied=''
    path_to_hw_gen=''
    for line in lines:
        line = line.strip()
        if line.startswith(r'%===h'):
            # Извлекаем путь между фигурными скобками
            path_to_hw_ied = Path(line.split(' ', 1)[1])
            #print('path_to_hw_ied ============>', path_to_hw_ied)
            break
        # Если путь найден, создаём путь на уровень выше
    if path_to_hw_ied:
        hw_parent_path = path_to_hw_ied.parents[0] 
        #print('hw_parent_path ============>', hw_parent_path)
        # Удаляем последний сегмент пути и добавляем '\00. Общее'
        #path_to_hw_gen = r'\\'.join(path_to_hw_ied.split(r'\\')[:-1]) + r'\00. Общее'  
        if os.path.exists(hw_parent_path / "00. Общее" ):   
            path_to_hw_gen = hw_parent_path / "00. Общее"
            #print('path_to_hw_gen ============>', path_to_hw_gen)

    # Находим активный fbpath (не закомментированный)
    for line in lines:
        line = line.strip()
        if line.startswith(r'\newcommand{\fbpath}') and not line.startswith('%'):
            # Извлекаем путь между фигурными скобками
            fbpath = line.split('{')[-1].rstrip('}')
            break
    
    if not fbpath:
        return paths

    # Ищем пути между тегами %===f
    in_section = False
    for line in lines:
        line = line.strip()
        
        # Пропускаем комментарии
        if line.startswith('%') and not line.startswith('%===f'):
            continue
            
        # Проверяем начало и конец секции
        if line == '%===f':
            in_section = not in_section
            continue
            
        # Если мы внутри секции и строка содержит \input
        if in_section and '\input{' in line:
            # Извлекаем путь между фигурными скобками
            path = line.split('{')[-1].rstrip('}')
            # Заменяем \fbpath на реальный путь
            if path.startswith('\\fbpath'):
                path = path.replace('\\fbpath', fbpath)
            temp_path = Path(path)
            parent_path = temp_path.parents[1] 
            if os.path.exists(parent_path / "_xlsx" / "funcs"):   
                paths.append(parent_path / "_xlsx" / "funcs")

    return paths, path_to_hw_ied, path_to_hw_gen

if __name__=='__main__':

    with open('general.tex', 'r', encoding='utf-8') as file:
        content = file.read()

    #print(content)

    paths = extract_paths(content)
    for path in paths:
        print(path)
