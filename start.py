import threading
from REST.index import server
from interface.job_queue_interface import Interface
def main():
    #start rest api for job queuing
    threading.Thread(target=server.run).start()
    #start interface for creating jobs
    Interface()


if __name__ == "__main__":
    main()