import os

def scan_current_directory_for_pdfs():
    current_directory = os.getcwd()
    files_and_folders = os.listdir(current_directory)
    pdf_files = []

    for item in files_and_folders:
        item_path = os.path.join(current_directory, item)
        if os.path.isfile(item_path) and item.lower().endswith('.pdf'):
            pdf_files.append(item_path)

    return pdf_files

def replace_pdf_with_attrs_txt(paths):
    new_paths = []
    for path in paths:
        base_path, file_name = os.path.split(path)
        file_name_without_extension = os.path.splitext(file_name)[0]
        new_txt_filename ='toa_' + file_name_without_extension + '.tex'
        new_attrs_filename = 'attrs_' + file_name_without_extension + '.txt'
        new_doc_filename = file_name_without_extension + '.docx'
        new_txt_path = os.path.join(base_path, new_txt_filename)
        new_attrs_path = os.path.join(base_path, new_attrs_filename)
        new_doc_path = os.path.join(base_path, new_doc_filename)
        new_paths.append((path, os.path.abspath(new_txt_path), os.path.abspath(new_attrs_path), os.path.abspath(new_doc_path)))

    return new_paths

def search_pdf():
    pdf_files_list = scan_current_directory_for_pdfs()

    txt_files_list = replace_pdf_with_attrs_txt(pdf_files_list)

    list_for_return = []

    for pdf_file, txt_file, attrs_file, doc_file in txt_files_list:
        print(f"PDF Path: {pdf_file}\nTXT File Path: {txt_file}\nAttrs File Path: {attrs_file}\nDoc File Path: {doc_file}\n")
        list_for_return.append((pdf_file, txt_file, attrs_file, doc_file))

    return list_for_return