# multiple-range-merging
Simple project which merges three geological data tables, by range to range correlation. Goal is to impute stratigraphical division 
to mud symptoms and core measurements. 

.csv ARE DELETED DUE TO POTENTIAL ONWERSHIP CONSEQUENCES !! Description below should answer any queastions about data order.

MYUWI is the key. 

stratigraphy:
contains 'STRATIGRAPHY_SYM' and 'LITHOLOGY' associated with 'TOP', 'BOTTOM' range.

lab_data(core measurements):
contains 'MYUWI', 'POROSITY', 'PERMEABILITY', 'BITUMINS_EXTRACT', associated with 'DEPTH' value.

symptoms:
contains 'MYUWI', 'SYMPTOMS', 'GROUP', 'TYPE' associated with , 'START', 'STOP' depth range.



