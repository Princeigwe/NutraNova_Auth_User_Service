import subprocess
import shlex

def start_worker():
  subprocess.Popen( shlex.split("python3 -m celery -A core worker -l INFO"), stdout=subprocess.PIPE, shell=True)
