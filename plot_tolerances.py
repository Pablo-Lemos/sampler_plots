# -*- coding: utf-8 -*-

"""
Plotter for tolerances plot
"""

if __name__ == '__main__':

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
    #Read the files

    #chain1 = np.loadtxt("chains/mn-eff03-omp1-tol03_d3y1_w_.txt", usecols = [0])
    #chain2 = np.loadtxt("chains/mn-eff03-omp1_d3y1_w_.txt", usecols = [0])
    #chain3 = np.loadtxt("chains/mn-eff03-omp1-tol001_d3y1_w_.txt", usecols = [0])

    chain1 = np.loadtxt("chains/pc-omp1-tol01-ff01_d3y1_w.txt", usecols = [0])
    chain2 = np.loadtxt("chains/pc-omp1-tol001-ff01_d3y1_w.txt", usecols = [0])
    chain3 = np.loadtxt("chains/pc-omp1-tol1e3-ff01_d3y1_w.txt", usecols = [0])

    ###############################################################################
    # do the plot:

    # plot size in cm. Has to match to draft to make sure font sizes are consistent
    x_size = 18.37
    y_size = 8.0
    main_fontsize = 10.0

    # start the plot:
    fig = plt.gcf()
    fig.set_size_inches( x_size/2.54, y_size/2.54 )
    gs = gridspec.GridSpec(1,3)
    ax1 = plt.subplot(gs[0,0])
    ax2 = plt.subplot(gs[0,1])
    ax3 = plt.subplot(gs[0,2])

    # do the plot:
    ax1.plot(chain1/max(chain1), lw=1., ls='-', color=colors[0], label='Tolerance = 0.1')
    ax2.plot(chain2/max(chain2), lw=1., ls='-', color=colors[0], label='Tolerance = 0.01')
    ax3.plot(chain3/max(chain3), lw=1., ls='-', color=colors[0], label='Tolerance = 0.001')

    # label on the axis:
    ax1.set_xlabel('Sample number', fontsize=main_fontsize);
    ax2.set_xlabel('Sample number', fontsize=main_fontsize);
    ax3.set_xlabel('Sample number', fontsize=main_fontsize);
    ax1.set_ylabel('Normalized Weight', fontsize=main_fontsize);
    plt.draw()

    # the ticks:
    ax1.set_xticklabels( ax1.get_xmajorticklabels(), horizontalalignment='center', fontsize=0.9*main_fontsize);
    ax2.set_xticklabels( ax2.get_xmajorticklabels(), horizontalalignment='center', fontsize=0.9*main_fontsize);

    #
    # the y ticks:
    ax2.set_yticks([]);
    ax3.set_yticks([]);

    ax1.set_xticks([]);
    ax2.set_xticks([]);
    ax3.set_xticks([]);


    # title:
    ax1.set_title('PolyChord, tolerance = 0.1')
    ax2.set_title('PolyChord, tolerance = 0.01')
    ax3.set_title('PolyChord, tolerance = 0.001')

    # update dimensions:
    bottom=0.1; top=0.89; left=0.09; right=0.99; wspace=0.03; hspace=0.05
    gs.update( bottom=bottom, top=top, left=left, right=right, wspace=wspace, hspace=hspace )

    # save:
    plt.savefig(out_folder+'/figure_tolerances.pdf')

    plt.show()