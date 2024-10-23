def make_plus(value):
    if value == '0' or value == 0 or value == '':
        return '--'
    else:
        return '+'

def parse_row_new(row):
    full_desc = row['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)']
    short_desc = row['ShortDescription'].replace("_", r"\_")
    node_name = row['NodeName (рус)'].replace("_", r"\_") # экранируем подчеркивание в имени узла
    digital_input = make_plus(row['DigitalInput'])
    digital_output = make_plus(row['DigitalOutput'])
    func_button = make_plus(row['FunctionalButton'])
    led = make_plus(row['LED'])  
    event_log = make_plus(row['Logger'])  
    disturber = make_plus(row['Disturber'])  
    start_disturber = make_plus(row['StartDisturber'])
    russ_name = row['RussianName'].replace("_", r"\_") # экранируем подчеркивание в имени узла
    type = row['type']
    
    return (node_name, full_desc, short_desc, digital_input, digital_output, led, func_button, event_log, disturber, start_disturber, russ_name, type)