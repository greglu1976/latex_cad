from tables import add_table_settings

def add_sect_binaries(doc, name_sect, type):

    tag1 = f'for {type}s_key, {type}s in {type}s.modules.items()'       
    # Создаем подраздел
    subsection_bin = doc.add_paragraph(f'{name_sect} '+ '{% ' + tag1 + ' %}')
    subsection_bin.style = 'ДОК Заголовок 2'

    # Создаем подраздел с тегами
    tag3 = f'{type}s.inserted_in_slot'
    tag4 = f'{type}s.type'
    tag5 = f'for {type}_key, {type} in {type}s.inputs.items()'
    subsubsection_bin = doc.add_paragraph('Слот {{ ' + tag3 + ' }}. Тип {{ ' + tag4 + ' }}{% ' + tag5 + ' %}')
    subsubsection_bin.style = 'ДОК Заголовок 3'
    tag2 =f'{type}.name'
    par_inputs = doc.add_paragraph('{{ '+ tag2 +' }}')
    par_inputs.style = 'ДОК Таблица Название'
    add_table_settings(doc, type)

    end_for = doc.add_paragraph('{% endfor %}{% endfor %}')
    end_for.style = 'TAGS'

    return doc