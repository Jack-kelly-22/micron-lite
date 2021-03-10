from flask import Flask,request
from flask_restful import Resource,Api
from flask_cors import CORS
from celery import Celery
from REST.dtypes.Job import Job
# import json
import threading
import os
from REST.dtypes.db_helper import Db_helper
# from dtypes.Spreadsheets import Spreadsheet
from SpreadWriter import SpreadWriter
from REST.celery_config import make_celery


server = Flask('backend')
server.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(server)
db_helper = Db_helper()
# celery -A index.celery worker

@celery.task()
def add_job(item):
    job = Job(item, db_helper)
    filter_dic = job.get_dic()
    # for folder in filter_dic['frame_ls']:
    SpreadWriter(filter_dic)

@server.route('/queue', methods=['POST'])
def q_job():
    options = request.get_json(force=True)
    print("(REST)queue job with options:",options)
    add_job.delay(options)
    return {'success':200}
print("Starting CORS")
CORS(server)
# server.run()
api = Api(server)
# server = app.server