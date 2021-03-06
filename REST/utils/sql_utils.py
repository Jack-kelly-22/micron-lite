from numpy import save as save
from numpy import load as load
from numpy import ndarray
from sqlite3 import Binary
import sqlite3
from io import BytesIO
import pickle

def fix_path(path):
        #return path.replace(" ","")
        #return path[1:]
        return path

def adapt_array(arr):
        out = BytesIO()
        save(out,arr)
        out.seek(0)
        return Binary(out.read())

def convert_array(text):
        out = BytesIO(text)
        out.seek(0)
        return load(out,allow_pickle=True)


def get_frame_fetch_str():
        s = ''' SELECT * from frames_index
                WHERE frame_id IN (SELECT frame_id 
                FROM frames_index
                WHERE frame_id = ?);'''
        return s

def get_img_fetch_str():
        s = ''' SELECT * from image_output
                WHERE img_id IN (SELECT img_id 
                FROM image_output
                WHERE img_id = ?);'''
        return s

def get_job_fetch_str():
        s = ''' SELECT * from jobs_index
                WHERE job_id IN (SELECT job_id 
                FROM jobs_index
                WHERE job_id = ?);'''
        return s

def get_img_post_str():
        s = ''' insert into image_output(img_id,img_name,img_path,pores,areas,all_areas,largest_holes,heat_img_path,heat_diff_path)
                           VALUES(?,?,?,?,?,?,?,?,?)'''
        return s

def get_jobs_fetch_str():
        s = '''SELECT * from jobs_index'''
        return s


def list_jobs():
        conn = sqlite3.connect("/Users/jackkelly/jkdev/dash_vs/local/pore.db")
        cur = conn.execute(''' SELECT job_id, job_name from jobs_index''')
        for row in cur:
                print("id:", row[0], type(row[0]))
                print("name:", row[1])
        print("done selecting")
