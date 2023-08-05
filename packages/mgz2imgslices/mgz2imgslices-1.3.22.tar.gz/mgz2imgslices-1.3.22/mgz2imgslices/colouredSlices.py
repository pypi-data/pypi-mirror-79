import nibabel as nib
import numpy as np
import pandas as pd
from PIL import Image
import re

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

mgz_vol = nib.load("/home/arushi/devel/mgz_converter_dataset/100307/aparc.a2009s+aseg.mgz")
np_mgz_vol = mgz_vol.get_fdata()

unique, counts = np.unique(np_mgz_vol, return_counts=True)
labels = dict(zip(unique, counts))

for item in labels:
    i_total_slices = np_mgz_vol.shape[0]

    for current_slice in range(0, i_total_slices):
        np_data = np_mgz_vol[:, :, current_slice]

        # prevents lossy conversion
        np_data=np_data.astype(np.uint8)

        df_colorLUT = readFSColorLUT("FreeSurferColorLUT.txt")
        df_rgba = df_colorLUT.loc[df_colorLUT["#No"] == "6070", ("R", "G", "B", "A")]
        # np_data = [df_rgba.iloc[0][0], df_rgba.iloc[0][1], df_rgba.iloc[0][2], df_rgba.iloc[0][3]]
        
        img = Image.fromarray(np_data)
        image_name = "testrgba" + str(current_slice) + ".png"
        img.save(image_name)