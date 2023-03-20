import pandas as pd
from pathlib import Path
import glob

data_dir = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')

dirs=[]
for x in data_dir.iterdir():
    if (x.is_dir()) & (len(x.name) < 4):
        dirs.append(x)

for dir in dirs:
    #if (dir.name == 'P8') or (dir.name == 'P14'):#
    #    continue
    for file in glob.glob(str(dir/'MVNX'/'*.xlsx')):
        com = pd.read_excel(file, sheet_name='Center of Mass', index_col=0)
        com.to_csv(file[:-5] + '_com.csv')





a=2