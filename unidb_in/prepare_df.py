import pandas as pd

def prepare_df(df):
    df['Logger'] = 0
    df['Disturber'] = 0
    df['StartDisturber'] = 0    
    df['61850_LN'] = '-'
    df['61850_Attr'] = '-'
    df['reserved1'] = '-'
    df['reserved2'] = '-'

    # Проходим по каждой строке датафрейма
    for index, row in df.iterrows():
        data_object_name = row['61850_DataObjectName']
        
        # Проверяем ячейку на наличие точки и знака '-'
        if '.' in data_object_name:
            parts = data_object_name.split('.')
            df.at[index, '61850_LN'] = parts[0]
            df.at[index, '61850_Attr'] = parts[1]
        elif data_object_name == '-':
            pass  # Ничего не делаем
        else:
            df.at[index, '61850_Attr'] = data_object_name

    df.drop(columns=['61850_DataObjectName'], inplace=True)
    #print(df)
    # Преобразовываем датафрейм в Excel
    #df.to_excel('./out/output.xlsx', index=False)
    return df   