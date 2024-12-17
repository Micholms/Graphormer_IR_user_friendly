#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

#In conda env: conda create -n name_of_env python=3.9
mv ./*.sh ../
cd ..

pip install 'numpy<1.24'
pip install pip==24
pip install lmdb
pip install torch-geometric==1.7.2
pip install tensorboardX==2.4.1
pip install ogb==1.3.2
pip install rdkit-pypi==2021.9.3
pip install tensorboard==2.15.0
pip install setuptools==59.5.0
pip install protobuf==3.20.*
pip install matplotlib==3.8.1
pip install dgllife==0.3.2
pip install dgl==1.1.2

cd Graphormer-IR/fairseq
git submodule update --init --recursive
pip install --editable .
python setup.py build_ext --inplace

#install torch packages, make sure to use correct CUDA (here 11.8, tested for 11.5)
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
pip install torch-scatter -f https://pytorch-geometric.com/whl/torch-2.0.0%2Bcu118.html
pip install torch-sparse -f https://pytorch-geometric.com/whl/torch-2.0.0%2Bcu118.html
