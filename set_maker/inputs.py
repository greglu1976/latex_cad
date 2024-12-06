from models.BinInput import BinInput

properties = {
    'Status': {
        'description': 'Статус ДВ',
        'name_in_software': 'Статус',
        'name_in_fsu': '-',
        'value_range': '0 = Не активен\n 1 = Активен',
        'unit': '-',
        'step': '-',
        'default_value': '0',
        'setpoint': '',
    },
    'Mode': {
        'description': 'Режим работы ДВ',
        'name_in_software': 'Режим',
        'name_in_fsu': '-',
        'value_range': '0 = Не активен\n 1 = Активен',
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
        'value_range': '0 = Не предусмотрено\n 1 = Предусмотрено',
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

input1 = BinInput(properties)
input2 = BinInput(properties)
input3 = BinInput(properties)
input4 = BinInput(properties)