# -*- coding: utf-8 -*-

"""
Plotter for evidence as a function of efficiency
"""
if __name__ == "__main__":
    ###############################################################################
    # initial imports:

    import os
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
    colors = [cu.nice_colors(i) for i in range(4)]

    # latex rendering:
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc('text', usetex=True)

    ###############################################################################
    # pre computations:
    eff = [1, 0.5, 0.1, 0.05, 0.01]
    logz = [3.44, 3.82, 1.63, 0.260, -0.118]
    dlogz = [0.76, 0.76, 0.77, 0.77, 0.77]
    ins_logz = [-0.44, -0.415, 0.058, -0.446, 0.132]
    ins_dlogz = [0.0077, 0.00389, 0.004877, 0.006194, 0.004139]

    ###############################################################################
    # do the plot:

    # plot size in cm. Has to match to draft to make sure font sizes are consistent
    x_size = 8.99
    y_size = 7.0
    main_fontsize = 10.0

    # start the plot:
    fig = plt.gcf()
    fig.set_size_inches( x_size/2.54, y_size/2.54 )
    gs = gridspec.GridSpec(1,1)
    ax1 = plt.subplot(gs[0,0])

    # do the plot:
    ax1.errorbar(eff, logz, yerr = dlogz, fmt = '.', color=colors[0], label=r'MultiNest $\log Z$')
    ax1.errorbar(eff, ins_logz, yerr = ins_dlogz, fmt = '.', color=colors[1], label=r'MultiNest INS $\log Z$')
    ax1.axhline(0, color=colors[2], ls = "--", label='Truth')

    # scale:
    #ax1.set_ylim([0.0,0.5])
    #ax2.set_ylim([0.0,0.5])

    # label on the axis:
    ax1.set_xlabel('Efficiency', fontsize=main_fontsize);
    ax1.set_ylabel('$\log Z$', fontsize=main_fontsize);

    ax1.set_xscale('log')

    # update dimensions:
    bottom=0.15; top=0.99; left=0.19; right=0.99; wspace=0.03; hspace=0.05
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