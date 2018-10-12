import pandas as pd

### LAB MEASUREMENTS AND STRATIGRAPHY MERGING ###
# read datasets
stratigraphy = pd.read_csv('stratigraphy.csv', na_values=-999.25)
lab_data = pd.read_csv('lab_data.csv', na_values=-999.25).drop(['TOP', 'BOTTOM'], axis=1)
symptoms = pd.read_csv('symptoms.csv')

# merge dataframes on MYUWI (well names)
df = lab_data.merge(stratigraphy, how='left', on=['MYUWI'])

# filter by range
columns_list= list(lab_data.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']
df = df[(df.DEPTH >= df.TOP) & (df.DEPTH <= df.BOTTOM)][columns_list].reset_index(drop=True)

# # write to xlsx
# writer = pd.ExcelWriter('merged lab_str.xlsx')
# df.to_excel(writer,'merged lab_str')
# writer.save()

### DRILLING SYMPTOMS AND STRATIGRAPHY MERGING ###

# merge dataframes on MYUWI (wellnames)
df2 = symptoms.merge(stratigraphy, how='left', on=['MYUWI'])

# filter by range
columns_list2= list(symptoms.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']

df2 = df2[((df2.START >= df2.TOP)
           & (df2.STOP >= df2.TOP)
           & (df2.START <= df2.BOTTOM)
           & (df2.STOP <=df2.BOTTOM))
          | ((df2.START <= df2.BOTTOM) & (df2.STOP >= df2.TOP))][columns_list2].reset_index(drop=True)


# write to xlsx
writer = pd.ExcelWriter('test.xlsx')
df2.to_excel(writer,'test')
writer.save()


