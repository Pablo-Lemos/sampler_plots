# -*- coding: utf-8 -*-

"""
Plotter for figure 1
"""

if __name__ == "__main__":
    ###############################################################################
    # initial imports:

    import os
    import getdist.plots as gplot
    import getdist.mcsamples as mcsamples
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import color_utilities as cu

    ###############################################################################
    # initial setup:

    # output folder:
    out_folder = './paper_plots/'
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # getdist settings:
    # https://getdist.readthedocs.io/en/latest/analysis_settings.html
    analysis_settings = {
                         'ignore_rows': 0,
                         'contours': [0.68, 0.95, 0.997],
                         'fine_bins': 2048,
                         'fine_bins_2D': 2048,
                         'smooth_scale_1D': -1,
                         'smooth_scale_2D': -1,
                         'boundary_correction_order': 1,
                         'mult_bias_correction_order': 1,
                        }

    # color palette:
    colors = [cu.nice_colors(i) for i in range(4)]

    # latex rendering:
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc('text', usetex=True)

    ###############################################################################
    # generate the two test chains:

    chain_1 = mcsamples.loadMCSamples("chains/mn-eff1-omp1_d3y1_w_")
    chain_2 = mcsamples.loadMCSamples("chains/mn-eff03-omp1_d3y1_w_")
    chain_3 = mcsamples.loadMCSamples("chains/mn-eff01-omp1_d3y1_w_")
    chain_4 = mcsamples.loadMCSamples("chains/mn-eff001-omp1_d3y1_w_")
    chain_5 = mcsamples.loadMCSamples("chains/mn-eff1e3-omp1_d3y1_w_")
    ###############################################################################
    # do the plot:

    # plot size in cm. Has to match to draft to make sure font sizes are consistent
    x_size = 8.99
    y_size = 8.5
    main_fontsize = 10.0

    # create the getdist plotter and set all the settings we need:
    g = gplot.getSubplotPlotter(width_inch=x_size/2.54)
    g.settings.num_plot_contours = 2
    g.settings.solid_contour_palefactor = 0.6
    g.settings.alpha_factor_contour_lines = 1.0
    g.settings.fontsize = main_fontsize
    g.settings.axes_fontsize = 0.9*main_fontsize
    g.settings.lab_fontsize = main_fontsize
    g.settings.legend_fontsize = 0.9*main_fontsize
    g.settings.figure_legend_loc = 'upper right'
    g.settings.figure_legend_ncol = 1
    g.settings.legend_frame = True
    g.settings.axis_marker_lw = 1.
    g.settings.x_label_rotation = 0.
    g.settings.lw_contour = 1.

    # plot the chains:
    g.triangle_plot([chain_5, chain_1],
                    ['omega_m', 'sigma_8', 'w'],
                    contour_colors=colors,
                    contour_ls=['-', '--', '-', '-'],
                    contour_lws=[1., 1., 1., 1.],
                    filled=False, no_tight=True
                    )

    # ticks:
    for _row in g.subplots:
        for _ax in _row:
            if _ax is not None:
                _ax.tick_params('both', length=2.5, width=.8,
                                which='major', zorder=999,
                                labelsize=0.9*main_fontsize)
                _ax.xaxis.label.set_size(main_fontsize)
                _ax.yaxis.label.set_size(main_fontsize)

    # update the settings:
    g.fig.set_size_inches(x_size/2.54, y_size/2.54)

    # set the legend (note we remove the getdist one and make it from scratch):
    g.legend.remove()

    leg_handlers = [mpatches.Patch(color=colors[0]),
                    mpatches.Patch(color=colors[1]), ]
    legend_labels = ['Efficiency=$10^{-3}$', 'Efficiency=$1$']

    # legend for the second plot:
    leg = g.fig.legend(handles=leg_handlers,
                       labels=legend_labels,
                       fontsize=0.9*main_fontsize,
                       frameon=True,
                       fancybox=False,
                       edgecolor='k',
                       ncol=1,
                       borderaxespad=0.0,
                       columnspacing=2.0,
                       handlelength=1.4,
                       loc='upper right',
                       bbox_to_anchor=(0.0, 0.0, 0.9, 0.9),
                       )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)

    # update dimensions:
    bottom = 0.12
    top = 0.99
    left = 0.15
    right = 0.99
    wspace = 0.
    hspace = 0.
    g.gridspec.update(bottom=bottom, top=top, left=left, right=right,
                      wspace=wspace, hspace=hspace)
    leg.set_bbox_to_anchor((0.0, 0.0, right, top))

    # save:
    g.fig.savefig(out_folder+'/figure_efficiency_contours.pdf')

    plt.show()