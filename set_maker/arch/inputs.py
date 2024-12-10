from models.BinInput import BinInput

properties = {
    'Status': {
        'description': 'Статус ДВ',
        'name_in_software': 'Статус',
        'name_in_fsu': '-',
        'value_range': '0 = Не активен\n1 = Активен',
        'unit': '-',
        'step': '-',
        'default_value': '0',
        'setpoint': '',
    },
    'Mode': {
        'description': 'Режим работы ДВ',
        'name_in_software': 'Режим',
        'name_in_fsu': '-',
        'value_range': '0 = Не активен\n1 = Активен',
        'unit': '-',
        'step': '-',
        'default_value': '0',
        'setpoint': '',
    },
    'Filtr_Time': {
        'description': 'Время фильтрации ДВ',
        'name_in_software': 'Время фильтрации',
        'name_in_fsu': '-',
        'value_range': '0...20',
        'unit': 'мс',
        'step': '1',
        'default_value': '20',
        'setpoint': '',
    },
        'Inversion': {
        'description': 'Режим инверсии ДВ',
        'name_in_software': 'Инверсия',
        'name_in_fsu': '-',
        'value_range': '0 = Не предусмотрено\n1 = Предусмотрено',
        'unit': '-',
        'step': '-',
        'default_value': '0',
        'setpoint': '',
    },
        'Appointment': {
        'description': 'Назначение ДВ',
        'name_in_software': 'Описание',
        'name_in_fsu': '-',
        'value_range': '0...31',
        'unit': 'Символ',
        'step': '-',
        'default_value': '',
        'setpoint': '',
    },      
}

input1 = BinInput(properties, 'Дискретный вход 1')
input2 = BinInput(properties, 'Дискретный вход 2')
input3 = BinInput(properties, 'Дискретный вход 3')
input4 = BinInput(properties, 'Дискретный вход 4')