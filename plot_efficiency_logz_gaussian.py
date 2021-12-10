# -*- coding: utf-8 -*-

"""
Plotter for evidence as a function of efficiency
"""
if __name__ == "__main__":
    ###############################################################################
    # initial imports:

    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import color_utilities as cu
    import matplotlib.gridspec as gridspec

    ###############################################################################
    # initial setup:

    # output folder:
    out_folder = './paper_plots/'
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # color palette:
    colors = [cu.nice_colors(i) for i in range(10)]

    # latex rendering:
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc('text', usetex=True)

    ###############################################################################
    # pre computations:
    #eff = [1, 0.5, 0.1, 0.05, 0.01]
    #logz = [3.44, 3.82, 1.63, 0.260, -0.118]
    #dlogz = [0.76, 0.76, 0.77, 0.77, 0.77]
    #ins_logz = [-0.44, -0.415, 0.058, -0.446, 0.132]
    #ins_dlogz = [0.0077, 0.00389, 0.004877, 0.006194, 0.004139]
    eff = [1, 0.3, 0.1, 0.03, 0.01]
    mn_logz = np.zeros([5, 10])
    mn_dlogz = np.zeros([5, 10])
    ins_logz = np.zeros([5, 10])
    ins_dlogz = np.zeros([5, 10])

    for i, effi in enumerate(eff):
        d = np.loadtxt('./data/eff'+str(effi)+'.csv', delimiter=',')
        mn_logz[i] = d[:,0]
        mn_dlogz[i] = d[:,1]
        ins_logz[i] = d[:,2]
        ins_dlogz[i] = d[:,3]

    nreps = [15, 30, 60, 120]
    #pc_logz = [-0.22817, -0.11663, -0.13532, 0.03712]
    #pc_dlogz = [0.30747, 0.30300, 0.30493, 0.30719]
    pc_logz = np.zeros([4, 10])
    pc_dlogz = np.zeros([4, 10])
    for i, nr in enumerate(nreps):
        d = np.loadtxt('./data/nr'+str(nr)+'.csv', delimiter=',')
        pc_logz[i] = d[:,0]
        pc_dlogz[i] = d[:,1]

    ###############################################################################
    # do the plot:

    # plot size in cm. Has to match to draft to make sure font sizes are consistent
    x_size = 18
    y_size = 9.0
    main_fontsize = 10.0

    # start the plot:
    fig = plt.gcf()
    fig.set_size_inches( x_size/2.54, y_size/2.54 )
    gs = gridspec.GridSpec(1,2)
    ax1 = plt.subplot(gs[0,0])
    ax2 = plt.subplot(gs[0,1], sharey=ax1)
    plt.setp(ax2.get_yticklabels(), visible=False)
    fig.suptitle("Gaussian Likelihood (known truth)")

    # do the plot:
    for i, ii in enumerate(np.linspace(-0.05, 0.05, 10)):
        ax1.errorbar(10**(np.log10(eff) + ii), mn_logz[:,i], yerr = mn_dlogz[:,i], fmt = '.', color=colors[0], alpha=0.4)
        ax1.errorbar(10**(np.log10(eff) + ii), ins_logz[:,i], yerr = ins_dlogz[:,i], fmt = '.', color='orange', alpha=0.4)

    #ax1.errorbar(eff, logz, yerr = dlogz, fmt = '.', color=colors[0], label=r'MultiNest $\log Z$')
    #ax1.errorbar(eff, ins_logz, yerr = ins_dlogz, fmt = '.', color=colors[1], label=r'MultiNest INS $\log Z$')
    ax1.axhline(0, color='grey', ls = "--", label='Truth')

    # label on the axis:
    ax1.set_xlabel('Efficiency', fontsize=main_fontsize);
    ax1.set_ylabel('$\log Z$', fontsize=main_fontsize);

    ax1.set_xscale('log')

    ax1.title.set_text('Multinest')
    ax2.title.set_text('Polychord')

    # do the plot:
    for i, ii in enumerate(np.linspace(-3.05, 3.05, 10)):
        ax2.errorbar(nreps + ii, pc_logz[:,i], yerr = pc_dlogz[:,i], fmt = '.', color=colors[3], alpha=0.4)
    ax2.axhline(0, color='grey', ls = "--", label='Truth')

    ax2.set_xlabel('Num Repeats', fontsize=main_fontsize);
    ax2.set_xticks([15,30,60,120])
    #ax2.set_xticklabels([15,30,60,120])

    # update dimensions:
    bottom=0.15; top=0.8; left=0.09; right=0.99; wspace=0.03; hspace=0.05
    gs.update( bottom=bottom, top=top, left=left, right=right, wspace=wspace, hspace=hspace )

    # legends:
    leg = ax1.legend(fontsize=0.9 * main_fontsize,
                     frameon=False,
                     fancybox=False,
                     edgecolor='k',
                     ncol=1,
                     borderaxespad=0.0,
                     columnspacing=2.0,
                     handlelength=1.4,
                     loc='upper left',
                     bbox_to_anchor=(0.04, 0.96)
                     )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)

    # save:
    plt.savefig(out_folder+'/figure_efficiency_logz_gaussian.pdf')

    plt.show()