import os
import re
import csv
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Configurations for label creation')
parser.add_argument('--task', type=str, default='task_1_tumor_vs_normal',
                    help='tasks')
args = parser.parse_args()

def select_dataset(path):
    tcga_list = []
    with open('list.txt', 'w') as file:
        for tcga_wsi in os.listdir(path):
            barcode_identifier = tcga_wsi.split("-")
            if len(barcode_identifier) > 4 and not re.search(r'(BS|TS)', barcode_identifier[5]):
                file.write(tcga_wsi + '\n')
                tcga_list.append(tcga_wsi)

    os.system('mv list.txt dataset_csv')
    return tcga_list


def create_csv_for_train(tcga_list):
    clinical_data=pd.read_csv('dataset_csv/prad_tcga_clinical_data.tsv', sep='\t')
    t2_list = ['T2','T2a', 'T2b', 'T2c']
    t3_list = ['T3','T3a', 'T3b', 'T3c']

    if args.task == 'task_2_tumor_subtyping':
        with open('tumor_subtyping.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["case_id", "slide_id", "label"])

            for tcga_wsi in tcga_list:
                barcode_identifier = tcga_wsi.split("-")
                if len(barcode_identifier) > 4:
                    label = clinical_data.loc[clinical_data['Patient ID'] == '-'.join(barcode_identifier[:3]), 'Person Neoplasm Status'].iloc[0]
                    label_tumor = clinical_data.loc[clinical_data['Patient ID'] == '-'.join(barcode_identifier[:3]), 'American Joint Committee on Cancer Tumor Stage Code'].iloc[0]
                    if label == 'WITH TUMOR':
                        if label_tumor in t2_list:
                            writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], 'stage_2'])
                        elif label_tumor in t3_list:
                            writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], 'stage_3'])
                        else:
                            pass
                    else:
                        pass
        
        os.system('mv tumor_subtyping.csv dataset_csv')
    
    elif args.task == 'task_1_tumor_vs_normal':
        with open('tumor_vs_normal.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["case_id", "slide_id", "label"])

            for tcga_wsi in tcga_list:
                barcode_identifier = tcga_wsi.split("-")
                if len(barcode_identifier) > 4:
                    label = clinical_data.loc[clinical_data['Patient ID'] == '-'.join(barcode_identifier[:3]), 'Person Neoplasm Status'].iloc[0]
                    if label == 'TUMOR FREE':
                        writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], 'normal_tissue'])
                    elif label == 'WITH TUMOR':
                        writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], 'tumor_tissue'])
                    else:
                        pass
        
        os.system('mv tumor_vs_normal.csv dataset_csv')
    
    else:
        raise NotImplementedError


def move_folders(path):
    for folder in os.listdir(path):
        if len(folder.split("-")) == 5:
            os.system(f'mv {os.path.join(path, folder)} prostate_data')
        else:
            continue

tcga_list = select_dataset("/data/prostate_data")
create_csv_for_train(tcga_list)
