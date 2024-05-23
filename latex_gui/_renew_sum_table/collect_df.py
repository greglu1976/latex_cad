import os

import pandas as pd

from logger import logger


def collect_df(list_of_tuples):
    for work_tuple in list_of_tuples:
        path_to = work_tuple[0]
        funcs = work_tuple[1]
        full_path = path_to+'/_xlsx/funcs/'
        for func in funcs:
            t = full_path+func+'.xlsx'
            if os.path.isfile(t):
                print('OK>',t)
                #df = pd.read_excel('имя_файла.xlsx', sheet_name='Sheet1')
        pass