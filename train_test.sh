#!/bin/bash

#PARTE 3: Run Train

if [ -z "$(ls -A DATA_DIRECTORY)" ]; then
    echo "Non esistono dati in DATA_DIRECTORY"
else
    python create_splits_seq.py --task task_1_tumor_vs_normal --seed 1 --label_frac 0.75 --k 10
    CUDA_VISIBLE_DEVICES=0,1 python main.py --drop_out --early_stopping --lr 2e-4 --k 10 --label_frac 0.5 --exp_code task_1_tumor_subtyping_retrain --weighted_sample --bag_loss ce --inst_loss svm --task task_1_tumor_vs_normal --model_type clam_sb --log_data --split_dir task_1_tumor_vs_normal_80 --subtyping --data_root_dir FEATURES_DIRECTORY
fi