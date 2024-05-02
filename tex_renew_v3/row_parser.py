from include_tex import dict_default

def process_num(num, step):
    decimal_places = len(str(step).split('.')[1])  # Определяем количество знаков после запятой числа step
    formatted_v = '{:.{}f}'.format(num, decimal_places)  # Форматируем число v с заданным количеством знаков после запятой
    formatted_v = formatted_v.replace('.', ',')  # Заменяем символ "." на ","
    return formatted_v  

def parse_note(note, default):
    result_list = note.split(",")
    res_list = []
    str_default = str(default)
    for result in result_list:
        result_psd = result.split("-")[1]
        result_def = str(result.split("-")[0])
        result_def = result_def.strip()
        if str(default).strip()==result_def:
            str_default = result_psd
        res_list.append(result_psd)
    ret_str = ''
    for res in res_list:
        ret_str += res + r'/\\'
    ret_str = ret_str[:-3]
    #print(ret_str)
    return (ret_str, str_default)

def parse_row(row):
    category = row['Категория (group)']
    if category!='setting':
        return ()
    full_desc = row['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)']
    short_desc = row['ShortDescription'].replace("_", r"\_")
    applied_desc = row['AppliedDescription'].replace("_", r"\_")
    units = row['units']
    if units =='%':
        units = '\%'
    min_value =  row['minValue']
    max_value =  row['maxValue']
    step =  row['step']
    default = row['DefaultValue']
    note = row['Note (Справочная информация)']

    if units == 'мс' and max_value>1000:
        max_value = max_value/1000
        min_value = min_value/1000
        step = step/1000
        default = default/1000
        units = 'с'

    if isinstance(step, (int, float)) and step<1:
        max_value = process_num(max_value, step)
        min_value = process_num(min_value, step)
        default = process_num(default, step)
    else:
        max_value = str(max_value).replace('.', ',')  # Заменяем символ "." на ","
        min_value = str(min_value).replace('.', ',')  # Заменяем символ "." на ","
        default = str(default).replace('.', ',')  # Заменяем символ "." на ","
    step = str(step).replace('.', ',')

    if note != '-': # Здесь убираем шаг у программных переключателей 
        step = '-'

    diap = min_value +' ... '+ max_value
    if note !='-':
        t = parse_note(note, default)
        diap = t[0]
        default = t[1]
    default = dict_default.get(default.strip(), default)
    applied_desc = dict_default.get(applied_desc.strip(), applied_desc)

    return (full_desc + ' (' + short_desc +')', applied_desc, diap, units, step, default)