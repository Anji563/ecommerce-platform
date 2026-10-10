import subprocess
import sys
import os

# Start dummy HTTP server on port 10000 for Render health check
print("Starting HTTP health check server on port 10000...")
http_server = subprocess.Popen([sys.executable, "-m", "http.server", "10000"])

# Run Celery worker in the foreground so the process stays alive
print("Starting Celery worker...")
celery_process = subprocess.run([
    "celery", 
    "-A", 
    "app.tasks.celery_app", 
    "worker", 
    "--loglevel=info"
])

# Terminate health check server if celery stops
http_server.terminate()
sys.exit(celery_process.returncode)