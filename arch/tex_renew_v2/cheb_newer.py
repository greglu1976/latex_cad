import pandas as pd

from get_df_info import get_ln_info
from get_strs import get_strs_from_df

xl_name = '1.xlsx'
requested_lntype = 'LVZSPTOC'

# header=1 потому что заголовки со второй строчки начинаются, первая строчка пустая
df = pd.read_excel(xl_name, index_col=None, sheet_name='Settings', header=1)

#print(df)

df_list = []

grouped = df.groupby('NodeName (рус)')
# Итерируемся по уникальным значениям 'Значение' и создаем датафреймы для каждой группы
for value, group in grouped:
    df_list.append(group)


# Вывод инфо по каждому из датафреймов
for df_group in df_list:
    # Получаем значение в столбце 'Значение' из первой строки датафрейма
    #column_value = df_group['NodeName (рус)'].iloc[0]
    # Создаем имя файла на основе значения столбца 'Значение'
    #file_name = f"{column_value}.xlsx"
    # Сохраняем каждый датафрейм в отдельный Excel файл
    #df_group.to_excel(file_name, index=False)
    print(get_ln_info(df_group))

# Проход по списку функций для поиска нужной
for df_group in df_list:
    if get_ln_info(df_group)[0] == requested_lntype:
        get_strs_from_df(df_group)