#!/bin/bash

#PARTE 3: Run Train

if [ -z "$(ls -A DATA_DIRECTORY)" ]; then
    echo "Non esistono dati in DATA_DIRECTORY"
else
    python create_splits_seq.py --task task_1_tumor_vs_normal --seed 1 --label_frac 0.75 --k 5
    CUDA_VISIBLE_DEVICES=0,1 python main.py --drop_out --early_stopping --lr 2e-4 --k 5 --label_frac 0.5 --exp_code task_2_tumor_subtyping_prostate --weighted_sample --bag_loss ce --inst_loss svm --task task_2_tumor_subtyping --model_type clam_sb --log_data --split_dir task_2_tumor_subtyping_75 --subtyping --data_root_dir FEATURES_DIRECTORY
fi