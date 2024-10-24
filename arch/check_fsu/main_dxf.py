import ezdxf
import pandas as pd
import os

def extract_text_from_dxf(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    mtext = []
    for entity in doc.modelspace():
        if entity.dxftype() == 'MTEXT':
            mtext.append(entity.plain_text())
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(mtext))
    
    # Создание DataFrame
    df = pd.DataFrame(mtext, columns=['Строка'])
    df['Число повторений'] = df.groupby('Строка')['Строка'].transform('count')
    df = df.drop_duplicates()
    df.to_excel('dxf.xlsx', index=False)

if os.path.isfile('1.dxf'):
    # Пример использования
    input_file = '1.dxf'
    output_file = 'dxf.txt'
    extract_text_from_dxf(input_file, output_file)

