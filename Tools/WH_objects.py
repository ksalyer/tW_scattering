from coffea.processor.accumulator import AccumulatorABC
from coffea.analysis_objects import JaggedCandidateArray
import numpy as np
## happily borrowed from https://github.com/bu-cms/bucoffea/blob/master/bucoffea/helpers/helpers.py

def mask_or(df, masks):
    """Returns the OR of the masks in the list
    :param df: Data frame
    :type df: LazyDataFrame
    :param masks: Mask names as saved in the df
    :type masks: List
    :return: OR of all masks for each event
    :rtype: array
    """
    # Start with array of False
    decision = np.ones(df.size)==0

    # Flip to true if any is passed
    for t in masks:
        try:
            decision = decision | df[t]
        except KeyError:
            continue
    return decision

def mask_and(df, masks):
    """Returns the AND of the masks in the list
    :param df: Data frame
    :type df: LazyDataFrame
    :param masks: Mask names as saved in the df
    :type masks: List
    :return: OR of all masks for each event
    :rtype: array
    """
    # Start with array of False
    decision = np.ones(df.size)==1

    # Flip to true if any is passed
    for t in masks:
        try:
            decision = decision & df[t]
        except KeyError:
            continue
    return decision


def getFilters(df, year=2018, dataset='None'):
    #filters, recommendations in https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2
    if year == 2018:
        filters_MC = [\
            "Flag_goodVertices",
            "Flag_globalSuperTightHalo2016Filter",
            "Flag_HBHENoiseFilter",
            "Flag_HBHENoiseIsoFilter",
            "Flag_EcalDeadCellTriggerPrimitiveFilter",
            "Flag_BadPFMuonFilter",
            "Flag_ecalBadCalibFilterV2"
        ]
        
        filters_data = filters_MC + ["Flag_eeBadScFilter"]
        
    elif year == 2017:
        filters_MC = [\
            "Flag_goodVertices",
            "Flag_globalSuperTightHalo2016Filter",
            "Flag_HBHENoiseFilter",
            "Flag_HBHENoiseIsoFilter",
            "Flag_EcalDeadCellTriggerPrimitiveFilter",
            "Flag_BadPFMuonFilter",
            "Flag_ecalBadCalibFilterV2"
        ]
        
        filters_data = filters_MC + ["Flag_eeBadScFilter"]

    elif year == 2016:
        filters_MC = [\
            "Flag_goodVertices",
            "Flag_globalSuperTightHalo2016Filter",
            "Flag_HBHENoiseFilter",
            "Flag_HBHENoiseIsoFilter",
            "Flag_EcalDeadCellTriggerPrimitiveFilter",
            "Flag_BadPFMuonFilter",
        ]
        
        filters_data = filters_MC + ["Flag_eeBadScFilter"]
        
    if dataset.lower().count('data') or dataset.lower().count('run201'):
        return mask_and(df, filters_data)
    else:
        return mask_and(df, filters_MC)
        
def getTriggers(df, year=2018, dataset='None'):
    # these are the MET triggers from the MT2 analysis
    
    if year == 2018:
        triggers = [\
            "HLT_PFMET120_PFMHT120_IDTight",
            "HLT_PFMET120_PFMHT120_IDTight_PFHT60",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",
        ]
        
    elif year == 2017:
        triggers = [\
            "HLT_PFMET120_PFMHT120_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
        ]
        
    elif year == 2016:
        triggers = [\
            "HLT_PFMET120_PFMHT120_IDTight",
            "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
        ]
        
    if dataset.lower().count('data') or dataset.lower().count('run201'):
        return mask_or(df, triggers)
    else:
        return (df['run']>0)

    
def getMuons(df, WP='veto'):
    muon = JaggedCandidateArray.candidatesfromcounts(
            df['nMuon'],
            pt = df['Muon_pt'].content,
            eta = df['Muon_eta'].content,
            phi = df['Muon_phi'].content,
            mass = df['Muon_mass'].content,
            miniPFRelIso_all=df['Muon_miniPFRelIso_all'].content,
            looseId =df['Muon_looseId'].content,
            mediumId =df['Muon_mediumId'].content,
            pdgId =df['Muon_pdgId'].content,
            )
    if WP=='veto':
        return muon[(muon.pt > 10) & (abs(muon.eta) < 2.4) & (muon.looseId) & (muon.miniPFRelIso_all < 0.2)]
    elif WP=='medium':
        return muon[(muon.pt > 25) & (abs(muon.eta) < 2.4) & (muon.mediumId) & (muon.miniPFRelIso_all < 0.2)]


def getElectrons(df, WP='veto'):
    electron = JaggedCandidateArray.candidatesfromcounts(
            df['nElectron'],
            pt = df['Electron_pt'].content,
            eta = df['Electron_eta'].content,
            #etaSC = (df['Electron_eta']+df['Electron_deltaEtaSC']).content,
            phi = df['Electron_phi'].content,
            mass = df['Electron_mass'].content,
            miniPFRelIso_all=df['Electron_miniPFRelIso_all'].content,
            cutBased=df['Electron_cutBased'].content
            )
    if WP=='veto':
        return electron[(electron.pt>10) & (abs(electron.eta) < 2.4) & (electron.miniPFRelIso_all < 0.1) &  (electron.cutBased >= 1)]
    elif WP=='medium':
        return electron[(electron.pt>25) & (abs(electron.eta) < 2.4) & (electron.miniPFRelIso_all < 0.1) &  (electron.cutBased >= 3)]
    elif WP=='tight':
        return electron[(electron.pt>30) & (abs(electron.eta) < 2.4) & (electron.miniPFRelIso_all < 0.1) &  (electron.cutBased >= 4)]

