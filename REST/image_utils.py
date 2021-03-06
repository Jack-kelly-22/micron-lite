from skimage.draw import set_color
from skimage.io import imsave
from skimage.draw import circle,circle_perimeter,rectangle_perimeter
def color_circle(c,r,image):
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r)
    #set_color(image, (y_ls,x_ls), color=(0, 77, 253))
    set_color(image, (y_ls, x_ls), color=(255, 255, 255))
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r-1)
    set_color(image, (y_ls, x_ls), color=(255, 255, 255))
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r-2)
    set_color(image, (y_ls, x_ls), color=(255, 255, 255))


def color_holes(hole_ls, image):
    #print(len(hole_ls))
    for hole in hole_ls:
        color_circle(hole[4],hole[5],image)
    return image

def color_holes2(hole_ls, image):
    for hole in hole_ls:
        color_circle(hole[0],hole[1],image)
    return image


def add_boarder(image,boarder):
    y, x, z = image.shape
    for i in range(0, 5):
        coords = rectangle_perimeter(start=(boarder//2 + i, boarder//2 + i), end=(y - boarder//2 + i, x - boarder//2 + i))
        set_color(image, coords, (255, 0, 0))

    return image


def save_out_image(image,out_path):
    save_name = '.' + out_path
    imsave(save_name,image)
    print("saved image at",save_name)
    # io.imsave("." + self.image_out_path + "/" + self.name[:-4] + "_out.png", self.out_image)
