'''
excel图书库转为obsidian md格式
'''
import pandas as pd
import markdown

if __name__ == '__main__':
    excel_path = '/Users/rod/Downloads/体验清单.xlsx'
    df = pd.read_excel("/Users/rod/Downloads/体验清单.xlsx", sheet_name='书籍')
    for index, row in df.iterrows():
        print(row)
