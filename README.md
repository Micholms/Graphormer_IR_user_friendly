Graphormer IR user-friendly is a modified version of the Graphormer-IR model (https://github.com/HopkinsLaboratory/Graphormer-IR) by the authours of **Graphormer-IR: Graph Transformers Predict Experimental IR Spectra Using Highly Specialized Attention**. 
This updated version allows for use with simple interactive scripts, but all other work should be credited to them. 

@article{Stienstra2024, author = {Cailum M. K. Stienstra and Liam Hebert and Patrick Thomas and Alexander Haack and Jason Guo and W. Scott Hopkins}, doi = {10.1021/ACS.JCIM.4C00378}, issn = {1549-9596}, journal = {Journal of Chemical Information and Modeling}, month = {6}, publisher = {American Chemical Society}, title = {Graphormer-IR: Graph Transformers Predict Experimental IR Spectra Using Highly Specialized Attention}, url = {https://pubs.acs.org/doi/abs/10.1021/acs.jcim.4c00378}, year = {2024}, }

The Graphormer-IR code is based on the original work Grahormer by the authours of **Do Transformers Really Perform Badly for Graph Representation?**

@inproceedings{ ying2021do, title={Do Transformers Really Perform Badly for Graph Representation?}, author={Chengxuan Ying and Tianle Cai and Shengjie Luo and Shuxin Zheng and Guolin Ke and Di He and Yanming Shen and Tie-Yan Liu}, booktitle={Thirty-Fifth Conference on Neural Information Processing Systems}, year={2021}, url={https://openreview.net/forum?id=OeWooOxFwDa} }

---------------------------------------------------------------------
Set-up 

The model is based on Pytorch, and thus required correct installation. Here, an installation for CUDA 11.5 to 11.8 is available. Follow these steps in order to install the model:
  1. Create a conda envrionment with python 3.9

     conda create --name _<name_of_env>_ python=3.9

  2. Activate conda enviroment

     conda activate _<name_of_env>_

  3. Clone github repository

     git clone --recursive https://github.com/Micholms/Graphormer_IR_user_friendly

  4. Move into Graphormer_IR_user_friendly

     cd Graphormer_IR_user_friendly

  5. Run install for CUDA 11.5/11.8

     bash install_CUDA11.5_11.8.sh

After this point, only model and data is needed. It is possible to train a model from scratch, but the authors of Graphormer-IR made their best trained models available online at Zenodo (https://github.com/HopkinsLaboratory/Graphormer-IR).




