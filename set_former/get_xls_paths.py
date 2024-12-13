#Собираем пути к функциям РЗА из файла general.tex РЭ 
import os
from pathlib import Path

def extract_paths(file_content):
    paths = []
    fbpath = None
    
    # Разбиваем файл на строки
    lines = file_content.split('\n')
    
    
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

    return paths

if __name__=='__main__':

    with open('general.tex', 'r', encoding='utf-8') as file:
        content = file.read()

    #print(content)

    paths = extract_paths(content)
    for path in paths:
        print(path)
