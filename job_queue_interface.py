#file is reasponsible for user interface
import os
import tkinter as tk
from tkinter import filedialog
import requests
from REST.dtypes.Job import Job
from REST.dtypes.db_helper import Db_helper
from SpreadWriter import SpreadWriter
from interface.ScrollableFrame import ScrollableFrame
# from utils import default_settings
from constants import constants
import queue
import threading
import asyncio
# Function for opening the
# file explorer window
class Interface():
    def __init__(self,async_loop):
        self.thread_queue = queue.Queue()
        self.base_folder = ""
        self.added_folders = []
        self.output_folder = ""
        self.include_list = []
        self.async_loop = async_loop
        self.root = tk.Tk()
        self.root.title('Porosity Calculator')
        self.x_start = 0
        self.y_start = 0
        # Set window size
        self.root.geometry("800x500")
        # Set window background color
        self.root.config()
        # self.options = default_settings.get_default_options()
        self.options = constants().default_options
        self.thresh_var = tk.StringVar(value=str(self.options['constants']['thresh']))
        self.fiber_var = tk.StringVar(value=str('dark'))
        self.min_var = tk.StringVar(value=self.options['constants']['min_ignore'])
        self.scale_var = tk.StringVar(value=str(self.options['constants']['scale']))
        self.multi_var = tk.BooleanVar(value=self.options['constants']['multi'])
        self.local_var = tk.BooleanVar(value=self.options['constants']['use_alt'])
        self.crop_var = tk.BooleanVar(value= self.options['constants']['crop'])
        self.boarder_var = tk.StringVar(value=self.options['constants']['boarder'])
        self.name_var = tk.StringVar(value=self.options['job_name'])
        self.num_var = tk.StringVar(value=self.options['constants']['num_circles'])
        self.warn_var = tk.StringVar(value=self.options['constants']['warn_size'])
        self.job_num = tk.StringVar(value= "0")
        self.min_pore = tk.StringVar(value=self.options['constants']['min_porosity'])
        self.max_pore = tk.StringVar(value=self.options['constants']['max_porosity'])
        self.max_diam = tk.StringVar(value=self.options['constants']['max_diam'])
        self.options['constants']['min_ignore'] = tk.StringVar()
        font_1 = "Verdana 22 bold"
        font_2 = "Verdana 16"
        self.frame = ScrollableFrame(self.root)
        label = tk.Label(self.root, text="Frames",font = font_1).place(x=10, y=20)
        button = tk.Button(self.root, text="Select Frames", command=self.browseFiles).place(x=230, y=20)
        # output dirrectory button
        # button = tk.Button(self.root, text="Select Folder", command=self.browseOutput).place(x=170, y=350)
        button = tk.Button(self.root, text="Add Job To Queue", command=self.execute_outputs).place(x=250, y=470)

        #setup constants areas
        x_const = 400
        y_const = 30
        y_space = 40
        contants_header = tk.Label(self.root,text="Options",font=font_1).place(x=x_const+140,y=y_const)
        y_const+=60
        fiber_type = tk.OptionMenu(self.root, self.options['constants']['fiber_type'], "Dark", "Light", "Circles")
        mutli_text = tk.Label(self.root,text="Multi-color",).place(x=x_const+30,y=y_const)
        multi_check = tk.Checkbutton(self.root,variable=self.multi_var).place(x=x_const, y=y_const)
        local_text = tk.Label(self.root, text="Local Thresholding").place(x=x_const + 230, y=y_const)
        local_check = tk.Checkbutton(self.root).place(x=x_const + 200, y=y_const)
        y_const = y_const + 30
        thresh_text = tk.Label(self.root, text= "Threshold",font=font_2).place(x=x_const,y=y_const)
        thresh_val = tk.Entry(self.root,textvariable = self.thresh_var,
                              ).place(x=540,y=y_const, width=50)
        y_const+=y_space
        ignore_text = tk.Label(self.root, text="Size to ignore(microns)").place(x=x_const,y=y_const)
        ignore_val = tk.Entry(self.root,
                              textvariable=self.min_var
                            ).place(x=540,y=y_const,width=50)

        y_const+=y_space
        circles_text = tk.Label(self.root, text="Circles to Draw").place(x=x_const,y=y_const)
        circles_label = tk.Entry(self.root,
                              width="30",
                              textvariable=self.num_var
                            ).place(x=540,y=y_const,width=50)
        y_const+=y_space
        crop_text = tk.Label(self.root, text="Crop boarder").place(x=x_const,y = y_const)
        scale_entry = tk.Entry(self.root,

                               textvariable=self.boarder_var,
                               ).place(x=540, y=y_const, width=50)
        y_const+=y_space

        scale_text = tk.Label(self.root, text="Scale(microns/px)").place(x=x_const, y=y_const)
        scale_entry = tk.Entry(self.root,
                                 width="30",
                                 textvariable=self.scale_var
                                 ).place(x=540, y=y_const, width=50)
        y_const+=y_space
        warn_text = tk.Label(self.root, text="warn size(microns)").place(x=x_const, y=y_const)
        warn_entry = tk.Entry(self.root,
                               width="30",
                               textvariable=self.warn_var
                               ).place(x=540, y=y_const, width=50)

        # clear_frames = tk.Button(self.root, text="Clear frames", command=self.clear_frames()).place(x=250, y=310)

        y_const +=y_space
        name_text = tk.Label(self.root, text="Job name",font = font_2).place(x=x_const, y=y_const)
        name_entry = tk.Entry(self.root,
                              textvariable=self.name_var
                              ).place(x=540, y=y_const, width=180)
        self.frame.place(x=20, y=90)
        button = tk.Button(self.root, text="quit", command=self.close).place(x=50, y=470)
        self.create_warning_frame()
        self.root.mainloop()

    def create_warning_frame(self):
        font_1 = "Verdana 22 bold"
        font_2 = "Verdana 12"
        #pass requirement header
        tk.Label(self.root, text="Pass Requirements", font=font_2).place(x=50, y=320)
        #min porosity label and input
        tk.Label(self.root, text="Min porosity(%)", font=font_2).place(x=20, y=390)
        tk.Entry(self.root,textvariable=self.min_pore).place(x=130, y=390, width=50)
        # max porosity label and input
        tk.Label(self.root, text="Max porosity(%)", font=font_2).place(x=210, y=390)
        tk.Entry(self.root, textvariable=self.max_pore).place(x=320, y=390, width=50)
        #max circle diameter
        tk.Label(self.root, text="Max diameter(microns)", font=font_2).place(x=20, y=430)
        tk.Entry(self.root, textvariable=self.max_diam).place(x=200, y=430, width=100)

    def browseFiles(self):
        "Prompts user for folders to include"
        filename = filedialog.askdirectory(initialdir="/",
                                           title="Select a Folder To View",
                                           )
        cwd = filename
        self.base_folder = cwd + '/'
        self.viewFolder(cwd)

    def viewFolder(self, cwd):
        folder_list = os.listdir(cwd)
        self.include_list=[]
        label = tk.Label(self.root, text=("Folder:" + cwd)).place(x=20, y=40)
        for folder in folder_list:
            chkValue = tk.BooleanVar()
            chkValue.set(False)
            checkbutton = tk.Checkbutton(self.frame.scrollable_frame, text=folder, var=chkValue, width=20)
            checkbutton.pack()
            self.include_list.append([chkValue, folder])

    def close(self):
        self.root.quit()


    def update_constants(self):
        constants = self.options['constants']
        constants['thresh'] = int(self.thresh_var.get())
        constants['fiber_type'] = self.fiber_var.get()
        constants['warn_size'] = int(self.warn_var.get())
        constants['use_alt'] = self.local_var.get()
        constants['alt_thresh'] = int(self.thresh_var.get())
        constants['multi'] = bool(self.multi_var.get())
        constants['num_circles'] = int(self.num_var.get())
        constants['fiber_type']='dark'
        constants['scale'] = float(self.scale_var.get())
        constants['min_ignore'] = float(self.min_var.get())
        constants['max_diam'] = float(self.max_diam.get())
        constants['min_porosity'] = float(self.min_pore.get())
        constants['max_allowed'] = float(self.max_diam.get())
        constants['max_porosity'] = float(self.max_pore.get())

        if int(self.boarder_var.get()) > 1:
            constants['crop'] = True
            constants['boarder'] = int(self.boarder_var.get())

        self.options['constants'] = constants




    def start_working_2(self,options):
        db_helper = Db_helper()
        # opt = self.thread_queue.get(0)
        # self._print(self.res)
        print("SIMPLE QUEUE JOB")
        job = Job(options, db_helper)
        filter_dic = job.get_dic()
        # for folder in filter_dic['frame_ls']:
        SpreadWriter(filter_dic)
        # self.thread_queue.put(options)
        # print("START WORKING")
        # self.root.after(100, self.listen_for_result)


    def update_options(self):
        self.options['job_name'] = str(self.name_var.get())
        self.options['program_type'] = 'dark'
        i = 0
        while i < len(self.include_list):
            if self.include_list[i][0].get():
                print(self.include_list[i][0])
                self.added_folders.append(self.base_folder + self.include_list[i][1])
            i = i + 1
        self.options['frame_paths'] = self.added_folders
        self.update_constants()


    def clear_options(self):
        self.added_folders = []
        self.include_list = []
        self.frame.destroy()
        self.frame = ScrollableFrame(self.root)
        self.frame.place(x=20, y=90)
        self.viewFolder(self.base_folder)


    def execute_outputs(self):
        self.update_options()
        #sent post https call to backend to queue job
        # request = requests.post('http://127.0.0.1:5000/queue', json=self.options)
        threading.Thread(target=_asyncio_thread, args=(self.async_loop,self.options)).start()
        self.async_loop = asyncio.get_event_loop()
        print("queue request sent with options: ",self.options)
        #remove folders from added folders and reset the values in scrollable frame
        self.clear_options()

def _asyncio_thread(async_loop,options):
    # async_loop.run_until_complete(do_job(options))
    asyncio.ensure_future(do_job(options))
    # await do_job(options)


def do_tasks(async_loop):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()



def do_job(options):
    db_helper = Db_helper()
    print("SIMPLE QUEUE JOB")
    job = Job(options, db_helper)
    filter_dic = job.get_dic()
    SpreadWriter(filter_dic)


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    Interface(async_loop)
