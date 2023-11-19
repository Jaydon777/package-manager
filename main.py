import threading
import logging
from gi import require_version
require_version('Gtk', '3.0')
require_version('WebKit2', '4.0')
from gi.repository import Gtk
import subprocess
import os
from webview_display import WebViewWindow
import os

# Configure logging to write to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_package_installed(package_name):
    try:
        subprocess.check_output(['dpkg', '-l', package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def is_package_installed_pip(package_name):
    try:
        subprocess.check_output(['pip3', 'show', package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def install_python_37():
    subprocess.run(['sudo', 'add-apt-repository', 'ppa:deadsnakes/ppa'])
    subprocess.run(['sudo', 'apt-get', 'update'])
    subprocess.run(['sudo', 'apt-get', 'install', 'python3.7'])

def install_starting_packages():

    # Install python3.7-venv if not already installed
    if not is_package_installed('python3.7-venv'):
        install_python_37()

    # Create a virtual environment named 'venv'
    subprocess.run(['python3.7', '-m', 'venv', 'venv'])

    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, 'venv')

    # Modify the PATH variable to include the virtual environment's bin directory
    os.environ['PATH'] = os.path.join(venv_path, 'bin') + os.pathsep + os.environ['PATH']

    # Check if Flask is installed
    if not is_package_installed_pip('Flask'):
        subprocess.call(['python3', '-m', 'pip', 'install', 'flask[async]'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # subprocess.call(['python3', '-m', 'pip', 'install', 'flask[async]'])
        logging.info("Installed Flask.")
    else:
        logging.info("Flask is already installed.")

    # Check if gir1.2-webkit2-4.0 is installed
    if not is_package_installed('gir1.2-webkit2-4.0'):
        subprocess.call(['sudo', 'apt-get', 'install', 'gir1.2-webkit2-4.0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # subprocess.call(['sudo', 'apt-get', 'install', 'gir1.2-webkit2-4.0'])
        logging.info("Installed gir1.2-webkit2-4.0.")
    else:
        logging.info("gir1.2-webkit2-4.0 is already installed.")

def run_flask_app():
    # Set the FLASK_ENV environment variable to "production"
    # os.environ['FLASK_ENV'] = 'production'

    # Run Flask in a separate process, capture stdout and stderr
    result = subprocess.run(['python3', 'flask_app/app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # result = subprocess.run(['python3', 'flask_app/app.py'])
    
    # Log the stdout and stderr
    logging.info(f"Flask application stdout:\n{result.stdout}")
    logging.error(f"Flask application stderr:\n{result.stderr}")


if __name__ == "__main__":
    install_starting_packages()

    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    logging.info("Flask execution started!")

    # Create the WebViewWindow
    win = WebViewWindow()

    # Run the Gtk main loop
    win.run()
