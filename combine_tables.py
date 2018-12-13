import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
import numpy as np

### LAB MEASUREMENTS AND STRATIGRAPHY MERGING ###
# read datasets
stratigraphy = pd.read_csv('stratigraphy.csv', na_values=-999.25)
lab_data = pd.read_csv('lab_data.csv', na_values=-999.25).drop(['TOP', 'BOTTOM'], axis=1)
symptoms = pd.read_csv('symptoms.csv')

# merge dataframes on MYUWI (well names)
df = lab_data.merge(stratigraphy, how='left', on=['MYUWI'])

# filter by range
columns_list = list(lab_data.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']
df = df[(df.DEPTH >= df.TOP) & (df.DEPTH <= df.BOTTOM)][columns_list].reset_index(drop=True)


### DRILLING SYMPTOMS AND LAB MEASUREMENTS MERGING

# merge dataframes on MYUWI (wellnames)
df2 = symptoms.merge(lab_data, how='left', on=['MYUWI'])

# filter by range
columns_list2 = list(symptoms.columns.values) + list(lab_data.drop(['MYUWI'], axis=1).columns.values)
df2 = df2[(df2.DEPTH >= df2.START) & (df2.DEPTH <= df2.STOP)][columns_list2].reset_index(drop=True)


### DRILLING SYMPTOMS, LAB MEASUREMENTS AND STRATIGRAPHY MERGING
# merge dataframes on MYUWI (wellnames)
Rdf = df2.merge(stratigraphy, how='left', on=['MYUWI'])

# filter by range
columns_list3 = list(df2.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']
Rdf = Rdf[(Rdf.DEPTH >= Rdf.TOP) & (Rdf.DEPTH <= Rdf.BOTTOM)][columns_list3].reset_index(drop=True)


# # write to .xlsx
# writer = pd.ExcelWriter('result2.xlsx')
# Rdf.to_excel(writer,'result2')
# writer.save()

# # # If you want to connect symptoms and stratigraphy directly, use this set of conditions:
# filter by range:
# columns_list2 = list(symptoms.columns.values) + ['STRATIGRAPHY_SYM', 'LITHOLOGY']
# df2 = df2[((df2.START >= df2.TOP)
#            & (df2.STOP >= df2.TOP)
#            & (df2.START <= df2.BOTTOM)
#            & (df2.STOP <= df2.BOTTOM))
#           | ((df2.START <= df2.BOTTOM) & (df2.STOP >= df2.TOP))][columns_list2].reset_index(drop=True)


### What is the samples frequency per MYUWI(well id) and STRATIGRAPHY_SYM ? ? ?
sample_count = (Rdf
                .groupby(['MYUWI', 'STRATIGRAPHY_SYM'])
                # .n.count().sort_values(ascending=False)
                ['POROSITY','PERMEABILITY', 'BITUMINS_EXTRACT'].count()
                )


### prepare plot
barchart = sample_count.plot.bar()


barchart.set_title("samples frequency", fontsize=18)
# barchart.set_yscale("log", nonposy='clip')
# y_t = np.arange(0, 900, 100).tolist() # optional
barchart.set_ylabel("count", fontsize=18)
# barchart.set_yticks(y_t)

def labels(chart=None):
    # create a list to collect the plot.patches data
    totals = []

    # find the values and append to list
    for i in chart.patches:
        totals.append(i.get_height())

    # set individual bar labels using above list
    total = sum(totals)

    # set individual bar labels using above list
    for i in chart.patches:
        # get_x pulls left or right; get_height pushes up or down
        chart.text(i.get_x(), i.get_height(), \
                # str(round((i.get_height()/total)*100, 2))+'%', fontsize=15, # PERCENT
                str(round(i.get_height(), 2)),  va='center', fontsize=6, color='black')
    plot.show()

labels(chart=barchart)



### What is the median PERMEABILITY and BIT_EXTR. per MYUWI(well id) and STRATIGRAPHY_SYM ? ? ?
median_PERM_BIT = (Rdf
                   .groupby(['MYUWI', 'STRATIGRAPHY_SYM'])
                   ['PERMEABILITY', 'BITUMINS_EXTRACT'].median()
                   )

### prepare plot
barchart2 = median_PERM_BIT.plot.bar()
barchart2.set_title("median PERMEABILITY and BITUMINS", fontsize=18)
barchart2.set_yscale("log", nonposy='clip')
# y_t = np.arange(0, 900, 100).tolist() # optional
barchart2.set_ylabel("", fontsize=18)
# barchart.set_yticks(y_t)

# create labels
labels(barchart2)



### What is the median POROSITY per MYUWI(well id) and STRATIGRAPHY_SYM ? ? ?
median_POR = (Rdf
              .groupby(['MYUWI', 'STRATIGRAPHY_SYM'])
              ['POROSITY'].median()
              )

### prepare plot
barchart3 = median_POR.plot.bar()
barchart3.set_title("median POROSITY", fontsize=18)
# barchart2.set_yscale("log", nonposy='clip')
# y_t = np.arange(0, 900, 100).tolist() # optional
barchart3.set_ylabel("", fontsize=18)
# barchart.set_yticks(y_t)

# create labels
labels(barchart3)

# Is porosity and permeability correlated with bitumins volume ?
Ca2_set = Rdf[Rdf.STRATIGRAPHY_SYM.isin(['Ca2'])]
cor_col = ['POROSITY', 'PERMEABILITY', 'BITUMINS_EXTRACT']

#scatterplot
sns.set()
cols = cor_col
sns.pairplot(Ca2_set[cor_col], size = 2.5)
plot.show()
# COMMENT: Just POROSITY vs BITUMINS_EXTRACT seems to have correlation.
# Let's have a closer look on this.

# POROSITY vs BITUMINS_EXTRACT across boreholes

#bivariate analysis BITUMINS_EXTRACT/POROSITY
def bivariate_bit_por(borehole=None, title=None):
    Ca2_set = Rdf[Rdf.STRATIGRAPHY_SYM.isin(['Ca2']) & Rdf.MYUWI.isin([borehole])]
    var = 'BITUMINS_EXTRACT'
    data = pd.concat([Ca2_set['POROSITY'], Ca2_set[var]], axis=1)
    scatterplot = data.plot.scatter(y=var, x='POROSITY')#, ylim=(0,800000));
    scatterplot.set_title(title, fontsize=18)
    plot.show()

#bivariate analysis across 3 most common boreholes (MY3, MY58, MY84)
bivariate_bit_por('MY3', "MY3, CA2")
bivariate_bit_por('MY58', "MY58, CA2")
bivariate_bit_por('MY84', "MY84, CA2")

