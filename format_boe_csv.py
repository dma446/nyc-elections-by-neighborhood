import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])
header = df.columns[0:11]
df.drop(header, axis=1, inplace=True)
df.columns = header
df.to_csv(sys.argv[1].replace('.csv', '_f.csv'), index=None)