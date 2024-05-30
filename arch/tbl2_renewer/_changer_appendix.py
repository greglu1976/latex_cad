
import os

import logging


def _get_files_list_by_extension(folder_path, extensions):
    files_list = []

    for root, directories, files in os.walk(folder_path):
        for filename in files:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, filename)
                files_list.append(file_path)

    return files_list

def change_app_a(path_to_app_a, tex):

    files = _get_files_list_by_extension(path_to_app_a, ['.tex', ])

    for file in files:
        file_name = os.path.splitext(os.path.basename(file))[0]
        file_ext = os.path.splitext(os.path.basename(file))[1]
        directory_path = os.path.dirname(file)
        
        if file_ext=='.tex' and not '_' in file_name:
            is_inside = False
            tex_final = [] # сюда собирать будем выходной файл

            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '%===t2' in line and not is_inside:
                        tex_final.append(line) # Write the opening %===t2 tag
                        is_inside = True
                        tex_final+=tex
                    elif is_inside and '%===t2' in line:
                        tex_final.append(line)  # Write the closing %===t1 tag
                        is_inside = False
                    elif is_inside:
                        continue
                    else:
                        tex_final.append(line)
                        
            old_file_path = os.path.join(directory_path, file_name  + file_ext)
            new_file_path = os.path.join(directory_path, file_name  + '.bac')

            if os.path.exists(new_file_path):
                os.remove(new_file_path)
                print(f"Deleted existing file at {new_file_path}")
                logging.info(f"Удаляем существующий файл: {new_file_path}")

            os.rename(old_file_path, new_file_path)           
            #final_name = os.path.join(directory_path, '~'+file_name+'.tex')
            with open(file, 'w', encoding='utf-8') as file:
                # Записать каждую строку из списка в файл
                for line in tex_final:
                    file.write(line)
            logging.info(f"Записываем файл: {file}")