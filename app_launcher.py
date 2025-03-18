import subprocess

# Hardcoded paths for standard applications
APP_PATHS = {
    "spotify": r"C:\Users\nayav\AppData\Roaming\Spotify\Spotify.exe",
    "chrome": r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
    "vscode": r"C:\Users\nayav\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "steam": r'"C:\Program Files (x86)\Steam\Steam.exe"',
    "matlab": r'"C:\Program Files\MATLAB\R2024b\bin\matlab.exe"',
    "notepad": "notepad.exe",
}

def open_application(app_name):
    """Open an application using its hardcoded path or special UWP command."""
    app_name = app_name.lower()
    
    if app_name == "netflix":
        try:
            subprocess.Popen("explorer shell:AppsFolder\\4DF9E0F8.Netflix_mcm4njqhnhss8!Netflix", shell=True)
            return "Opening Netflix app..."
        except Exception as e:
            return f"Error opening Netflix: {e}"

    elif app_name in APP_PATHS:
        try:
            subprocess.Popen(APP_PATHS[app_name], shell=True)
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Error opening {app_name}: {e}"

    else:
        return f"{app_name} is not in my list of hardcoded apps, boss."