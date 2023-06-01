import os
import pandas as pd

def remove_files():
    h5_dir = os.listdir('FEATURES_DIRECTORY/tumor_vs_normal_resnet_features/h5_files')
    pt_dir = os.listdir('FEATURES_DIRECTORY/tumor_vs_normal_resnet_features/pt_files')

    slides = pd.read_csv('dataset_csv/tumor_subtyping.csv')

    for h5, pt in zip(h5_dir, pt_dir):
        if h5.split('.h5')[0] in slides['slide_id'].values and pt.split('.pt')[0] in slides['slide_id'].values:
            pass
        else:
            os.remove(os.path.join('FEATURES_DIRECTORY/tumor_vs_normal_resnet_features/h5_files', h5))
            os.remove(os.path.join('FEATURES_DIRECTORY/tumor_vs_normal_resnet_features/pt_files', pt))
    
    print('removed')
