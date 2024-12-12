Graphormer IR user-friendly 
--------------------------------------

Graphormer IR user-friendly is a modified version of the Graphormer-IR model (https://github.com/HopkinsLaboratory/Graphormer-IR) by the authors of: **Graphormer-IR: Graph Transformers Predict Experimental IR Spectra Using Highly Specialized Attention**. 

@article{Stienstra2024, author = {Cailum M. K. Stienstra and Liam Hebert and Patrick Thomas and Alexander Haack and Jason Guo and W. Scott Hopkins}, doi = {10.1021/ACS.JCIM.4C00378}, issn = {1549-9596}, journal = {Journal of Chemical Information and Modeling}, month = {6}, publisher = {American Chemical Society}, title = {Graphormer-IR: Graph Transformers Predict Experimental IR Spectra Using Highly Specialized Attention}, url = {https://pubs.acs.org/doi/abs/10.1021/acs.jcim.4c00378}, year = {2024}, }

The Graphormer-IR code is based on the original work Grahormer by the authors of: **Do Transformers Really Perform Badly for Graph Representation?**

@inproceedings{ ying2021do, title={Do Transformers Really Perform Badly for Graph Representation?}, author={Chengxuan Ying and Tianle Cai and Shengjie Luo and Shuxin Zheng and Guolin Ke and Di He and Yanming Shen and Tie-Yan Liu}, booktitle={Thirty-Fifth Conference on Neural Information Processing Systems}, year={2021}, url={https://openreview.net/forum?id=OeWooOxFwDa} }

This updated version allows for use with simple interactive scripts, but all other work should be credited to Cailum M. K. Stienstra, Liam Hebert, Patrick Thomas, Alexander Haack, Jason Guo and W. Scott Hopkins along Chengxuan Ying, Tianle Cai, Shengjie Luo, Shuxin Zheng, Guolin Ke, Di He, Yanming Shen and Tie-Yan Liu.

**Set-up**
---------------------------------------------------------------------


The model is based on Pytorch, and thus required correct installation. Here, an installation for CUDA 11.5 to 11.8 is available. Follow these steps in order to install the model:
  1. Create a conda environment with python 3.9
     
    conda create --name <name_of_env> python=3.9

  2. Activate conda enviroment
     
    conda activate <name_of_env>

  3. Clone github repository
     
    git clone --recursive https://github.com/Micholms/Graphormer_IR_user_friendly

  4. Move into Graphormer_IR_user_friendly
     
    cd Graphormer_IR_user_friendly

  5. Run install for CUDA 11.5/11.8
  
    bash install_CUDA11.5_11.8.sh

  6. Lastly, move up one directory

    cd ..

After this point, only model and data is needed. The folder Graphormer_IR_user_friendly have been renamed to Graphormer-IR and all files put in the correct place.

**Data**
-----------------------------------------------------------------------

_Regarding pre-trained splits_

See info here https://github.com/HopkinsLaboratory/Graphormer-IR or https://pubs.acs.org/doi/abs/10.1021/acs.jcim.4c00378

_For fine-tuning_

It is possible to fine-tune a split with use of your own data. The input should be in a .csv file, with SMILES, phase and intensities for 400-4000 cm-1, with 2cm-1 intervals, as the example _NIST_IR_Dataset.csv_

Possible phases (at the moment) are gas, KBr. nujol mull, liquid film and CCl4. Training, validation and testing split can be created by running the csv-file through gen_splits.py (found in _scripts_ )

    cd scripts
    python3 gen_splits.py <path_to_csv-file>

This will generate four files: _training_dataset.csv_, _testing_dataset.csv, valid_indices.csv_ and _train_indices.csv_ (placed in a folder named _Data_splits_. Move this to main folder for easier access.)


**Usage**
----------------------------------------------------------------------

It is possible to train a model from scratch, but the authors of Graphormer-IR made their best trained splits available online at Zenodo (https://github.com/HopkinsLaboratory/Graphormer-IR). Information of model training, architecture etc can be found there. 


There exist interactive scripts enabling fine-tuning, evaluation and prediction.


**Fine-tuning:** 

Run Interactive_training.sh in its location and answer all questions accordingly. 

    bash Interactive_training.sh
    
It is also possible to fine tune without the interactive script by first move the folder with training_dataset.csv, valid_indices.csv and train_indices.csv( possibly _Data_splits_)

    cp -r <dataset_path> Graphormer-IR/graphormer/
    
Then:

    cd examples/property_prediction
  
    bash IRspec.sh <LR> <EPOCHS> <BASE-MODEL-DIR> <DIR_FOR_SAVING>

where <LR> and <EPOCHS> are numeric number, <BASE-MODEL-DIR> are the FOLDER for the model to fine-tune, and <DIR_FOR_SAVING> the folder for the fine-tuned model 

NOTE: WandB is included in these scripts, edit Train_IR_model.sh and IRspec.sh for interactive or normal usage, respectively, to remove/change this.  

NOTE: If downloading from Zenodo, put the model in a folder. For example "base_model/split1_0.8516.pt" then use _base_model_ as BASE-MODEL-DIR.


**Evulation:**

Run Interactive_evaluation.sh in its location and answer all questions accordingly. 

    bash Interactive_evaluation.sh
    
It is also possible to evaluate without the interactive script by:

    cd graphormer/evaluate
    bash evaluate_quick.sh  <MODEL-DIR> <DATA>

where <MODEL-DIR> are the FOLDER for the model to evaluate, and <DATA> the path to the data to evaluate with (possible testing_dataset.csv from _Data_splits_)

Histogram over SIS values (Spectral Information Similarities) as well as result of 10th to 100th percentile of predictions based on SIS, will pop up.

The predicted intensities along with SIS values and true values will be obtain in a csv file (_eval_result.csv_), for 400-4000 cm-1


**Prediction:**

Prediction, without experimental values, can be done both by direct input and by a list of SMILES with PHASES from a csv file, by running Interactive_prediction.sh in its location and answer all questions accordingly. 

    bash Interactive_prediction.sh
    
It is also possible to predict from file without the interactive script by:

    cd graphormer/evaluate
    bash predict_quick.sh  <MODEL-DIR> <DATA>

where <MODEL-DIR> are the FOLDER for the model to predict with, and <DATA> the path to the data to predict with. The data file should be ordered as the example _SMILES_to_predict.csv_

The prediction result will be saved in a file called pred_result.csv. Furthermore, the plotted spectrum will appear (can be saved manually).




