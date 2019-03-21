#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files /home/aditya/Documents/project/SubGen/scripts/train.csv\
  --dev_files /home/aditya/Documents/project/SubGen/scripts/dev.csv \
  --test_files /home/aditya/Documents/project/SubGen/scripts/val.csv \
  --train_batch_size 8 \
  --dev_batch_size 8 \
  --test_batch_size 8 \
  --n_hidden 2048 \
  --epoch -150 \
  --validation_step 1 \
  --early_stop True \
  --earlystop_nsteps 6 \
  --estop_mean_thresh 0.1 \
  --estop_std_thresh 0.1 \
  --dropout_rate 0.1 \
  --learning_rate 0.0001 \
  --report_count 100 \
  --use_seq_length False \
  --export_dir /home/aditya/Documents/project/indian_model/1/exported2/ \
  --checkpoint_dir /home/aditya/Downloads/deepspeech-0.4.1-checkpoint/ \
  "$@"

