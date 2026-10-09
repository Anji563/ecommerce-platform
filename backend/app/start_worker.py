import subprocess
import sys
import os

# Start dummy HTTP server on port 10000 for Render health check
print("Starting HTTP health check server on port 10000...")
subprocess.Popen([sys.executable, "-m", "http.server", "10000"])

# Run Celery worker in foreground to keep process alive
print("Starting Celery worker...")
os.execvp("celery", ["celery", "-A", "app.tasks.celery_app", "worker", "--loglevel=info"])