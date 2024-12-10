# Добавляет в конец документа раздел с дискретными вх/вых

from tables import add_table_settings, add_table_reg

def add_sect_binaries(doc, name_sect, type):

    tag1 = f'for {type}s_key, {type}s in {type}s.modules.items()'


        # Создаем подраздел
    subsection_bin = doc.add_paragraph(f'{name_sect} '+ '{% ' + tag1 + ' %}')
    subsection_bin.style = 'ДОК Заголовок 2'

        # Создаем подраздел с тегами
    tag3 = f'{type}s.inserted_in_slot'
    tag4 = f'{type}s.type'
    tag5 = f'for {type}_key, {type} in {type}s.inputs.items()'
    if not 'rza' in type:    
        subsubsection_bin = doc.add_paragraph('Слот {{ ' + tag3 + ' }}. Тип {{ ' + tag4 + ' }}{% ' + tag5 + ' %}')
    else:
        #subsubsection_bin = doc.add_paragraph('{% ' + tag4 + ' %}')
        subsubsection_bin = doc.add_paragraph('{{ ' + tag4 + ' }}{% ' + tag5 + ' %}')
    
    subsubsection_bin.style = 'ДОК Заголовок 3'
    tag2 =f'{type}.name'
    par_inputs = doc.add_paragraph('{{ '+ tag2 +' }}')
    par_inputs.style = 'ДОК Таблица Название'
    add_table_settings(doc, type)

    end_for = doc.add_paragraph('{% endfor %}{% endfor %}')
    end_for.style = 'TAGS'

    return doc

def add_sect_reg(doc):

    text1 = doc.add_paragraph('Возможна регистрация не более 200 сигналов. {% for regs_key, regs in regs.inputs.items() %}')
    text1.style = 'ДОК Текст'

    par_inputs = doc.add_paragraph('{{ regs.name }}')
    par_inputs.style = 'ДОК Таблица Название'

    add_table_reg(doc)

    end_for = doc.add_paragraph('{% endfor %}')
    end_for.style = 'TAGS'

    return doc

