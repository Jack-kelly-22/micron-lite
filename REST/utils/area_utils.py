from numpy import pad,dstack,where
from skimage.draw import disk

def remove_z_set(coord_set):
    """Converts tuple of lists of ares into set and removes z"""
    x_y = set()
    for coord in coord_set:
        x_y.add((coord[1],coord[0]))
    return x_y


def check_circle(circle_pts,area_pts):
    if(circle_pts.issubset(area_pts)):
        return True
    else:
        if(len(circle_pts-area_pts)<4):
            return True
    return False


def try_circle(coords, middle,size):
    """Attempts to place circle with radius of size at coords middle
    Parameters:
        coords:
    """
    go = True
    i = size
    area_pts = set()
    ls_x,ls_y = [],[]
    while go:
        ls_x,ls_y = disk((middle[0],middle[1]),i)
        j = 0
        circle_pts = {(ls_x[k],ls_y[k]) for k in range(1,len(ls_x))}
        if not check_circle(circle_pts,coords):
            go = False
        i = i + 1
    return i-1,(middle[0],middle[1])


def get_largest_circle_in_region(coords,max = 1,centroid= None):
    """ calculates the largest circle that will fit in the
    region defined by reg_tup
    Parameters:
        reg_tup(tuple): details about pore
    Returns:
        tup: (center,radius,points)"""
    center = [0,0]
    reg_coords = coords
    n = 0
    coord_set = coords
    i = max
    #coord_set = {(reg_coords[j][0],reg_coords[j][1]) for j in range(0,len(coords))}
    for pt in reg_coords:
        if centroid is not None:
            pt = (centroid[0], centroid[1])
            #print("testing centroid:", pt, " first")
            centroid = None
            center=pt
        n, pts = try_circle(coord_set, pt, max)
        if (n > max):
            max = n
            max_pts = pts
            center = pt

    #print("found max-:", max)
    return center,max,


def sum_images(colored,original,boarder):
    r_cons, g_cons, b_cons = [0, 0, 0]
    r_, g_, b_ = colored[:, :, 0], colored[:, :, 1], colored[:, :, 2]
    rb = pad(array=r_, pad_width=boarder // 2, mode='constant', constant_values=r_cons)
    gb = pad(array=g_, pad_width=boarder // 2, mode='constant', constant_values=g_cons)
    bb = pad(array=b_, pad_width=boarder // 2, mode='constant', constant_values=b_cons)
    padded = dstack(tup=(rb, gb, bb))

    return where(padded!=0,padded,original)

def check_circle(circle_pts,area_pts):
    if(circle_pts.issubset(area_pts)):
        return True
    else:
        if(len(circle_pts-area_pts)<5):
            return True
    return False