import sqlite3
import csv

from numpy import ndarray,array,load,save
from io import BytesIO
from sqlite3 import Binary
def convert_array(text):
        out = BytesIO(text)
        out.seek(0)
        return load(out,allow_pickle=True)

def adapt_array(arr):
        out = BytesIO()
        save(out,arr)
        out.seek(0)
        return Binary(out.read())

def write_diam(job_name1):
        sqlite3.register_adapter(ndarray,adapt_array)
        sqlite3.register_converter("array", convert_array)

        conn = sqlite3.connect('pore.db',detect_types=sqlite3.PARSE_DECLTYPES)
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs_index WHERE job_name=? LIMIT 1;",(job_name1,))
        row = cur.fetchall()
        areas = []
        frames = row[0][5]
        diams = []
        for frame in frames:
                cur = conn.cursor()
                cur.execute("SELECT image_data_ls,scale_v FROM frames_index WHERE frame_id=? LIMIT 1;", (frame,))
                images = cur.fetchall()
                scale = float(images[0][1])
                print('scale:', scale)
                for image in images[0][0]:
                        #print("image id ,", image)
                        cur = conn.cursor()

                        cur.execute("SELECT largest_holes FROM image_output WHERE img_id=?;", (image,))
                        holes = cur.fetchall()
                        #print('holes :',type(holes),)
                        hole_ls = holes[0][0]
                        print("tye:",type(hole_ls))
                        for hole in hole_ls:
                                r = hole[1]
                                print(r)
                                d = r * 2 * float(scale)
                                diams.append(round(d,2))
                        areas = areas + holes
                diams.sort(reverse=True)
                print(diams)
        conn.close()
        # name of csv file
        filename=job_name1+"-diameter.csv"
        # writing to csv file
        with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the data rows
                for d in diams:
                        csvwriter.writerow([round(d,2)])
        return filename,len(diams)

job_name =input("please enter the name of the job you would like diameters of:")
f_name,diams = write_diam(job_name)
print(diams," diameters saved in: ", f_name,)
