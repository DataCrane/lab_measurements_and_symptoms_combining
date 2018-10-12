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


### DRILLING SYMPTOMS AND LAB MEASUREMENTS MERGING ###

# merge dataframes on MYUWI (wellnames)
df2 = symptoms.merge(lab_data, how='left', on=['MYUWI'])

# filter by range
columns_list2= list(symptoms.columns.values) + list(lab_data.drop(['MYUWI'], axis=1).columns.values)
df2 = df2[(df2.DEPTH >= df2.START) & (df2.DEPTH <= df2.STOP)][columns_list2].reset_index(drop=True)


### DRILLING SYMPTOMS, LAB MEASUREMENTS AND STRATIGRAPHY MERGING ###
# merge dataframes on MYUWI (wellnames)
Rdf = df2.merge(stratigraphy, how='left', on=['MYUWI'])

# filter by range
columns_list3= list(df2.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']
Rdf = Rdf[(Rdf.DEPTH >= Rdf.TOP) & (Rdf.DEPTH <= Rdf.BOTTOM)][columns_list3].reset_index(drop=True)


# write to .xlsx
writer = pd.ExcelWriter('result2.xlsx')
Rdf.to_excel(writer,'result2')
writer.save()


