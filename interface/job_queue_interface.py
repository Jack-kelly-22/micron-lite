#file is reasponsible for user interface
import os
import tkinter as tk
from tkinter import filedialog
import requests
from interface.ScrollableFrame import ScrollableFrame
# from utils import default_settings
from constants import constants

# Function for opening the
# file explorer window
class Interface():
    def __init__(self):

        self.base_folder = ""
        self.added_folders = []
        self.output_folder = ""
        self.include_list = []

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
        self.boarder_var = tk.StringVar(value="0")
        self.name_var = tk.StringVar(value=self.options['job_name'])
        # self.adjust_var = tk.BooleanVar(value=self.options['constants'][])
        self.num_var = tk.StringVar(value=self.options['constants']['num_circles'])
        self.warn_var = tk.StringVar(value=self.options['constants']['warn_size'])
        self.job_num = tk.StringVar(value= "0")
        self.options['constants']['min_ignore'] = tk.StringVar()
        font_1 = "Verdana 22 bold"
        font_2 = "Verdana 16"
        self.frame = ScrollableFrame(self.root)
        label = tk.Label(self.root, text="Frames",font = font_1).place(x=10, y=20)
        button = tk.Button(self.root, text="Select Frames", command=self.browseFiles).place(x=230, y=20)
        # output dirrectory button
        pass_label = tk.Label(self.root, text="Pass Requirements ", ).place(x=120, y=350)
        # button = tk.Button(self.root, text="Select Folder", command=self.browseOutput).place(x=170, y=350)
        button = tk.Button(self.root, text="Add Job To Queue", command=self.execute_outputs).place(x=250, y=410)

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
        button = tk.Button(self.root, text="quit", command=self.close).place(x=50, y=440)

        self.root.mainloop()

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
        constants['thresh'] = self.thresh_var.get()
        constants['fiber_type'] = self.fiber_var
        constants['warn_size'] = self.warn_var.get()
        constants['use_alt'] = self.local_var.get()
        constants['alt_thresh'] = self.thresh_var.get()
        constants['multi'] = self.multi_var.get()
        constants['num_circles'] = self.num_var.get()
        constants['fiber_type']='dark'
        constants['min_ignore'] = self.min_var.get()
        if int(self.boarder_var.get()) > 1:
            constants['crop'] = True
            constants['boarder'] = int(self.boarder_var.get())

        self.options['constants'] = constants


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
        request = requests.post('http://127.0.0.1:8050/queue', json=self.options)
        print("queue request sent with options: ",self.options)
        #remove folders from added folders and reset the values in scrollable frame
        self.clear_options()
