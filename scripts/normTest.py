import ROOT

inFile = "/hadoop/cms/phedex/store/mc/RunIIAutumn18NanoAODv7/SMS-TChiWH_TuneCP2_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUFall18Fast_Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/100000/1CA252C9-2FA4-8848-959F-3C3CA93CDAF3.root"

file = ROOT.TFile.Open(inFile,"READ")

c = ROOT.TChain("Runs")
c.Add(inFile)
c.GetEntry(0)

#Get list of branch names that contain mass points
branches = []
for b in c.GetListOfBranches():
    branches.append(b.GetName())
branches.remove("run")

print(branches)

#Make a list of mass points in tree
massPoints = []
for i in range(len(branches)):
    mystr = branches[i]
    iMass = mystr.index("TChiWH_")
    mass = mystr[iMass:][7:]
    massPoints.append(mass)
massPoints = list(dict.fromkeys(massPoints))

#Make dictionary of info
dictionaries = []
for j in range(len(massPoints)):
    nEvents = getattr(c, 'genEventCount_TChiWH_'+massPoints[j])
    sumw = getattr(c, 'genEventSumw_TChiWH_'+massPoints[j])
    sumw2 = getattr(c, 'genEventSumw2_TChiWH_'+massPoints[j])

    dictionaries.append({"mass": massPoints[j],
                         "nEvents": nEvents,
                         "sumw": sumw,
                         "sumw2": sumw2})

#print(dictionaries)