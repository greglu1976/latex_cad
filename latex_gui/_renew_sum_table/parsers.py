import re

def parse_func_paths(lines):
    function_paths = []
    inside_func_tag = False
    current_func = []
    fbpath=''
    isFoundFbPath = False
# ИЩЕМ ПУТИ К ФУНКЦИЯМ
    for line in lines:
        if 'fbpath' in line and not isFoundFbPath and not line.strip().startswith('%'):
            isFoundFbPath = True
            fbparts = line.split('{')
            fb_content = fbparts[-1].strip()
            fbpath = fb_content.rstrip('}')+'/'
        if inside_func_tag:
            if line.strip() == "%===f":
                inside_func_tag = False
            else:
                current_func.append(line.strip())
                # Проверяем строку на наличие пути и добавляем его в список если найден и строка не начинается с %
                if not line.strip().startswith('%'):
                    match = re.search(r'\\input{(.*?)/_latex', line)
                    if match:
                        path = match.group(1)
                        if '\\fbpath/' in path:
                            path = path.replace('\\fbpath/', '')
                        function_paths.append(fbpath+path)
        else:
            if line.strip() == "%===f":
                inside_func_tag = True
    return function_paths


def parse_app_path(lines):
    app_path = ''
    inside_app_tag = False
    isFoundPath = False
# ИЩЕМ ПУТЬ К ПРИЛОЖЕНИЮ А
    for line in lines:
        if 'apppath' in line and not isFoundPath and not line.strip().startswith('%'):
            isFoundPath = True
            fbparts = line.split('{')
            fb_content = fbparts[-1].strip()
            apppath = fb_content.rstrip('}')+'/'
        if inside_app_tag:
            if line.strip() == "%===a1":
                inside_app_tag = False
            else:
                # Проверяем строку на наличие пути и добавляем его в список если найден и строка не начинается с %
                if not line.strip().startswith('%'):
                    match = re.search(r'\\input{(.*?)/_latex', line)
                    if match:
                        path = match.group(1)
                        if '\\apppath/' in path:
                            path = path.replace('\\apppath/', '')
                        app_path = apppath+path
                        break
        else:
            if line.strip() == "%===a1":
                inside_app_tag = True
    return app_path    
