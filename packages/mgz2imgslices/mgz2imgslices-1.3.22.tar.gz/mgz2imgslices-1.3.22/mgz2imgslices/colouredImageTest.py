import pandas as pd
import re
import numpy as np

def readFSColorLUT(str_filename):
        l_column_names = ["#No", "LabelName", "R", "G", "B", "A"]

        df_FSColorLUT = pd.DataFrame(columns=l_column_names)

        with open(str_filename) as f:
            for line in f:
                if line and line[0].isdigit():
                    line = re.sub(' +', ' ', line)
                    l_line = line.split(' ')
                    l_labels = l_line[:]
                    df_FSColorLUT.loc[len(df_FSColorLUT)] = l_labels
                    df_FSColorLUT['R'] = df_FSColorLUT['R'].astype(int)
                    df_FSColorLUT['G'] = df_FSColorLUT['G'].astype(int)
                    df_FSColorLUT['B'] = df_FSColorLUT['B'].astype(int)
                    df_FSColorLUT['A'] = df_FSColorLUT['A'].astype(int)                                      
        return df_FSColorLUT

# df = readFSColorLUT('FreeSurferColorLUT.txt')

# print(df.loc[df["#No"] == "6070", ("R", "B", "G", "A")].iloc[0][1])

data1 = np.load("/home/arushi/devel/mgz2imgslices/out/label-002/sample.npy")
data2 = np.load("/home/arushi/devel/mgz2imgslices/out/label-full/sample.npy")
# data3 = np.load("/home/arushi/devel/mgz2imgslices/out/label-full/sample-00200.npy")

print(np.unique(data1))
print(np.unique(data2))
# print(np.unique(data3))