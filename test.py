import shutil
import subprocess

app_name = "Chrome"
print(subprocess.run(["where", app_name], capture_output=True, text=True).stdout.strip())