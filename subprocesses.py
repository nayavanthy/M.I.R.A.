import subprocess
import time
import signal
import os

fastapi_process = None
mongo_process = None

def start_operations():
    global fastapi_process, mongo_process

    # Use raw string (r"") or replace backslashes with double backslashes
    mongo_path = r"C:\Users\nayav\Downloads\mongodb-windows-x86_64-8.0.5\mongodb-win32-x86_64-windows-8.0.5\bin\mongod.exe"
    db_path = r"C:\Users\nayav\Desktop\Ryle\MIRA\data\db"

    # Start MongoDB
    mongo_process = subprocess.Popen([mongo_path, "--dbpath", db_path])

    # Start FastAPI server
    fastapi_process = subprocess.Popen(["uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"])

    time.sleep(2)  # Wait for backend to start

def kill_operations():
    global fastapi_process, mongo_process
    
    if fastapi_process:
        print("Terminating FastAPI server...")
        fastapi_process.terminate()  # Send terminate signal
        fastapi_process.wait()  # Ensure process is fully stopped
        fastapi_process = None  # Reset the variable
    
    if mongo_process:
        print("Terminating MongoDB...")

        # Try terminating normally
        mongo_process.terminate()
        try:
            mongo_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("MongoDB did not terminate, forcing shutdown...")

            # Kill MongoDB process forcefully
            if os.name == 'nt':  # Windows
                subprocess.run("taskkill /F /IM mongod.exe /T", shell=True)
            else:  # Linux/Mac
                os.kill(mongo_process.pid, signal.SIGKILL)

        mongo_process = None