def getTaus(df, WP='veto'):
    tau = JaggedCandidateArray.candidatesfromcounts(
            df['nTau'],
            pt=df['Tau_pt'].content, 
            eta=df['Tau_eta'].content, 
            phi=df['Tau_phi'].content,
            mass=df['Tau_mass'].content,
            decaymode=df['Tau_idDecayMode'].content,
            newid=df['Tau_idMVAnewDM2017v2'].content,
        )
    if WP == 'veto':
        return tau[(tau.pt > 20) & (abs(tau.eta) < 2.4) & (tau.decaymode) & (tau.newid >= 8)]

def getIsoTracks(df, WP='veto'):
    isotrack = JaggedCandidateArray.candidatesfromcounts(
            df['nIsoTrack'],
            pt=df['IsoTrack_pt'].content, 
            eta=df['IsoTrack_eta'].content,
            phi=df['IsoTrack_phi'].content, 
            mass=((df['IsoTrack_pt']>0)*0.).content,
            rel_iso=df['IsoTrack_pfRelIso03_all'].content, 
        )
    if WP == 'veto':
        return isotrack[(isotrack.pt > 10) & (abs(isotrack.eta) < 2.4) & ((isotrack.rel_iso < 0.1) | ((isotrack.rel_iso*isotrack.pt) < 6))]
 
    
def getFatJets(df, ptcorr=None, masscorr=None):
    ptpostfix = '' if ptcorr is None else ptcorr
    masspostfix = '' if masscorr is None else masscorr
    fatjet = JaggedCandidateArray.candidatesfromcounts(
            df['nFatJet'],
            pt = df['FatJet_pt%s'%ptpostfix].content,
            eta = df['FatJet_eta'].content,
            phi = df['FatJet_phi'].content,
            mass = df['FatJet_mass%s'%masspostfix].content,
            msoftdrop = df["FatJet_msoftdrop%s"%masspostfix].content,  
            deepTagMD_HbbvsQCD = df['FatJet_deepTagMD_HbbvsQCD'].content, 
            deepTagMD_WvsQCD = df['FatJet_deepTagMD_WvsQCD'].content, 
            deepTag_WvsQCD = df['FatJet_deepTag_WvsQCD'].content
            
        )
    return fatjet[(fatjet.pt>200) & (abs(fatjet.eta)<2.4)]

def getJets(df):
    jet = JaggedCandidateArray.candidatesfromcounts(
            df['nJet'],
            pt = df['Jet_pt'].content,
            eta = df['Jet_eta'].content,
            phi = df['Jet_phi'].content,
            mass = df['Jet_mass'].content,
            jetId = df['Jet_jetId'].content, # https://twiki.cern.ch/twiki/bin/view/CMS/JetID
            btagDeepB = df['Jet_btagDeepB'].content, # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
        )
    return jet[(jet.pt>30) & (abs(jet.eta)<2.4) & (jet.jetId>1)]

def getBTags(jet, year=2016):
    if year == 2016:
        return jet[(jet.btagDeepB>0.6321)] # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
    elif year == 2017:
        return jet[(jet.btagDeepB>0.4941)] # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
    elif year == 2018:
        return jet[(jet.btagDeepB>0.4184)] # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X

def getHTags(fatjet, year=2016):
    # 2.5% WP
    # https://indico.cern.ch/event/853828/contributions/3723593/attachments/1977626/3292045/lg-btv-deepak8v2-sf-20200127.pdf#page=4
    if year == 2016:
        return fatjet[(fatjet.deepTagMD_HbbvsQCD > 0.8945)] 
    elif year == 2017:
        return fatjet[(fatjet.deepTagMD_HbbvsQCD > 0.8695)] 
    elif year == 2018:
        return fatjet[(fatjet.deepTagMD_HbbvsQCD > 0.8365)] 

def getWTags(fatjet, year=2016, WP='1p0'):
    # 1% WP
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/DeepAK8Tagging2018WPsSFs
    if year == 2016:
        cuts = {'1p0': 0.918, '2p5': 0.763}
        return fatjet[(fatjet.deepTag_WvsQCD > cuts[WP])] 
    elif year == 2017:
        cuts = {'1p0': 0.925, '2p5': 0.772}
        return fatjet[(fatjet.deepTag_WvsQCD > cuts[WP])] 
    elif year == 2018:
        cuts = {'1p0': 0.918, '2p5': 0.762}
        return fatjet[(fatjet.deepTag_WvsQCD > cuts[WP])] # yes, really

def getGenW(df):
    GenW = JaggedCandidateArray.candidatesfromcounts(
            df['nGenW'],
            pt = df['GenW_pt'].content,
            eta = df['GenW_eta'].content,
            phi = df['GenW_phi'].content,
            mass = ((df['GenW_pt']>0)*80).content,
        )
    return GenW

def getGenParts(df):
    GenPart = JaggedCandidateArray.candidatesfromcounts(
        df['nGenPart'],
        pt=df['GenPart_pt'].content,
        eta=df['GenPart_eta'].content,
        phi=df['GenPart_phi'].content,
        mass=df['GenPart_mass'].content,
        pdgId=df['GenPart_pdgId'].content,
        status=df['GenPart_status'].content,
        genPartIdxMother=df['GenPart_genPartIdxMother'].content,
        statusFlags=df['GenPart_statusFlags'].content,
    )

def getHadWFromGenPart(GenPart):
    return GenPart[GenPart[((GenPart.pdgId<6) & (GenPart.pdgId>0) & (abs(GenPart[GenPart.genPartIdxMother].pdgId)==24))].genPartIdxMother]

