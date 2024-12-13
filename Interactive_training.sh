#!/usr/bin/env bash

echo $'\033[1m

                                                     Welcome to fine-tuning of IR model.

'
tput sgr0
echo "                                                 Answer all questions accourding to instructions.

"

echo '                                                 Enter base model DIRECTORY'
echo -n "                                                   Model DIRECTORY: "
read -r model

until  test -d ./$model
do
    echo -n "                                                 Model DIRECTORY doesn't exist. Enter model DIRECTORY path: "
    read -r model
done
echo $'\033[1m                                                 Directory exists.

'

echo "                                                 Enter learining rate"
echo -n "                                                   LR: "
read -r lr

echo "                                                 Enter number of epochs"
echo -n "                                                   Epochs: "
read -r epochs

echo "                                                 Enter path to save fine-tuned model"
echo -n "                                                   Save path: "
read -r save


echo "                                                 Enter DIRECTORY to dataset to train on"
echo -n "                                                   Dataset DIRECTORY: "
read -r dataset

until  test -d ./$dataset
do
    echo -n "                                                 Dataset DIRECTORY doesn't exist. Enter DIRECTORY to dataset: "
    read -r dataset
done
echo $'\033[1m                                                 Directory exists.

'


cp -r $dataset/*.csv ./


bash Graphormer-IR/examples/property_prediction/Train_IR_model.sh $lr $epochs $model $save

rm testing_dataset.csv
rm training_dataset.csv
rm train_indices.csv
rm valid_indices.csv

