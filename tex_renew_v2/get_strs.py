# принимает датафрейм и возвращает список строк
# с необходимыми данными для таблицы типа 1

import pandas as pd


from _dicts import dict_settings


def add_str_custom_header(custom_header, tex_final):

    tex_final.append("\\multicolumn{5}{|c|}{" + custom_header.strip('\n')  + "} \\\\"+"\n")

    tex_final.append("\\hline\n")
    return tex_final

def format_number(num):
    num_str = str(num)
    if '.' in num_str:
        num_str = num_str.rstrip('0').rstrip('.')
        formatted_num = num_str.replace('.', ',')
    else:
        formatted_num = num_str

    return formatted_num


# Промежуточная функция парсинга, подготовка для latex
def handle_str(str):
    if (str==''):
        return '--'
    #print(str)
    if str in dict_settings:
        return dict_settings[str]
    str = str.replace('/', ' \\\\')
    str = str.replace('_', '\\_')
    str = str.replace('%', '\%')
    return str



def get_strs_from_df(df):
    strs = []
    # Заменяем все NaN на пустую строку
    df = df.fillna('')

    for index, row in df.iterrows():
        col_param = (str(row['FullDescription (Описание параметра для пояснения в ПО ЮНИТ Сервис)']) 
        + ' (' + handle_str(str(row['ShortDescription'])) + ')')
        col_obozn = handle_str(str(row['AppliedDescription']))


        # проверяем есть ли мс в единица измерений
        col_ediniz = str(row['units'])
        if str(row['units']) == 'мс':
            col_ediniz = 'с'

        col_step = ''
        minVal = ''
        maxVal = ''
        beetween = ' ... '
        note = str(row['Note (Справочная информация)'])
        if note!='':
            minVal = ''
            maxVal = ''
            beetween = ''
            note = note.replace(',', ' \\\\')
        else:
            if col_ediniz == 'с':
                minVal = format_number(str(row['minValue']/1000))
                maxVal = format_number(str(row['maxValue']/1000))
                col_step = format_number(str(row['step']/1000))
            else:
                minVal = format_number(str(row['minValue']))
                maxVal = format_number(str(row['maxValue']))
                col_step = format_number(str(row['step'])  )             
                
        col_znach = note + minVal + beetween + maxVal

        if col_ediniz == '':
            col_ediniz = '--'
        if col_step == '':
            col_step = '--'
        str2append = "\\centering " + col_param + " & \\centering " + col_obozn + " & \\centering " + col_znach + " & \\centering " + col_ediniz + " & \\centering\\arraybackslash " + col_step + " \\\\"+"\n"
        strs.append(str2append)
        strs.append("\\hline\n")

    return strs
