import re

file_path = "general.tex"  # Путь к файлу general.tex

with open(file_path, 'r' , encoding='utf-8') as file:
    for line in file:
        if 'manualpath' in line:
            parts = line.split('{')
            desired_content = parts[-1].strip()
            desired_content = desired_content.rstrip('}')
            print("Содержимое вторых фигурных скобок в строке с подстрокой manualpath:", desired_content)