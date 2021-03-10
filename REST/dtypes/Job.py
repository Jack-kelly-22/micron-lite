from REST.dtypes.Frame import Frame
from os import mkdir, listdir, makedirs
import sqlite3
import uuid
from REST.utils.sql_utils import adapt_array, convert_array
from numpy import ndarray, array
from shutil import rmtree
from REST.utils.export_diams import write_diam


class Job:
    def __init__(self, options, db_ref):
        self.job_name = options["job_name"]
        self.job_id = str(uuid.uuid4()).replace('-', '') + "_" + self.job_name
        self.type = int(options["input_type"])
        self.tags = str(options["tags"])
        self.options = options
        self.frame_ls = []
        self.frame_ref_ls = []
        self.try_make_dir()
        self.frame_paths = options['frame_paths']
        self.create_frames(options, db_ref, options["frame_paths"])
        self.constants = options["constants"]
        self.update_ref_ls()
        self.add_job_db()

    def get_dic(self):
        self.options['frame_ls'] = self.frame_ls
        return self.options

    def try_make_dir(self):
        """will attempt to create directory for job outputs
        if folder already exists will empty folder"""
        try:
            mkdir("./job-data/" + self.job_name)
        except Exception as e:
            print("exception:", e)
            print("emptying dir... dir empty")
            rmtree("./job-data/" + self.job_name)
            makedirs("./job-data/" + self.job_name)


    def update_ref_ls(self):
        for frame in self.frame_ls:
            self.frame_ref_ls.append(frame.id)

        print("job frame ref ls updated")

    def add_job_db(self):
        sqlite3.register_adapter(ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        conn = sqlite3.connect("REST/data/pore.db", detect_types=sqlite3.PARSE_DECLTYPES)

        out_path = "." + "/job-data/" + self.job_name
        sql_str = ''' insert into jobs_index(job_id,job_name,job_path,job_type,tags,frame_ls,frame_names)
                        VALUES(?,?,?,?,?,?,?)'''
        conn.execute(sql_str, (
        self.job_id, self.job_name, out_path, self.type, self.tags, array(self.frame_ref_ls), array(self.frame_paths)))
        conn.commit()
        conn.close()
        #        write_diam(self.job_name)

    def create_frames(self, options, db_ref, frame_paths):
        i = 0
        out_path = "/job-data/"
        for fpath in frame_paths:
            f = Frame(fpath,options,db_ref)
            self.frame_ls.append(f)
