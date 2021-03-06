#file contains values to be used as default parameters
class constants:
  def __init__(self):
    constants1 = {
      "thresh": 200,
      "fiber_type": 'dark',
      "use_alt": False,
      "multi": False,
      "alt_thresh": 55,
      "min_ignore": 10,
      "warn_size": 5000,
      "scale": 2.59,
      "num_circles": 100,
      "crop": False,
      "boarder": 0,
      "max_allowed":100,
      'min_porosity':0.2,
      'max_porosity':0.9
    }

    self.version = {
      'version': '2.0.3'
    }

    self.default_options = {
      "program_type": "light",
      "input_type": 0,
      "job_name": "default_name",
      "frame_paths": [],
      "constants": constants1,
      "tags": ["NULL(lol)"],
      "out_path": ''

    }
    self.frame_dic = {}

    self.image_dic = {
      "img_path":'',
      "pass": False,
      'img_name':'',
      "fail_reason":[],
      "largest_pore":0,
      "porosity":0,
      "avg_pore":0,
      "out_path":'./job_data',
      "num_violated": 0,
      "violated_pores":[]
    }

  def get_image_dic(self):
    image_dic = {
      "img_path":'',
      "pass": False,
      'img_name':'',
      "fail_reason":[],
      "largest_pore":0,
      "porosity":0,
      "avg_pore":0,
      "out_path":'./job_data',
      "num_violated": 0,
      "violated_pores":[]
    }
    return image_dic

