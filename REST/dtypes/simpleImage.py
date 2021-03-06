from skimage.measure import label,regionprops
from os import listdir
from skimage.io import imread
# from skimage.util import r
from REST.utils import image_utils
from REST import area_utils
from math import pi
from porespy.metrics import porosity
from cv2 import resize
class SimpleImage:

    def __init__(self,image_dic,options):
        self.image_data = imread(image_dic["img_path"])
        self.image_data_backup=self.image_data
        self.options = options
        self.image_dic = image_dic
        self.constants = options['constants']
        self.prep_image()
        self.violated_circles = []
        self.out_image = None
        regions = self.get_regions()
        img_pass = self.is_pass(regions)

        if not img_pass:
            self.not_pass()

    def set_porosity(self,img_seg):
        self.image_dic['porosity'] = porosity(img_seg)

    def get_image_dic(self):
        return self.image_dic

    def not_pass(self):
        """
        saves original image with circles overlayed
        sets pass to false
        adds cirlces to image_dic
        """

        if self.constants['crop']:
            i=0
            while i<len(self.largest_holes):
                center = (self.largest_holes[i][0][0]+self.constants['boarder'],self.largest_holes[i][0][1]+self.constants['boarder'])
                self.largest_holes[i][0]=center
                i+=1
            self.out_image = area_utils.sum_images(self.out_image,self.out_image,self.constants['boarder'])
            self.out_image = image_utils.add_boarder(self.out_image,self.constants['boarder'])


        #set pass value to false
        self.image_dic['pass'] = False
        #adds violated circles to image_dic
        self.image_dic['violated_circles'] = self.violation
        #count the number of circles that violated rules
        self.image_dic['num_violated'] = len(self.violated)
        #color circles that violated guidlines
        self.out_image = image_utils.color_holes2(self.violated,self.image_data)
        #save resulting image


        image_utils.save_out_image(self.out_image,self.image_dic['out_path'])


    def is_pass(self,regions):
        """Check if image meets porosity requirements and max pore size limit
        if area larger then max allowed is detected all areas larger than max appended
        to violated circles"""
        go = True
        scale_area = float(self.constants["scale"]) ** 2
        #calculate the min area of a circle larger then max diameter
        min_area = (self.constants['max_allowed']/2) ** 2 * pi
        large_reg = regions
        #remove regions with area smaller than the min_area
        large_reg.filter(lambda reg: reg['area']*scale_area>min_area)
        for region in large_reg:
            if go:
                go = self.area_pass(region)
            else:
                self.area_pass(region)
        if not go:
            self.image_dic['fail_reason'].append("Circle found exceeding limit")
        #fail image if porosity is greater than max porosity
        if self.image_dic['porosity']>self.constants['max_porosity']:
            go = False
            self.image_dic['fail_reason'].append("Porosity too high")
        #fail image if porosity is less than min porosity
        if self.image_dic['porosity']<self.constants['min_porosity']:
            go = False
            self.image_dic['fail_reason'].append("Porosity too low")
        return go

    def area_pass(self,region):
        """determines if size of largest circle in region violates guidelines
        Parameters:
            region(regionprops): dataframe of aspects of region
        Returns:
            True/False if region violates guidelines
        """
        scale_r = float(self.constants['scale'])
        max_diam = self.constants['max_allowed']
        coords = area_utils.remove_z_set(region['coords'])
        center,r = area_utils.get_largest_circle_in_region(coords)
        #convert r(px) => r(microns)
        r*=scale_r
        if not r<=max_diam:
            print("FAILED R:",r ,"Microns")
            self.violated_circles.append([center,r])
        return r<=max_diam

    def get_regions(self):
        img_seg = image_utils.get_thresh_image(self.image_data,self.constants)
        scale_area = float(self.constants['scale'])**2
        label_image = label(img_seg)
        regions = regionprops(label_image)
        self.set_porosity(img_seg)
        regions.filter(lambda reg: reg['area']*scale_area >self.constants['min_ignore'])
        regions.sort(lambda reg:reg['area'],reverse=True)
        return regions

    def prep_image(self):
        """does necessary operations to image before processing areas"""
        self.image_data=resize(self.image_data, dsize =(800,600), interpolation = cv2.INTER_AREA)
        if self.constants['crop']:
            self.image_data = image_utils.get_crop_image(self.image_data,self.constants['boarder'])











