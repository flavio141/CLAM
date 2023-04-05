#!/bin/bash

#PARTE 3: Estraggo le Features

if [ -z "$(ls -A DATA_DIRECTORY)" ]; then
    echo "Non esistono dati in DATA_DIRECTORY"
else
    CUDA_VISIBLE_DEVICES=0 python extract_features_fp.py --data_h5_dir RESULTS_DIRECTORY --data_slide_dir DATA_DIRECTORY --csv_path RESULTS_DIRECTORY/process_list_autogen.csv --feat_dir FEATURES_DIRECTORY --batch_size 512 --slide_ext .svs
fi