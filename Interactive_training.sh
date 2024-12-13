#!/usr/bin/env bash

echo $'\033[1m

                                                     Welcome to fine-tuning of IR model.

'
tput sgr0
echo "                                                 Answer all questions accourding to instructions.

"

echo '                                                 Enter base model path'
echo -n "                                                   Model path: "
read -r model

echo "                                                 Enter learining rate"
echo -n "                                                   LR: "
read -r lr

echo "                                                 Enter number of epochs"
echo -n "                                                   Epochs: "
read -r epochs

echo "                                                 Enter path to save fine-tuned model"
echo -n "                                                   Save path: "
read -r save


echo "                                                 Enter path to dataset to train on"
echo -n "                                                   Dataset path: "
read -r dataset


cp -r $dataset/*.csv ./


bash Graphormer-IR/examples/property_prediction/Train_IR_model.sh $lr $epochs $model $save $dataset

rm testing_dataset.csv
rm training_dataset.csv
rm train_indices.csv
rm valid_indices.csv
