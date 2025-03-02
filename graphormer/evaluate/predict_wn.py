import torch
import numpy as np
import sys


from fairseq import checkpoint_utils, utils, options, tasks
from fairseq.logging import progress_bar
from fairseq.dataclass.utils import convert_namespace_to_omegaconf
import ogb

import os
import pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import math

from os import path
import pickle
from tqdm import tqdm
import csv
from rdkit import Chem
from rdkit.Chem import Draw
#from evaluation_plot import *

sys.path.append( path.dirname(   path.dirname( path.abspath(__file__) ) ) )

from pretrain import load_pretrained_model

import logging

def import_data(file):
    with open(file) as rf:
        r=csv.reader(rf)
        next(r)
        data=[]
        for row in r:
            data.append(row)
        print("Data imported") 
        return data


def make_conv_matrix(frequencies,std_dev=15):
    length=len(frequencies)
    gaussian=[(1/(2*math.pi*std_dev**2)**0.5)*math.exp(-1*((frequencies[i])-frequencies[0])**2/(2*std_dev**2)) for i in range(length)]
    conv_matrix=np.empty([length,length])
    for i in range(length):
        for j in range(length):
            conv_matrix[i,j]=gaussian[abs(i-j)]
    return conv_matrix

def check_negative(y_pred):
    for i in range(len(y_pred)-1):
        if y_pred[i]<0:
            if y_pred[i+1]>=0:
                y_pred[i]=0

    return y_pred

