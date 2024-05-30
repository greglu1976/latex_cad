import pandas as pd

from prepare_df import prepare_df
from process_df import get_dfs
from analize_dfs import analize_dfs

def get_df():
    # в составе эксела есть особый лист controls где есть сигналы оперативного управления
    # на данный момент включаемые сигналы указываются символом * в столбце Note
    # выставляется ВРУЧНУЮ перед обработкой файла
    df_0 = pd.read_excel('1.xlsx', sheet_name='Controls', header=1)
    df_0['Категория (group)'] = df_0['Категория (group)'].replace('measurement', 'control')
    df_0 = df_0[df_0["Note (Справочная информация)"] == '*']
    df_0["NodeName (рус)"] = 'control'
    df_0["61850_DataObjectName"] = 'control.control'
    #df_0.to_excel('./out/df0.xlsx', index=False)

    # Считывание данных из файла Excel в DataFrame
    df_1 = pd.read_excel('1.xlsx', sheet_name='Status information', header=1)
    df_2 = pd.read_excel('1.xlsx', sheet_name='Settings', header=1)
    df = pd.concat([df_1, df_2], ignore_index=True)
    df = pd.concat([df, df_0], ignore_index=True)

    # Подготовим DataFrame

    empty_node_names = df[df["NodeName (рус)"].isna()]["NodeName (рус)"].index
    for idx in empty_node_names:
        if "LLN0" in df.loc[idx, "61850_TypeLN"]:
            df.loc[idx, "NodeName (рус)"] = "БУ"
            obj = df.loc[idx, "61850_DataObjectName"]
            df.loc[idx, "61850_DataObjectName"] = "LLN0." + obj

    df = df.fillna(value='-')
    df.drop(df.columns[50], axis=1, inplace=True)
    df.drop(columns=['Уровень доступа на запись, не менее (authLevel)'], inplace=True)
    df.drop(columns=['№'], inplace=True)
    df.drop(columns=['Длина'], inplace=True)   
    df.drop(columns=['ShortDescription (лимит длины)'], inplace=True)
    df.drop(columns=['Name GEB'], inplace=True)
    df.drop(columns=['Примечание'], inplace=True)
    df.drop(columns=['read-only UNITService'], inplace=True)
    df.drop(columns=['Command UNITService'], inplace=True)
    df.drop(columns=['maxSize'], inplace=True)
    df.drop(columns=['ConvertingFlag'], inplace=True)
    df.drop(columns=['ConvertingBasis'], inplace=True) 
    df.drop(columns=['multiplayer'], inplace=True)
    df.drop(columns=['TransfCoef'], inplace=True) 
    df.drop(columns=['Значение в архиве'], inplace=True) 
    df.drop(columns=['103_ASDU_read'], inplace=True)
    df.drop(columns=['103_ASDU_write'], inplace=True) 
    df.drop(columns=['103_GI'], inplace=True) 
    df.drop(columns=['103_InformationInstanceNumber'], inplace=True)
    df.drop(columns=['103_FUN'], inplace=True)
    df.drop(columns=['103_INF'], inplace=True) 
    df.drop(columns=['103_INF_InstShift'], inplace=True)
    df.drop(columns=['MappingMask'], inplace=True) 
    df.drop(columns=['Extension_enum'], inplace=True)
    df.drop(columns=['Extension_enum_HMI'], inplace=True)
    df.drop(columns=['Функция чтение1'], inplace=True) 
    df.drop(columns=['Адрес регистра 1 DEC(слово)'], inplace=True)
    df.drop(columns=['Адрес регистра 1 HEX (слово)'], inplace=True)
    df.drop(columns=['Адрес регистра 2 DEC (бит)'], inplace=True) 
    df.drop(columns=['Адрес регистра 2 HEX (бит)'], inplace=True)
    df.drop(columns=['Функция запись'], inplace=True)
    df.drop(columns=['Регистр на запись HEX'], inplace=True)
    df.drop(columns=['EventReg'], inplace=True)
    df.drop(columns=['OperEventReg'], inplace=True)
    df.drop(columns=['61850_Reference'], inplace=True)
    #df.drop(columns=['61850_DataObjectName'], inplace=True)

    df['Категория (group)'] = df['Категория (group)'].replace('measurement', 'status')

    df = df.sort_values(by=["NodeName (рус)"], ascending=True)

    ##########################################################################
    ### подготовим датафрейм - распарсим столбец 61850_DataObjectName на два столбца
    df = prepare_df(df)

    ##########################################################################
    ### вытаскиваем набор приведенных датасетов
    dfs = get_dfs(df)
    ##########################################################################

    ##########################################################################
    #### анализируем состав датасетов на наличие однотипных узлов
    analize_dfs(dfs)  
    #print(len(dfs))

    return df