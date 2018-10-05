import pandas as pd
import numpy as np

# from openpyxl.workbook import Workbook

stratigraphy = pd.read_csv('stratigraphy.csv')
# print(stratigraphy.head())

lab_data = pd.read_csv('lab_data.csv')
# print(lab_data.head())

symptoms = pd.read_csv('symptoms.csv')
# print(symptoms.head())

# print(stratigraphy.info())
# print(lab_data.info())

# df1 = pd.merge(stratigraphy, lab_data, how='inner', on='MYUWI', validate='m:m')

a = lab_data.DEPTH.values
bh = stratigraphy.BOTTOM.values
bl = stratigraphy.TOP.values

i, j = np.where((a[:, None] >= bl) & (a[:, None] <= bh))

df1 = pd.DataFrame(
    np.column_stack([lab_data.values[i], stratigraphy.values[j]]),
    columns=lab_data.columns.append(stratigraphy.columns)
    )



writer = pd.ExcelWriter('SHIP 1.xlsx')
df1.to_excel(writer,'SHIP 1')
writer.save()

