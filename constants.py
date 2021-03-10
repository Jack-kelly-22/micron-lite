#file contains values to be used as default parameters
class constants:
  def __init__(self):
    constants1 = {
      "thresh": 120,
      "fiber_type": 'dark',
      "use_alt": False,
      "multi": True,
      "alt_thresh": 55,
      "min_ignore": 10,
      "warn_size": 5000,
      "scale": 2.59,
      "num_circles": 100,
      "crop": False,
      "boarder": 100,
      "max_allowed":50,
      'min_porosity':0.2,
      'max_porosity': 0.09,
      'max_diam':50,
      'num_images':0,
      "debug":True
    }

    self.version = {
      'version': '3.0.3'
    }

    self.default_options = {
      "program_type": "dark",
      "simple":True,
      "version": '3.0.3',
      "input_type": 0,
      "job_name": "default_name",
      "frame_paths": [],
      'frames':[],
      "constants": constants1,
      "tags": ["NULL"],
      "largest_pore": 0,
      "out_path": "/job-data/",
      # 'max_porosity':0.9,
      "num_images":0
    }
    # self.frame_dic = {}

    self.image_dic = {
      "img_path":'',
      "pass": False,
      'img_name':'',
      "fail_reason":[],
      "largest_pore":0,
      "porosity":0,
      "all_areas":[],
      "largest_holes":[],
      "avg_pore":0,
      # "out_path":'./job-data',
      "num_violated": 0,
      "violated_pores":[]
    }

  def get_image_dic(self):
    image_dic = {
      "img_path":'',
      "pass": False,
      'img_name':'',
      "fail_reason":[],
      "largest_pore":0.0,
      "porosity":0,
      "avg_pore":0,
      "out_path":'./job-data',
      "num_violated": 0,
      "violated_pores":[]
    }
    return image_dic

