import subprocess
import shlex
import psutil


def kill_previous_running_celery_worker():
  process_name = "celery"

  for proc in psutil.process_iter():
    if process_name in proc.name().lower():
      subprocess.Popen( shlex.split(f"kill {proc.pid}"), stdout=subprocess.PIPE, shell=True)

def start_worker():
  kill_previous_running_celery_worker()
  subprocess.Popen( shlex.split("python3 -m celery -A core worker -l INFO"), stdout=subprocess.PIPE, shell=True)
