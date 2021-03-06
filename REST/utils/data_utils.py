from numpy import histogram,hsplit,vsplit,average
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import zscore




def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """
    plt.figure(figsize=(3,len(data[0])*2))
    if not ax:
        ax = plt.gca()


    # Plot the heatmap
    #ax.figure(figsize=(3,len(data)))
    data = np.transpose(data)
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)

    #cbar.make_axes(ax,'left')
    #cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom",)


    # We want to show all ticks...
    #ax.set_xticks(np.arange(data.shape[1]))
    #ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Let the horizontal axes labeling appear on top.
    #ax.tick_params(top=True, bottom=False,
    #               labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")
    plt.subplots_adjust(top=0.9,left=0)

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar



def get_histogram(areas,scale,ignore=20):
    new_areas = [area * (scale*scale) for area in areas]
    filtered = list(filter(lambda x: x>ignore,new_areas))
    hist,bins = histogram(filtered,30)
    print(hist)
    return hist,bins



def split_up_image(image,num = 8):
    img_grid = []
    pore_grid = []
    h_img = vsplit(image,num)
    for row in h_img:
        cols = hsplit(row,num)
        pore_row=[]
        for cell in cols:
            print("Average is:", average(cell))
            pore_row.append(average(cell))
        pore_grid.append(pore_row)
        img_grid.append(cols)
    z_pore_grid = zscore(pore_grid)
    return img_grid,pore_grid,z_pore_grid

