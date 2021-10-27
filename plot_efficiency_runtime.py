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

    #os.environ["PATH"] += os.pathsep + "/usr/local/texlive/2021/bin/universal-darwin"
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
    eff = [1, 0.3, 0.1, 0.01, 0.001]
    runtime = [13.8, 16.2, 23.7, 39.3, 109.5]

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
    ax1.errorbar(eff, runtime, fmt = '.', color=colors[0])

    # label on the axis:
    ax1.set_xlabel('Efficiency', fontsize=main_fontsize);
    ax1.set_ylabel('Runtime (hours)', fontsize=main_fontsize);

    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # update dimensions:
    bottom=0.15; top=0.99; left=0.19; right=0.99; wspace=0.03; hspace=0.05
    gs.update( bottom=bottom, top=top, left=left, right=right, wspace=wspace, hspace=hspace )

    # save:
    plt.savefig(out_folder+'/figure_efficiency_runtime.pdf')

    plt.show()