
import logging

from __dicts import list_SYS_LNs, list_PROT_LNs

def _extract_iec_ln(str):
    str = str.split('_')[0]
    last_five = str[-5:]
    if 'LLN0' in last_five:
        return 'LLN0'
    else:
        return last_five[:4]

def prepare_df(df): # на вход датафрейм - на выходе список датафреймов
    logging.info('Поготовка датафреймов...')
    df['Group'] = 'NODATA'
    for index, row in df.iterrows():
        iec_ln = _extract_iec_ln(row['Name GEB'])
        if iec_ln in list_SYS_LNs:
            df.at[index, 'Group'] = 'SYS'
        if iec_ln in list_PROT_LNs:
            df.at[index, 'Group'] = 'PROT'
    #df.to_excel('out2.xlsx', index=False)
    # разбиваем датафрейм на список датафреймов по значению столбца Group

    # Группировка DataFrame по столбцу 'Group'
    grouped = df.groupby('Group')
    # Помещение поддатафреймов в список
    sub_df_list = [group for _, group in grouped]
    return sub_df_list 