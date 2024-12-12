#!/usr/bin/env bash

echo $'\033[1m

                                                    Welcome to prediction of IR spectra.

'
tput sgr0
echo "                                                 Answer all questions accourding to instructions.

"

echo "                                                 Enter path to DIRECTORY of model to predict with"

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


echo "                                                 File or direct input?"

echo -n "                                                    Answer (file/input): "
read -r ans

if test $ans = 'file'; then
echo "                                                 Enter path to file with SMILES and phase"

echo -n "                                                    Smiles path (csv file):"
read -r smiles

    until  test -f ./$smiles
    do
echo -n "                                                 SMILES file doesn't exist. Enter SMILES path (csv file): "
read -r smiles
    done
echo $'\033[1m                                                 File exists.

'
tput sgr0

else
echo "                                                 Enter SMILE"

echo -n "                                                    SMILE (surrounded by \" \"): "
read -r s

echo "                                                 Enter PHASE (valid phases: gas. KBr, CCl4, nujol mull, liquid film):"

echo -n "                                                    PHASE (surrounded by \" \"): "
read -r p

    echo "smiles, phase" > smiles.csv
    echo $s,$p >>smiles.csv
fi

echo $'\033[1m
                                                    Starting predictions of SMILES from: ' $ans 'using model:' $model


tput sgr0
cp -r $model Graphormer-IR/graphormer/evaluate/

#cd Graphormer-IR

if test $ans = 'file'
then
    bash Graphormer-IR/graphormer/evaluate/predict_new.sh $model $smiles
else
    bash Graphormer-IR/graphormer/evaluate/predict_new.sh $model smiles.csv
    rm smiles.csv
fi
