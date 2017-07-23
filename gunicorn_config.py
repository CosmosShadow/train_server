import multiprocessing

bind = '0.0.0.0:8080'
workers = 2
threads = 1
daemon = True
pidfile = 'gunicorn.pid'

def post_worker_init(worker):
    pass
