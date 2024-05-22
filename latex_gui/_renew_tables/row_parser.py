from .include_tex import dict_default

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
        #res_list.append(result_psd) # здесь включение без строк 1 - ххххх, 0 - и т.д. просто строка обозначающая значение
        result = result.replace("\n", "") # строка 1 для вывода в виде 0 = Недоступно и пр.
        res_list.append(result.replace("-", "=")) # строка 2 для вывода в виде 0 = Недоступно и пр.

    ret_str = ''
    for res in res_list:
        #ret_str += res + r'/\\' # собираем со слешем
        ret_str += res + r'\\' # собираем без слеша
    #ret_str = ret_str[:-3] # собираем со слешем
    ret_str = ret_str[:-2] # собираем без слеша
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

    #if units == 'мс' and max_value>1000: # с контролем диапазона от 0 до 1000 мс не преобразовывать
    if units == 'мс':  # без контроля диапазона от 0 до 1000 мс - все преобразум
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