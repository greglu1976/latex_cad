class BinInput:
    def __init__(self, properties):
        self.properties = properties

    def to_dict(self):
        return self.properties

    #def __str__(self):
        #return "\n".join([f"{key}: {value}" for key, value in self.properties.items()])

    def __str__(self):
        return str(self.to_dict())    


if __name__ == "__main__":
    properties = {
        'Status': {
            'description': 'Статус ДВ',
            'name_in_software': 'Статус',
            'value_range': '0 = Не активен, 1 = Активен',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
        'Mode': {
            'description': 'Режим работы',
            'name_in_software': 'Режим',
            'value_range': '0 = Не активен, 1 = Активен',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
        'Filtr_Time': {
            'description': 'Время фильтрации',
            'name_in_software': 'Время фильтрации',
            'value_range': '0...20',
            'unit': 'мс',
            'step': '1',
            'default_value': '20',
            'setpoint': '',
        },
            'Inversion': {
            'description': 'Режим инверсии ДВ',
            'name_in_software': 'Инверсия',
            'value_range': '0 = Не предусмотрено, 1 = Предусмотрено',
            'unit': '-',
            'step': '-',
            'default_value': '0',
            'setpoint': '',
        },
            'Appointment': {
            'description': 'Назначение ДВ',
            'name_in_software': 'Описание',
            'value_range': '0...31',
            'unit': 'Символ',
            'step': '-',
            'default_value': '-',
            'setpoint': '',
        },      
    }

    input1 = BinInput(properties)
    print(input1.to_dict())