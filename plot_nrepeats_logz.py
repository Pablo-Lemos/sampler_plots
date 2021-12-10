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
    colors = [cu.nice_colors(i) for i in range(4)]

    # latex rendering:
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc('text', usetex=True)

    ###############################################################################
    # pre computations:
    nrepeats = [15, 30, 60, 120]
    logz = [-281.54, -282.52, -282.09, -282.34]
    dlogz = [0.18, 0.19, 0.18, 0.18]

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
    ax1.errorbar(nrepeats, logz, yerr = dlogz, fmt = '.', color=colors[3], label='PolyChord')
    ax1.axhspan(-282.34 - 0.18, -282.34 + 0.18, color='grey', alpha=0.4, label='PolyChord best')

    ticks = [15, 30, 60, 120]
    ax1.set_xticks(ticks);

    # label on the axis:
    ax1.set_xlabel('Num Repeats', fontsize=main_fontsize);
    ax1.set_ylabel('$\log Z$', fontsize=main_fontsize);

    # update dimensions:
    bottom=0.15; top=0.99; left=0.22; right=0.99; wspace=0.03; hspace=0.05
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
                     bbox_to_anchor=(0.54, 0.96)
                     )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)

    # save:
    plt.savefig(out_folder+'/figure_nrepeats_logz.pdf')

    plt.show()