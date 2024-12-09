#!/usr/bin/env bash

echo $'\033[1m

                                                     Welcome to evalutation of IR spectra model.

'
tput sgr0
echo "                                                 Answer all questions accourding to instructions.

"



echo "                                                 Enter path to DIRECTORY of model to evaluate"

echo -n "                                                    Model DIRECTORY: "
read -r model

until  test -d ./$model
do
    echo -n "                                                 Model DIRECTORY doesn't exist. Enter model DIRECTORY path: "
    read -r model
done
echo $'\033[1m                                                 Directory exists.

'
tput sgr0
echo "                                                 Enter path to file to use as testing set"

echo -n "                                                    Testing set path: "
read -r testing


until  test -f ./$testing
do
    echo -n "                                                 File doesn't exist. Enter testing set path: "
    read -r testing
done
echo $'\033[1m                                                 File exists.

'

echo $'\033[01
                                                    Starting evaluation of model:' $model'. Using dataset: ' $testing

echo



tput sgr0

cp -r $model Graphormer-IR/graphormer/evaluate/
cp -r $testing Graphormer-IR/graphormer/evaluate/

bash Graphormer-IR/graphormer/evaluate/evaluate_new.sh $model $testing


rm -r Graphormer-IR/graphormer/evaluate/$model
rm -r Graphormer-IR/graphormer/evaluate/$testing

