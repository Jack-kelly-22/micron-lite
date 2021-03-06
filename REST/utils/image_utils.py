def get_crop_image(image,boarder):
    """:returns crop image with"""
    y,x,z = image.shape
    bx,by = 800-boarder,600-boarder
    startx = x // 2 - (bx // 2)
    starty = y // 2 - (by // 2)
    cropped = image[starty:starty + by, startx:startx + bx]
    return cropped


def get_thresh_image(image, constants):
    if constants["use_alt"]:
        print("USED ALT THRESH")
        img_seg = get_alt_thresh_image(image, constants["alt_thresh"], constants['fiber_type'])
    else:
        # image = rgb2gray(image)
        print("start regular thresh")
        img_seg = get_reg_thresh_image(image, constants["thresh"], constants['fiber_type'])
    return img_seg


def get_alt_thresh_image(image, alt_thresh, fiber, ):
    image = rgb2gray(image)

    tr = threshold_local(image, 601, 'mean', mode='constant', cval=0, offset=-(alt_thresh / 255.0))

    # print("fiber is ", fiber)
    if fiber == 'dark':
        print("went")
        img_seg = (image >= tr).astype(uint8)
    else:
        print("light fibers")
        img_seg = (image < tr).astype(uint8)

    window_size = 25
    return img_seg


def get_reg_thresh_image(image, threshold, fiber):
    """Performs constant image thresholding"""
    # image = tfImage.adjust_contrast(image,1.5)

    image = rgb2gray(image)
    if fiber == 'dark':
        img_seg = (image > threshold / 255).astype(uint8)
    else:
        img_seg = (image < threshold / 255).astype(uint8)
    return img_seg