def eval(args, use_pretrained, checkpoint_path=None, logger=None):
    start=int(args.start)
    end=int(args.end)
    n_point=int((end-start)/2)
    cfg = convert_namespace_to_omegaconf(args) 
    np.random.seed(cfg.common.seed)
    utils.set_torch_seed(cfg.common.seed)
    # initialize task
    task = tasks.setup_task(cfg.task)
    model = task.build_model(cfg.model)

    if use_pretrained:
        model_state = load_pretrained_model(cfg.task.pretrained_model_name)
    else:
        model_state = torch.load(checkpoint_path)["model"]

    model.load_state_dict(
        model_state, strict=True, model_cfg=cfg.model
    )
    del model_state

    model.to(torch.cuda.current_device())
    # load dataset
    split = args.split
    task.load_dataset(split)

    batch_iterator = task.get_batch_iterator(
        dataset=task.dataset(split),
        max_tokens=cfg.dataset.max_tokens_valid,
        max_sentences=cfg.dataset.batch_size_valid,
        max_positions=utils.resolve_max_positions(
            task.max_positions(),
            model.max_positions(),
        ),
        ignore_invalid_inputs=cfg.dataset.skip_invalid_size_inputs_valid_test,
        required_batch_size_multiple=cfg.dataset.required_batch_size_multiple,
        seed=cfg.common.seed,
        num_workers=cfg.dataset.num_workers,
        epoch=0,
        data_buffer_size=cfg.dataset.data_buffer_size,
        disable_iterator_cache=False,
    )
    itr = batch_iterator.next_epoch_itr(
        shuffle=False, set_dataset_epoch=False
    )
    progress = progress_bar.progress_bar(
        itr,
        log_format=cfg.common.log_format,
        log_interval=cfg.common.log_interval,
        default_log_format=("tqdm" if not cfg.common.no_progress_bar else "simple")
    )

    # infer
    y_pred = []
    y_true = []
    smilesL = []

    with torch.no_grad():
        model.eval()

        for i, sample in enumerate(progress): ## Grabbing batched input, SMILES
            sample = utils.move_to_cuda(sample)

            y = model(**sample["net_input"])
            smilesL.extend(sample["net_input"]['batched_data']['smiles'])
            y = y[:, :].reshape(-1)
            y_pred.extend(y.detach().cpu())
            y_true.extend(sample["target"].detach().cpu().reshape(-1)[:y.shape[0]])
            torch.cuda.empty_cache()



    # save predictions
    # evaluate pretrained models
    if use_pretrained:
        if cfg.task.pretrained_model_name == "pcqm4mv1_graphormer_base":
            evaluator = ogb.lsc.PCQM4MEvaluator()
            input_dict = {'y_pred': y_pred, 'y_true': y_true}
            result_dict = evaluator.eval(input_dict)
            logger.info(f'PCQM4Mv1Evaluator: {result_dict}')
        elif cfg.task.pretrained_model_name == "pcqm4mv2_graphormer_base":
            evaluator = ogb.lsc.PCQM4Mv2Evaluator()
            input_dict = {'y_pred': y_pred, 'y_true': y_true}
            result_dict = evaluator.eval(input_dict)
            logger.info(f'PCQM4Mv2Evaluator: {result_dict}')
    else: 
        if args.metric == "auc":
            auc = roc_auc_score(y_true, y_pred)
            logger.info(f"auc: {auc}")
        elif args.metric == "mae":
            mae = np.mean(np.abs(y_true - y_pred))
            logger.info(f"mae: {mae}")
        else: 
            y_pred = np.asarray(y_pred, dtype = np.float64)
        
            dset_size = 1801 ## size of wavenumber vector (400, 4000) 1801 before

            eval_only=True
            phase = import_data(sys.argv[-1])
            
            save = True

            total = len(y_pred)//dset_size
            conv_matrix = make_conv_matrix(frequencies=list(range(start,end,2)),std_dev=15) ## in wavenumber, used for smoothing gaussian convolution

            stack = []


            for i in range(total):
                smiles = smilesL[i]
                ph = phase[i][1]
                if len(phase[i])>2:
                    ID=phase[i][2]
                else: ID=[]


                y_val_pred = y_pred[i*dset_size: (i+1)*dset_size] ## Grabbing batched data
                y_val_pred=check_negative(y_val_pred)
                y_val_pred /= np.nanmax(y_val_pred) ## normalizing to sum
                y_val_pred=y_val_pred[:n_point]

                if eval_only:
                    
                    wv =np.arange(start, end, 2)
                    conv1=np.matmul(y_val_pred,conv_matrix)
                    sum1=np.nansum(conv1)
                    norm1=conv1/sum1 ## prediction
                    norm2 = list(np.zeros_like(norm1)) # padded true value
                    norm1=list(norm1)

                    norm1.extend([smiles])
                    norm1.extend([ph])
                    norm1.extend([ID])
                    print("Prediction for:", smiles, "in: ",ph,", with ID: ",ID)
                    stack.append(norm1)

                    if len(smilesL)<20:
                        plt.plot(wv, y_val_pred)
                        plt.title(smiles + ". Phase: " +phase[i][1])
                        plt.show()## if there is no target spectra (testing predictions)
                        continue
                    else:continue


            if save:


                wv =np.arange(start, end, 2)

                wv_pred = [str(i) for i in wv]
                header = wv_pred + ['smiles','phase', "ID"]
                cwd = os.getcwd()
                with open('./pred_results.csv', 'w', newline='\n') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',')
                    csvwriter.writerow(header)
                    for row in stack:
                        csvwriter.writerow(row)
                print("Results saved as: pred_results.csv")


            

def main():
    parser = options.get_training_parser()
    parser.add_argument(
        "--split",
        type=str,
    )

    parser.add_argument(
        "--metric",
        type=str,
    )
    parser.add_argument(
        "--start",
        type=int,
    )
    parser.add_argument(
        "--end",
        type=int,
    )
    args = options.parse_args_and_arch(parser, modify_parser=None)
    start=int(args.start)
    end=int(args.end)
    n_point=int((end-start)/2)
    logger = logging.getLogger(__name__)
    if args.pretrained_model_name != "none":
        eval(args, True, logger=logger)
    elif hasattr(args, "save_dir"):
        if os.path.isdir(args.save_dir):
            for checkpoint_fname in os.listdir(args.save_dir):
                checkpoint_path = Path(args.save_dir) / checkpoint_fname
                logger.info(f"evaluating checkpoint file {checkpoint_path}")
        else:
            checkpoint_path=args.save_dir
            logger.info(f"evaluating checkpoint file {checkpoint_path}")
        eval(args, False, checkpoint_path, logger)

if __name__ == '__main__':
    main()
