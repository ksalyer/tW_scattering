import os
import pandas as pd

deepAK8_SF = os.path.expandvars("$TWHOME/data/deepAK8/DeepAK8V2_Top_W_SFs.csv")

W_SF = pd.read_csv(deepAK8_SF, sep=',')

columns = ['pT_low', 'pT_high', 'SF', 'SF_lowerErr', 'SF_upperErr', 'Year', 'MistaggingRate']

W_SF = W_SF[((W_SF['Object']=='W') & (W_SF['version']=='Nominal'))][columns]
#SF_2017 = W_SF[((W_SF['Object']=='W') & (W_SF['version']=='Nominal')][columns]
#SF_2018 = W_SF[((W_SF['Object']=='W') & (W_SF['version']=='Nominal')][columns]

def getSFValue(i, SF, WP, sigma=0):
    if sigma == 1:
        return float(SF[SF['MistaggingRate']==WP][['SF']].values[i]) * (1 + sigma* float(SF[SF['MistaggingRate']==WP][['SF_upperErr']].values[i]) )
    elif sigma == -1:
        return float(SF[SF['MistaggingRate']==WP][['SF']].values[i]) * (1 + sigma* float(SF[SF['MistaggingRate']==WP][['SF_lowerErr']].values[i]) )
    else:
        return float(SF[SF['MistaggingRate']==WP][['SF']].values[i])

def getWTagSF(WTag, GenW, year=2016, WP='1p0', sigma=0):
    # this is probably the worst lookup in history
    matched_WTag = WTag[WTag.match(GenW, deltaRCut=0.8)]
    
    SF = W_SF[W_SF['Year']==year]
    #if year == 2016:
    #    SF = SF_2016
    #elif year == 2017:
    #    SF = SF_2017
    #elif year == 2018:
    #    SF = SF_2018
    
    sf = (matched_WTag.pt <= 300) * getSFValue(0, SF, WP, sigma) +\
         ((matched_WTag.pt > 300)&(matched_WTag.pt <= 400)) * getSFValue(1, SF, WP, sigma) +\
         (matched_WTag.pt > 400) * getSFValue(2, SF, WP, sigma)
    

    return sf.prod()

