import pandas as pd

from logger import logger
from .include_tex import long_table_header, long_table_header_desc
from .row_parser import parse_row
from .include_tex import dict_func

def parse_to_tex(paths):
    print(paths)
    tex_list = []
    #tex_list.append('\\fontsize{10pt}{11pt}\selectfont')
    #tex_list.append('')
    # ищем БУ LLN0 для начальной инициализации переменных
    
    df_info = pd.DataFrame()
    for path in paths:
        if path[1] == 'LLN0':
            df_info = pd.read_excel(path[0]+path[1]+path[2], sheet_name='Info')
            df_LLN0 = pd.read_excel(path[0]+path[1]+path[2], sheet_name='Signals')
            break
    IEC61850Name = '*empty*'
    RussianName = '*empty*'
    if df_info.empty:
        logger.warning("Нет LLN0 в составе функционального блока")
    else:
        for index, row in df_info.iterrows():
            if row['Parameter'] == 'RussianName':
                RussianName = row['Value']
            if row['Parameter'] == 'IEC61850Name':
                IEC61850Name = row['Value']  
    # Начинаем собирать tex файл
    desc_func = dict_func.get(RussianName,'')
    tex_list.append('\color{uniblue}{\section {' + f'{RussianName} {desc_func}' +'}}')
    tex_list.append('\color{black}')
    df_LLN0 = df_LLN0.drop(df_LLN0[df_LLN0['Категория (group)'] != 'setting'].index)
    if not df_LLN0.empty:
        
        tex_list.append(long_table_header_desc)
        tex_list.append('\caption{Общие параметры для настройки функционального блока '+'\\textbf{'+f'{RussianName}'+'}\hfill\\vspace{-0.5\\baselineskip}}' + r'\\')
        tex_list +=long_table_header

        count = 1
        isInfo = False
        for index, row in df_LLN0.iterrows():
            row_parsed, isInfoStr = parse_row(row)
            tex_list.append('\centering ' + str(count) + ' & \centering ' + row_parsed[0] + ' & \centering ' + row_parsed[1] + ' & \centering ' + row_parsed[2] + '& \centering ' + row_parsed[3] +  '& \centering '  + row_parsed[4] + ' & \centering ' + row_parsed[5]+ ' & \centering\\arraybackslash' +  r' \\')
            #tex_list.append('\centering ' + str(count) + ' & \centering ' + row['ShortDescription'] + ' & \centering T1 & \centering 0 ... 30 & \centering мс  & \centering с & \centering 0,01 & \centering\\arraybackslash' +  r' \\')
            tex_list.append('\hline')
            count +=1
            if isInfoStr:
                isInfo = True
        if isInfo:
            tex_list.append("\\multicolumn{8}{|l|}{" + "* - Для устройств с номинальным током 1 А (5 А)"  + "} \\\\"+"\n")

        tex_list.append('\end{longtable}')

    for path in paths:
        if path[1] != 'LLN0':
            df = pd.read_excel(path[0]+path[1]+path[2], sheet_name='Signals')
            df = df.drop(df[df['Категория (group)'] != 'setting'].index)
            if df.empty:
                continue
            tex_list.append(long_table_header_desc)
            tex_list.append('\caption{Параметры для настройки функции '+'\\textbf{'+f'{df.iloc[0, 1]}'+'}\hfill\\vspace{-0.5\\baselineskip}}' + r'\\')
            tex_list +=long_table_header 

            count = 1
            isInfo = False
            for index, row in df.iterrows():
                row_parsed, isInfoStr = parse_row(row)
                tex_list.append('\centering ' + str(count) + ' & \centering ' + row_parsed[0] + ' & \centering ' + row_parsed[1] + ' & \centering ' + row_parsed[2] + '& \centering ' + row_parsed[3] +  '& \centering '  + row_parsed[4] + ' & \centering ' + row_parsed[5]+ ' & \centering\\arraybackslash' +  r' \\')
                tex_list.append('\hline')
                count +=1
                if isInfoStr:
                    isInfo = True
            #print(df)
            if isInfo:
                tex_list.append("\\multicolumn{8}{|l|}{" + "* - Для устройств с номинальным током 1 А (5 А)"  + "} \\\\"+"\n")            
            tex_list.append('\end{longtable}')


    return tex_list


