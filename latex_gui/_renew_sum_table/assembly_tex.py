import os
import shutil

from logger import logger

def assembly_tex(final_tex, app_path):
    print(app_path +'/_latex/app1.tex')
    # Проверяем наличие файла в текущем каталоге
    if os.path.isfile(app_path +'/_latex/app1.tex'):
        with open(app_path +'/_latex/app1.tex', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    else:
        logger.error(f"Файл {app_path}/_latex/app1.tex не найден")
        return ('error',f"Файл {app_path}/_latex/app1.tex не найден")

    gen_tex = []
    is_inside = False
    for line in lines:
        if '%===t2' in line and not is_inside:
            is_inside = True
            gen_tex.append(line)
            for tex_line in final_tex:
                gen_tex.append(tex_line)            
            continue
        if '%===t2' in line and is_inside:
            is_inside = False
            gen_tex.append(line)
            continue
        if is_inside:
            continue
        if not is_inside:
            gen_tex.append(line)
    #print(app_path +'/app2.tex')

    if os.path.isfile(app_path +'/_latex/app1.tex'):
        shutil.copy(app_path +'/_latex/app1.tex', app_path +'/_latex/app1.bac')

    with open(app_path +'/_latex/app1.tex', 'w', encoding='utf-8') as file:
        for line in gen_tex:
            file.write(line)  


    return ('ok', '')