#!/bin/bash

#PARTE 1: Elenco delle cartelle da cancellare
folders=(
    FEATURES_DIRECTORY
    RESULTS_DIRECTORY
)

# Ciclo su tutte le cartelle da cancellare
for folder in "${folders[@]}"
do
    if [ -d "$folder" ]; then
        # Cancella la cartella e tutte le sue sottocartelle
        echo "Cancellazione delle subfolders di $folder..."
        #rm -rf $folder/*
    else
        echo "Attenzione: la cartella $folder non esiste."
    fi
done

#PARTE 2: Create Patches
if [ -z "$(ls -A DATA_DIRECTORY)" ]; then
    echo "Non esistono dati in DATA_DIRECTORY"
else
    python create_patches_fp.py --source DATA_DIRECTORY --save_dir RESULTS_DIRECTORY --patch_size 256 --preset bwh_biopsy.csv --seg --patch --stitch
fi

#PARTE 3: Estraggo le Features

if [ -z "$(ls -A DATA_DIRECTORY)" ]; then
    echo "Non esistono dati in DATA_DIRECTORY"
else
    CUDA_VISIBLE_DEVICES=0,1 python extract_features_fp.py --data_h5_dir RESULTS_DIRECTORY --data_slide_dir DATA_DIRECTORY --csv_path RESULTS_DIRECTORY/process_list_autogen.csv --feat_dir FEATURES_DIRECTORY --batch_size 512 --slide_ext .svs
fi