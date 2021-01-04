import pandas as pd
#import pickle
import pickle5 as pickle
import os

def getSignalWeight(df, model, year=2016):


    with open(os.path.expandvars('$TWHOME/data/WH_signalweights_%s.pkl'%year), 'rb') as f:
        signal_dict = pickle.load(f)

    signal_df = pd.DataFrame(signal_dict)

    tmp_name  = model.split('_')[0].replace('TChi','')
    tmp_mNLSP = int(model.split('_')[1])
    tmp_mLSP  = int(model.split('_')[2])
    #tmp_df = signal_df[signal_df['model']==tmp_name]
    try:
        xsec = float(signal_df[((signal_df['mNLSP']==tmp_mNLSP) & (signal_df['mLSP']==tmp_mLSP) )]['xsec'])
        sumweight = float(signal_df[((signal_df['mNLSP']==tmp_mNLSP) & (signal_df['mLSP']==tmp_mLSP) )]['sumweight'])
    except TypeError:
        #print ("No x-sec")
        xsec = 0
        sumweight = 1
    #mNLSP += df[model] * tmp_mNLSP
    #mLSP += df[model] * tmp_mLSP
    try:
        weight = ( df['genWeight'] * df['GenModel_'+model] * xsec / sumweight) # 
    except:
        weight = ( df['genWeight']*0 )
    return weight
