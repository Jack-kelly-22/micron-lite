from skimage.measure import label,regionprops
import os
from skimage.io import imread
from REST.utils import image_utils
from REST.utils import area_utils
from math import pi
from porespy.metrics import porosity
from uuid import uuid4
from cv2 import resize,INTER_AREA
class SimpleImage:

    def __init__(self,image_dic,options):
        self.image_data = imread(image_dic["img_path"])
        image_dic["id"] = str(uuid4()).replace('-','')
        self.image_data_backup=self.image_data
        self.options = options
        self.image_dic = image_dic
        self.image_dic['img_name'] = os.path.basename(os.path.normpath(self.image_dic['img_path']))
        self.constants = options['constants']
        self.prep_image()
        self.violated_circles = []
        self.out_image = self.image_data
        regions = self.get_regions()
        self.image_dic['largest_pore'] = 0
        self.image_dic['pass'] = self.is_pass(regions)

        if not self.image_dic['pass']:
            self.not_pass()

    def get_dic(self):
        print(self.image_dic)
        return self.image_dic

    def set_porosity(self,img_seg):
        self.image_dic['porosity'] = porosity(img_seg)

    def get_image_dic(self):
        return self.image_dic

    def not_pass(self):
        """
        saves original image with circles overlayed
        sets pass to false
        adds circles to image_dic
        """

        if self.constants['crop']:
            i=0
            while i<len(self.violated_circles):
                center = (self.violated_circles[i][0][0]+(self.constants['boarder']//2),self.violated_circles[i][0][1]+(self.constants['boarder']//2))
                self.violated_circles[i][0] = center
                i += 1
            self.out_image = area_utils.sum_images(self.out_image,self.image_data_backup,self.constants['boarder'])
            self.out_image = image_utils.add_boarder(self.out_image,self.constants['boarder'])

        #adds violated circles to image_dic
        self.image_dic['violated_circles'] = self.violated_circles
        #count the number of circles that violated rules
        self.image_dic['num_violated'] = len(self.violated_circles)
        #color circles that violated guidlines
        self.out_image = image_utils.color_holes2(self.violated_circles,self.out_image,float(self.constants['scale']))

        #save resulting image
        folder = os.path.basename(os.path.dirname(self.image_dic['img_path']))
        image_utils.save_out_image(self.out_image,
                                   './job-data/'+self.options['job_name']+'/'+folder+'/'+ os.path.basename(os.path.normpath(self.image_dic['img_path'])))


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
        large_reg=list(filter(lambda reg: reg['area']*scale_area>min_area,regions))
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
        r*=2
        r*=scale_r

        if r>self.image_dic['largest_pore']:
            self.image_dic['largest_pore']=r
        if not r <= max_diam:
            print("FAILED R:",r ,"Microns")
            self.violated_circles.append([center,r])
        return r<=max_diam

    def get_regions(self):
        img_seg = image_utils.get_thresh_image(self.image_data,self.constants)
        scale_area = float(self.constants['scale']) ** 2
        label_image = label(img_seg)
        regions = regionprops(label_image)
        if self.constants['debug']:
            print("DEBUG MODE COLOR IMAGE")
            self.out_image = image_utils.color_out_image(regions,self.out_image)
        self.set_porosity(img_seg)
        regions = list(filter(lambda reg: reg['area'] * scale_area > self.constants['min_ignore'],regions))
        regions = sorted(regions,key=lambda reg:reg['area'], reverse=True)
        return regions

    def prep_image(self):
        """does necessary operations to image before processing areas"""
        self.image_data=resize(self.image_data, dsize = (800,600), interpolation = INTER_AREA)
        if self.constants['crop']:
            self.image_data = image_utils.get_crop_image(self.image_data,self.constants['boarder'])

