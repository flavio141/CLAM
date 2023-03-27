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

#PARTE 2: Create le Patches
if [ -z "$(ls -A DATA_DIRECTORY)" ]; then
    echo "Non esistono dati in DATA_DIRECTORY"
else
    python create_patches_fp.py --source DATA_DIRECTORY --save_dir RESULTS_DIRECTORY --patch_size 256 --preset bwh_biopsy.csv --seg --patch --stitch
fi