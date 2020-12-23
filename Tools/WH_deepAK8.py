import os
import pandas as pd

deepAK8_SF = os.path.expandvars("$TWHOME/data/deepAK8/DeepAK8V2_Top_W_SFs.csv")

W_SF = pd.read_csv(deepAK8_SF, sep=',')

columns = ['pT_low', 'pT_high', 'SF', 'SF_lowerErr', 'SF_upperErr']

SF_2016 = W_SF[((W_SF['Object']=='W') & (W_SF['version']=='Nominal') & (W_SF['MistaggingRate']=='1p0') & (W_SF['Year']==2016))][columns]
SF_2017 = W_SF[((W_SF['Object']=='W') & (W_SF['version']=='Nominal') & (W_SF['MistaggingRate']=='1p0') & (W_SF['Year']==2017))][columns]
SF_2018 = W_SF[((W_SF['Object']=='W') & (W_SF['version']=='Nominal') & (W_SF['MistaggingRate']=='1p0') & (W_SF['Year']==2018))][columns]

def getSFValue(i, SF, sigma=0):
    if sigma == 1:
        return float(SF[['SF']].values[i]) * (1 + sigma* float(SF[['SF_upperErr']].values[i]) )
    elif sigma == -1:
        return float(SF[['SF']].values[i]) * (1 + sigma* float(SF[['SF_lowerErr']].values[i]) )
    else:
        return float(SF[['SF']].values[i])

def getWTagSF(WTag, GenW, year=2016, sigma=0):
    # this is probably the worst lookup in history
    matched_WTag = WTag[WTag.match(GenW, deltaRCut=0.8)]
    
    if year == 2016:
        SF = SF_2016
    elif year == 2017:
        SF = SF_2017
    elif year == 2018:
        SF = SF_2018
    
    sf = (matched_WTag.pt <= 300) * getSFValue(0, SF, sigma) +\
         ((matched_WTag.pt > 300)&(matched_WTag.pt <= 400)) * getSFValue(1, SF, sigma) +\
         (matched_WTag.pt > 400) * getSFValue(2, SF, sigma)
    

    return sf.prod()

