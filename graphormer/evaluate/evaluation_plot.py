import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def get_true_pred(df):
    true=df.iloc[:,:1800]
    true.index=df["smiles"]
    pred=df.iloc[:,1800:]
    pred.index=df["smiles"]
    true["sim"]=pred["sim"]
    return true, pred

def get_percentile(df,p):
    x=df["sim"]
    pcen=np.percentile(x,p)
    i_high=np.asarray([i-pcen if i-pcen>=0 else x.max()-pcen for i in x]).argmin()
    i_low=np.asarray([i-pcen if i-pcen<=0 else x.min()-pcen for i in x]).argmax()
    i_near=abs(x-pcen).argmin()
    return i_near


def plot_percentile(df,true, pred,p_range):
    indexes=[]
    m,n=0,0
    for i in p_range:
        indexes.append(get_percentile(df,i))
    fig, ax = plt.subplots(5,2,figsize=(12,15), sharex=True, sharey=True)
    
    for j,index in enumerate(indexes):
     
        true_v=true.iloc[index,:-1]
        pred_v=pred.iloc[index,:-2]
        x=np.arange(400,4000,2)
        ax[m,n].plot(x,true_v/true_v.max(), label="True")
        ax[m,n].plot(x,pred_v/pred_v.max(), label="Pred")
        ax[m,n].legend()
        ax[m,n].set_title("Percentile: "+ str(p_range[j])+". SIS: "+str(round(pred.iloc[index,-1],4)), fontsize=10)
        if j<4: 
            n=0
            m=m+1
        if j==4: 
            m=0
            n=1
        if j>4:
            n=1
            m=m+1
    plt.show()



