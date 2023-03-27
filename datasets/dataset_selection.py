import os
import re
import csv

def select_dataset(path):
    tcga_list = []
    with open('list.txt', 'w') as file:
        for tcga_wsi in os.listdir(path):
            barcode_identifier = tcga_wsi.split("-")
            if len(barcode_identifier) > 4 and not re.search(r'(BS|TS)', barcode_identifier[5]):
                file.write(tcga_wsi + '\n')
                tcga_list.append(tcga_wsi)

    os.system('mv list.txt datasets')
    return tcga_list


def create_csv_for_train(tcga_list):
    with open('tumor_subtyping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["case_id", "slide_id", "label"])

        for tcga_wsi in tcga_list:
            barcode_identifier = tcga_wsi.split("-")
            if len(barcode_identifier) > 4 and re.search(r'(3Z|6D|A3|AK|AS|B0|B2|B4|B8|BP|CB|CJ|CW|CZ|DV|EU|G6|GK|MM|MW|T7|V8|WM)', barcode_identifier[1]):
                writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], "CCRCC"])
            elif len(barcode_identifier) > 4 and re.search(r'(KL|KM|KN|KO|NP|UW)', barcode_identifier[1]):
                writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], "CRCC"])
            else:
                writer.writerow([barcode_identifier[2], tcga_wsi.split(".svs")[0], "PRCC"])
    
    os.system('mv tumor_subtyping.csv dataset_csv')


def create_link(tcga_list):
    for tcga_wsi in tcga_list:
        barcode_identifier = tcga_wsi.split("-")
        if len(barcode_identifier) > 4 and not os.listdir('DATA_DIRECTORY'):
            command = 'ln -s ' + '/data/kidney/' + tcga_wsi + ' /data/fsartori/CLAM/DATA_DIRECTORY'
            os.system(command)


def identify_non_tumor(tcga_list):
    with open('non_tumor.txt', 'w') as file:
        for tcga_wsi in tcga_list:
            barcode_identifier = tcga_wsi.split("-")
            if len(barcode_identifier) > 4 and re.search(r'(10|11)', barcode_identifier[3]):
                file.write(tcga_wsi + '\n')

    os.system('mv non_tumor.txt datasets')


tcga_list = select_dataset("/data/kidney")
create_csv_for_train(tcga_list)
#create_link(tcga_list)
identify_non_tumor(tcga_list)