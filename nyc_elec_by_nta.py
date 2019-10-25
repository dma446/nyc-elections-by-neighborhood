from collections import defaultdict
import csv
import json
import pandas as pd
import re
import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    print("Please add a csv file name.")

with open('ntas/nta_eds.txt') as json_file:
    nta_list = json.load(json_file)

nta_data = defaultdict(lambda: defaultdict(int))

with open(file_name) as csv_file:
    elec_csv = csv.DictReader(csv_file)
    for row in elec_csv:
        ed = row['AD'] + (3 - len(row['ED'])) * '0' + row['ED']
        for n in nta_list:
            if ed in nta_list[n]:
                candidate = row['Unit Name']
                votes = int(row['Tally'].replace(',', ''))
                nta_data[n][candidate] += votes

cols = ['Neighborhood']
results = []

for n in nta_data:
    for c in nta_data[n]:
        cols.append(c)
    break

for n in nta_data:
    row = []
    row.append(n)
    for c in nta_data[n]:
        row.append(nta_data[n][c])
    results.append(row)

df = pd.DataFrame(results, columns=cols)

remove_cols = ['Public Counter','Emergency','Manually Counted Emergency','Absentee/Military','Absentee / Military','Federal','Special Presidential','Affidavit','Scattered']

for col in remove_cols:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

candidates = list(df.columns)
candidates.remove('Neighborhood')

#Removes multiple ballot lines
unique_cand = []
for vote1 in candidates:
    largest_vote = vote1
    for vote2 in candidates:
        if largest_vote.split('(')[0] == vote2.split('(')[0]:
            tot1 = df[largest_vote].sum()
            tot2 = df[vote2].sum()
            largest_vote = largest_vote if max(tot1, tot2) == tot1 else vote2
    unique_cand.append(largest_vote)

for col in df.columns:
    if col in unique_cand:
        for cand in candidates:
            if col.split('(')[0] == cand.split('(')[0] and cand not in unique_cand: 
                df[col] += df[cand] 

df = df.drop([cand for cand in candidates if cand not in unique_cand], axis=1)
df.to_csv(file_name.replace('.csv', '_by_nta.csv'), index=False, encoding='utf-8')
