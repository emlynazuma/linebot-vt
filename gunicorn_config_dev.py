"""gunicorn server configuration."""
import multiprocessing

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 1
bind = "0.0.0.0:80"
errorlog = "-"
accesslog = "-"
reload = True
