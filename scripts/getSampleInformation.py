'''
takes DAS name, checks for local availability, reads norm, x-sec

e.g.
/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
-->
TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1

'''

import yaml
from yaml import Loader, Dumper

import os

import uproot
import glob
#from coffea.processor.dataframe import LazyDataFrame

from Tools.helpers import *

data_path = os.path.expandvars('$TWHOME/data/')

#def loadConfig():
#    with open(data_path+'config.yaml') as f:
#        config = yaml.load(f, Loader=Loader)
#    return config
#
#def getName( DAS ):
#    split = DAS.split('/')
#    if split[-1].count('AOD'):
#        return '__'.join(DAS.split('/')[1:3])
#    else:
#        return'dummy'

def readSampleNames( sampleFile ):
    with open( sampleFile ) as f:
        samples = [ tuple(line.split()) for line in f.readlines() ]
    return samples
    
#def readSumWeight( samplePath ):
#    # for central nanoAOD
#    sumWeight = 0.
#    nEvents = 0
#    files = glob.glob(samplePath + '/*.root')
#    for f in files:
#        rfile = uproot.open(f)
#        try:
#            tree = rfile['Runs']
#            df = LazyDataFrame(tree)
#            sumWeight += float(df['genEventSumw_'])
#            nEvents += int(df['genEventCount_'])
#        except KeyError:
#            tree = rfile['Events']
#            df = LazyDataFrame(tree)
#            sumWeight += float(df['genWeight'].sum())
#            nEvents += len(df['genWeight'])
#
#    return sumWeight, nEvents

def getMeta(file, local=True):
    '''
    for some reason, xrootd doesn't work in my environment with uproot. need to use pyroot for now...
    '''
    import ROOT
    c = ROOT.TChain("Runs")
    c.Add(file)
    c.GetEntry(0)
    if local:
        res = c.genEventCount, c.genEventSumw, c.genEventSumw2
    else:
        res = c.genEventCount_, c.genEventSumw_, c.genEventSumw2_
    del c
    return res

def dasWrapper(DASname, query='file'):
    sampleName = DASname.rstrip('/')

    dbs='dasgoclient -query="%s dataset=%s"'%(query, sampleName)
    dbsOut = os.popen(dbs).readlines()
    dbsOut = [ l.replace('\n','') for l in dbsOut ]
    return dbsOut

def getSampleNorm(files, local=True):
    files = [ 'root://cmsxrootd.fnal.gov/'+f for f in files ] if not local else files
    nEvents, sumw, sumw2 = 0,0,0
    for f in files:
        res = getMeta(f, local=local)
        nEvents += res[0]
        sumw += res[1]
        sumw2 += res[2]
    return nEvents, sumw, sumw2

def getBranches(files, local=True):
    import ROOT

    files = [ 'root://cmsxrootd.fnal.gov/'+f for f in files ] if not local else files
    branches = []

    for f in files:
        c = ROOT.TChain("Runs")
        c.Add(f)
        c.GetEntry(0)
    
        for b in c.GetListOfBranches():
            branches.append(b.GetName())
        branches.remove("run")
    return branches

def getMasses(branches):
    masses = []
    for i in range(len(branches)):
        mystr = branches[i]
        iMass = mystr.index("TChiWH_")
        mass = mystr[iMass:][7:]
        masses.append(mass)
    masses = list(dict.fromkeys(masses))
    return masses

def getScanNorm(files):
    import ROOT

    files = [ 'root://cmsxrootd.fnal.gov/'+f for f in files ] if not local else files

    masses = getMasses(getBranches(files))
    dictionaries = []

    for f in files:
        c = ROOT.TChain("Runs")
        c.Add(f)
        c.GetEntry(0)
    
        branches = []

        for b in c.GetListOfBranches():
            branches.append(b.GetName())
        branches.remove("run")

        for m in range(len(masses)):
            branchName = 'genEventCount_TChiWH_'+masses[m]
            if branchName in branches:
                nEvents = getattr(c, 'genEventCount_TChiWH_'+masses[m])
                sumw = getattr(c, 'genEventSumw_TChiWH_'+masses[m])
                sumw2 = getattr(c, 'genEventSumw2_TChiWH_'+masses[m])

                for d in range(len(dictionaries)):
                    if d["mass"] == masses[m]:
                        d["nEvents"] += nEvents
                        d["sumw"] += sumw
                        d["sumw2"] += sumw2
                    else:
                        dictionaries.append({"mass": masses[m],
                                             "nEvents": nEvents,
                                             "sumw": sumw,
                                             "sumw2": sumw2})
            else:
                continue
    return dictionaries


def main():

    config = loadConfig()

    # get list of samples
    sampleList = readSampleNames( data_path+'samples.txt' )

    with open(data_path+'samples.yaml') as f:
        samples = yaml.load(f, Loader=Loader)

    # initialize
    if not samples:
        samples = {}

    for sample in sampleList:
        sample_dict = {}

        # First, get the name
        name = getName(sample[0])
        print (name)

        # local/private sample?
        local = (sample[0].count('hadoop') + sample[0].count('home'))
        print ("Is local?", local)
        print (sample[0])

        # scan (fastsim) sample?
        fastsim = (sample[0].count('Fast'))
        print ("Is fastsim?", fastsim)
        print (sample[0])

        if local:
            sample_dict['path'] = sample[0]
            allFiles = glob.glob(sample[0] + '/*.root')
        else:
            sample_dict['path'] = None
            allFiles = dasWrapper(sample[0], query='file')
        print (allFiles)

        if fastsim:


        else:
            sample_dict['files'] = allFiles

            nEvents, sumw, sumw2 = getSampleNorm(allFiles, local=local)

        sample_dict.update({'sumWeight': sumw, 'nEvents': nEvents, 'xsec': float(sample[1]), 'name':name})
        
        samples.update({str(sample[0]): sample_dict})

        #print (sample[0], name)
        #if not sample[0] in samples.keys():
        #    samplePath = os.path.join(config['meta']['localNano'], getName(sample[0]) )
        #    if os.path.isdir( samplePath ):
        #        pass
        #    elif os.path.isdir( sample[0] ):
        #        samplePath = sample[0]
        #    else:
        #        raise NotImplementedError
        #    sumWeight, nEvents = readSumWeight(samplePath)
        #    samples.update({str(sample[0]): {'sumWeight': sumWeight, 'nEvents': nEvents, 'xsec': float(sample[1]), 'name':name, 'path':samplePath}})
        #sample['sumWeight'] = sumWeight
        #sample[

    with open(data_path+'samples.yaml', 'w') as f:
        yaml.dump(samples, f, Dumper=Dumper)
    # check if they are in the yaml file
    
    

    return samples


if __name__ == '__main__':
    samples = main()



