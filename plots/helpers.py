import os
import matplotlib.pyplot as plt
from Tools.helpers import finalizePlotDir

def saveFig( fig, ax, rax, path, name, scale='linear', shape=False, y_max=-1, preliminary='Simulation', lumi=137 ):
    outdir = os.path.join(path,scale)
    finalizePlotDir(outdir)
    ax.set_yscale(scale)
    ax.set_ylabel('Events')

    if scale == 'linear':
        if y_max<0 or True:
            pass
        else:
            ax.set_ylim(0, 1 if shape else 1.2*y_max)
    else:
        if y_max<0 and not shape:
            pass
        else:
            ax.set_ylim(0.000005 if shape else 0.05, 3 if shape else 300*y_max)

    #if scale == 'log':
    #    ax.set_ylim(y_min, y_max)
    #else:
    #    ax.set_ylim(0, y_max)
    #    #if shape:
    #    #     ax.yaxis.set_ticks(np.array([10e-4,10e-3,10e-2,10e-1,10e0]))
    #    #else:
    #    #    ax.yaxis.set_ticks(np.array([10e-2,10e-1,10e0,10e1,10e2,10e3,10e4,10e5,10e6]))


    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    for handle, label in zip(handles, labels):
        #print (handle, label)
        try:
            new_labels.append(my_labels[label])
            if not label=='pseudodata':
                handle.set_color(colors[label])
        except:
            pass

    if rax:
        plt.subplots_adjust(hspace=0)
        rax.set_ylabel('Obs./Pred.')
        rax.set_ylim(0.0,2.0)

    ax.legend(title='',ncol=2,handles=handles, labels=new_labels, frameon=False)

    fig.text(0., 0.995, '$\\bf{CMS}$', fontsize=20,  horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes )
    fig.text(0.15, 1., '$\\it{%s}$'%preliminary, fontsize=14, horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes )
    fig.text(0.65, 1., '$%s fb^{-1}$'%lumi, fontsize=14, horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes )
    fig.text(0.8, 1., '13 TeV', fontsize=14, horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes )

    fig.savefig(os.path.join(outdir, "{}.pdf".format(name)))
    fig.savefig(os.path.join(outdir, "{}.png".format(name)))
    #ax.clear()

colors = {
    #'mC750_l1': '#FF595E',
    'tW_scattering': '#FF595E',
    #'tW_scattering': '#000000',
    'TTW': '#8AC926',
    'TTX': '#FFCA3A',
    'TTZ': '#FFCA3A',
    'TTH': '#34623F',
    'TTTT': '#0F7173',
    'ttbar': '#1982C4',
    'wjets': '#6A4C93',
    'diboson': '#525B76',
    'DY': '#6A4C93',

    'mC750_l1': '#FF595E',
    '1000_1_scan': '#FF595E',
    'LL': '#1982C4',
    'ZNuNu': '#6A0136',
    'QCD': '#989C94',
    'WW': '#FF5714',
    'ttW': '#FFCA3A',
    'ST': '#8AC926',
    'WJets': '#1982C4',
    'TTJets': '#F76F8E',

}


'''
other colors (sets from coolers.com):
#525B76 (gray)
#34623F (hunter green)
#0F7173 (Skobeloff)
'''

my_labels = {
    #'mC750_l1': 'mC750_l1',
    'tW_scattering': 'tW scattering',
    'TTW': r'$t\bar{t}$W+jets',
    'TTX': r'$t\bar{t}$Z/H',
    'TTH': r'$t\bar{t}$H',
    'TTZ': r'$t\bar{t}$Z',
    'TTTT': r'$t\bar{t}t\bar{t}$',
    'ttbar': r'$t\bar{t}$+jets',
    'wjets': 'W+jets',
    'DY': 'Drell-Yan',
    'diboson': 'VV/VVV',

    '1000_1_scan': 'WH (1000,1) FS',
    'LL': 'Lost Lepton',
    'ZNuNu': r'$Z \rightarrow inv$',
    'QCD': 'QCD',
    'WW': 'WW',
    'ttW': r'$t\bar{t}$W+jets',
    'ST': 'ST',
    'WJets': 'W+jets',
    'TTJets': r'$t\bar{t}$+jets',
    #'TTTT': r'$t\bar{t}t\bar{t}$',
    #'DY': 'Drell-Yan',
    'mC750_l1': r'WH',

    'Data': 'Observed',
    'pseudodata': 'Pseudo-data',
    'uncertainty': 'Uncertainty',
}

data_err_opts = {
    'linestyle': 'none',
    'marker': '.',
    'markersize': 10.,
    'color': 'k',
    'elinewidth': 1,
}

signal_err_opts = {
    'linestyle':'-',
    'color':'crimson',
    'elinewidth': 1,
}

#signal_err_opts = {
#    'linestyle': '-',
#    'marker': '.',
#    'markersize': 0.,
#    'color': 'k',
#    'elinewidth': 1,
#    'linewidth': 2,
#}


error_opts = {
    'label': 'uncertainty',
    'hatch': '///',
    'facecolor': 'none',
    'edgecolor': (0,0,0,.5),
    'linewidth': 0
}

fill_opts = {
    'edgecolor': (0,0,0,0.3),
    'alpha': 1.0
}

signal_fill_opts = {
    'linewidth': 2,
    'linecolor': 'k',
    'edgecolor': (1,1,1,0.0),
    'facecolor': 'none',
    'alpha': 0.1
}

fillopts2 = {
    'edgecolor': (0,0,0,0.3),
    'facecolor': [('#1982C4'),('#F76F8E'),('#8AC926'),('#FFCA3A'),('#FF5714'),('#6A0136'),('#989C94')]  
}

