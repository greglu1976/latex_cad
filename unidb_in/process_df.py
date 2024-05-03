import pandas as pd

from logger import logger

def get_dfs(df):
    
    grouped_df = df.groupby("NodeName (рус)")
    list_of_dfs = [group[1] for group in grouped_df]

    for df in list_of_dfs:
        # Проверьте наличие значений в столбце "TypeLN"
        if df["61850_TypeLN"].notna().any():
            # Если есть значения, проверьте их уникальность
            if len(df["61850_TypeLN"].unique()) == 1:
                # Если все значения одинаковые, оставьте их как есть
                pass
            else:
                val_set=set()
                ln_type = 'error'
                for i in df.index:
                    val=df.loc[i, "61850_TypeLN"]
                    val_set.add(val)
                if "-" in val_set:
                    val_set.remove("-")
                if val_set.__len__()!=1:
                    logger.info(f"Не совпадают типы узлов в пределах одной функции: {val_set}")
                else:
                    ln_type = val_set.pop()

                for i in df.index:
                    if df.loc[i, "61850_TypeLN"]=='-':
                        df.loc[i, "61850_TypeLN"] = ln_type
        else:
            # Если в столбце "TypeLN" нет значений, заполните все ячейки значением "empty"
            df["61850_TypeLN"].fillna("empty", inplace=True)


    return list_of_dfs