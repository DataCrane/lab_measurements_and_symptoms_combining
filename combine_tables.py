import pandas as pd

# read datasets
stratigraphy = pd.read_csv('stratigraphy.csv', na_values=-999.25)
lab_data = pd.read_csv('lab_data.csv', na_values=-999.25).drop(['TOP', 'BOTTOM'], axis=1)

# symptoms = pd.read_csv('symptoms.csv')
# print(symptoms.head())

# merge dataframes do df
df = lab_data.merge(stratigraphy, how='left', on=['MYUWI'])

# filter by range
lab_list=list(lab_data.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']
df = df[(df.DEPTH >= df.TOP) & (df.DEPTH <= df.BOTTOM)][lab_list].reset_index(drop=True)

# write to xlsx
writer = pd.ExcelWriter('merged lab_str.xlsx')
df.to_excel(writer,'merged lab_str')
writer.save()


