import requests
from constants import constants
from index import server
import threading
# from interface.job_queue_interface import Interface

threading.Thread(target=server.run).start()
const = constants()
options = const.default_options
options['frame_paths'].append("/Users/jackkelly/PycharmProjects/pore_hr/frames_folder/diversity-training")
request = requests.post('http://127.0.0.1:5000/queue', json=options)
print("queue request sent with options: ",options)