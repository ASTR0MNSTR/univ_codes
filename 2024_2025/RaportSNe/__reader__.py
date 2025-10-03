import numpy as np
import pandas as pd
import os

def read_data(path_to_dir, filter):
    df_all = pd.DataFrame()
    for folder in os.listdir(path_to_dir):
        # with open(f'{path_to_dir}\{folder}\{folder}.dat', 'r'): 
        cols = {
            0 : 'num',
            3 : filter,
            4 : filter+'_err',
            7 : 'flag'
        }
        df = pd.read_csv(f'{path_to_dir}\{folder}\{folder}.dat', sep=r'\s+', header=None, engine='python', usecols=cols.keys(), names=cols.values())
        df['data'] = folder
        df['id'] = folder + '_' + df['num'].astype(str)
        
        df_all = pd.concat([df_all, df])
        
    df_all = df_all.reset_index(drop=True)
    df_all.to_csv(rf'E:/progs/fuzzy-chainsaw/2024_2025\RaportSNe/{filter}.csv', index=False)
        
        
# if __name__ == '__main__':
#     read_data(r'E:\progs\fuzzy-chainsaw\2024_2025\Photom\V', 'V_RBT')
#     read_data(r'E:\progs\fuzzy-chainsaw\2024_2025\Photom\dat\dat', 'R_RBT')