from numpy import histogram,hsplit,vsplit,average
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import zscore





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

