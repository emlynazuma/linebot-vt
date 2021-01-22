"""gunicorn server configuration."""
import multiprocessing

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:80"
errorlog = "/var/log/gunicorn/error.log"
