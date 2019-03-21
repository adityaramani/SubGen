#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files /content/SubGen/scripts/train1.csv\
  --dev_files /content/SubGen/scripts/dev1.csv \
  --test_files /content/SubGen/scripts/val1.csv \
  --train_batch_size 10 \
  --dev_batch_size 10 \
  --test_batch_size 10 \
  --n_hidden 2048 \
  --epoch -3 \
  --validation_step 1 \
  --early_stop True \
  --earlystop_nsteps 6 \
  --estop_mean_thresh 0.1 \
  --estop_std_thresh 0.1 \
  --dropout_rate 0.1 \
  --learning_rate 0.0001 \
  --report_count 100 \
  --use_seq_length False \
  --export_dir "/gdrive/My Drive/exported_models/" \
  --checkpoint_dir "/gdrive/My Drive/deepspeech-0.4.1-checkpoint" \
  "$@"

