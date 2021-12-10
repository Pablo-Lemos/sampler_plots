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
    from scipy.stats import multivariate_normal
    from matplotlib.patches import Ellipse
    import matplotlib.transforms as transforms

    ###############################################################################
    # initial setup:

    # output folder:
    out_folder = './paper_plots/'
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # color palette:
    colors = [cu.nice_colors(i) for i in range(4)]

    np.random.seed(2)


    # latex rendering:
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc('text', usetex=True)

    ###############################################################################
    # pre computations:
    def confidence_ellipse(x, y, ax, cov=False, small=True, n_std=3.0, facecolor='none', **kwargs):
        """
        Create a plot of the covariance confidence ellipse of `x` and `y`

        Parameters
        ----------
        x, y : array_like, shape (n, )
            Input data.

        ax : matplotlib.axes.Axes
            The axes object to draw the ellipse into.

        n_std : float
            The number of standard deviations to determine the ellipse's radiuses.

        Returns
        -------
        matplotlib.patches.Ellipse

        Other parameters
        ----------------
        kwargs : `~matplotlib.patches.Patch` properties
        """
        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        if cov:
            cov = np.cov(x, y)
        else:
            if small:
                cov = np.array([[1.27424495, -0.0793614], [-0.0793614, 0.85767217]])
            else:
                cov = 1.2 * np.array([[1.27424495, -0.0793614], [-0.0793614, 0.85767217]])

        pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
        # Using a special case to obtain the eigenvalues of this
        # two-dimensionl dataset.
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        ellipse = Ellipse((0, 0),
                          width=ell_radius_x * 2,
                          height=ell_radius_y * 2,
                          facecolor=facecolor,
                          **kwargs)

        # Calculating the stdandard deviation of x from
        # the squareroot of the variance and multiplying
        # with the given number of standard deviations.
        scale_x = np.sqrt(cov[0, 0]) * n_std
        mean_x = 0  # np.mean(x)

        # calculating the stdandard deviation of y ...
        scale_y = np.sqrt(cov[1, 1]) * n_std
        mean_y = 0  # np.mean(y)

        transf = transforms.Affine2D() \
            .rotate_deg(45) \
            .scale(scale_x, scale_y) \
            .translate(mean_x, mean_y)

        ellipse.set_transform(transf + ax.transData)
        return ellipse


    # Calculate 1 2 3 sigma

    z = np.random.multivariate_normal(mean=[0, 0], cov=np.identity(2), size=100000)
    rv = multivariate_normal(np.zeros(2), np.identity(2))

    s1 = np.sort(rv.pdf(z))[int((1 - 0.68) * 100000)]
    s2 = np.sort(rv.pdf(z))[int((1 - 0.95) * 100000)]
    s3 = np.sort(rv.pdf(z))[int((1 - 0.997) * 100000)]

    xx = np.random.multivariate_normal(mean=[0, 0], cov=np.identity(2), size=101)
    xx = np.delete(xx, np.where(rv.pdf(xx) == min(rv.pdf(xx))), 0)
    xx = np.delete(xx, np.where(rv.pdf(xx) == min(rv.pdf(xx))), 0)
    xx = np.concatenate([xx, np.array([[-3.3, 1]])])

    ###############################################################################
    # do the plot:

    # plot size in cm. Has to match to draft to make sure font sizes are consistent
    x_size = 18
    y_size = 12.0
    main_fontsize = 10.0

    # start the plot:
    fig = plt.gcf()
    fig.set_size_inches( x_size/2.54, y_size/2.54 )
    gs = gridspec.GridSpec(2,2)
    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(gs[0, 1])
    ax3 = plt.subplot(gs[1, 0])
    ax4 = plt.subplot(gs[1, 1])

    ax1.set_yticks([])
    ax1.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax3.set_yticks([])
    ax3.set_xticks([])
    ax4.set_yticks([])
    ax4.set_xticks([])

    ax2.set_yticklabels([])
    ax4.set_yticklabels([])

    # First plot
    x = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, x)
    Z = 1 / (2 * np.pi) * np.exp(-(np.power(X, 2) + np.power(Y, 2)) / 2)
    cs = ax1.contour(X, Y, Z, levels=[s3, s2, s1])

    fmt = {}
    strs = [r'$3 \sigma$', r'$2 \sigma$', r'$1 \sigma$']
    for l, s in zip(cs.levels, strs):
        fmt[l] = s

    #plt.gca().axis('equal')
    cs.collections[0].set_label('True Posterior')
    ax1.clabel(cs, fontsize=main_fontsize, inline=1, fmt=fmt)

    # Second plot
    cs = ax2.contour(X, Y, Z, levels=[s3, s2, s1])
    ax2.clabel(cs, fontsize=main_fontsize, inline=1, fmt=fmt)
    ax2.scatter(xx[:, 0], xx[:, 1], marker='.', color='red', label = 'MultiNest live points')

    # Third plot
    ax3.scatter(xx[:, 0], xx[:, 1], marker='.', color='red')
    cs = ax3.contour(X, Y, Z, levels=[s3, s2, s1])
    ellipse = confidence_ellipse(xx[:, 0], xx[:, 1], ax3, edgecolor='red', linestyle='--', label = 'MultiNest ellipse')
    ax3.add_patch(ellipse)
    ax3.clabel(cs, fontsize=main_fontsize, inline=1, fmt=fmt)

    # Fourth plot
    ellipse1 = confidence_ellipse(xx[:, 0], xx[:, 1], ax4, small=False, edgecolor='red', color='white', linestyle='--')
    ellipse2 = confidence_ellipse(z[:, 0], z[:, 1], ax4, cov=True, n_std=3.4, color='blue', alpha=0.2)
    ax4.add_patch(ellipse2)
    ax4.add_patch(ellipse1)
    ellipse3 = confidence_ellipse(xx[:, 0], xx[:, 1], ax4, edgecolor='red', linestyle='--')
    ax4.add_patch(ellipse3)
    ellipse4 = confidence_ellipse(xx[:, 0], xx[:, 1], ax4, small=False, edgecolor='orange', linestyle='-.', label = 'MultiNest expanded ellipse')
    ax4.add_patch(ellipse4)

    ax4.scatter(xx[:, 0], xx[:, 1], marker='.', color='red', zorder=10)
    cs = ax4.contour(X, Y, Z, levels=[s3, s2, s1])
    ax4.clabel(cs, fontsize=main_fontsize, inline=1, fmt=fmt)

    # update dimensions:
    bottom=0.01; top=0.99; left=0.01; right=0.99; wspace=0.03; hspace=0.05
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
                     )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)

    # legends:
    leg = ax2.legend(fontsize=0.9 * main_fontsize,
                     frameon=False,
                     fancybox=False,
                     edgecolor='k',
                     ncol=1,
                     borderaxespad=0.0,
                     columnspacing=2.0,
                     handlelength=1.4,
                     loc='upper right',
                     )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)

    # legends:
    leg = ax3.legend(fontsize=0.9 * main_fontsize,
                     frameon=False,
                     fancybox=False,
                     edgecolor='k',
                     ncol=1,
                     borderaxespad=0.0,
                     columnspacing=2.0,
                     handlelength=1.4,
                     loc='upper left',
                     )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)

    # legends:
    leg = ax4.legend(fontsize=0.9 * main_fontsize,
                     frameon=False,
                     fancybox=False,
                     edgecolor='k',
                     ncol=1,
                     borderaxespad=0.0,
                     columnspacing=2.0,
                     handlelength=1.4,
                     loc='upper right',
                     )
    leg.get_frame().set_linewidth('0.8')
    leg.get_title().set_fontsize(main_fontsize)


    # save:
    plt.savefig(out_folder+'/figure_multinest.pdf')

    plt.show()