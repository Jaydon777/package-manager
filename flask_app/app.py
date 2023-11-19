from flask import Flask, render_template, request, redirect, url_for, session, after_this_request
import time
import os
import subprocess

app = Flask(_name_)
app.secret_key = 'your_secret_key' 

log_content = []
installation_progress = 0

def perform_cv_functionality(both_one):
    global installation_progress, log_content
    dependencies = [
        "opencv-python==4.5.3.56",
        "numpy==1.17",
        "matplotlib==3.5",
        "tensorflow==2.10",
        "keras"
    ]

    try:
        for dependency in dependencies:
            install_command = ["pip3", "install", dependency]
            subprocess.run(install_command, check=True)
            time.sleep(1)
            if both_one == 'both':
                installation_progress += 8.33333
            elif both_one == 'one':
                installation_progress += 20
            # Pass the command to HTML
            log_content.append(f'Installing package: {dependency}\n')
    except Exception as e:
        # Pass the failure message to HTML
        log_content.append(f'Installation failed: {str(e)}\n')



def perform_nlp_functionality(both_one):
    global installation_progress, log_content
    dependencies = [
        "nltk==3.5",
        "spacy==3.7.2",
        "tensorflow==2.10",
        "keras==2.10",
        "torch",
        "torchvision",
        "torchaudio"
    ]

    try:
        for dependency in dependencies:
            if dependency == 'torch':
                install_command = ['pip3', 'install', '--no-cache-dir', 'torch']
            else:
                install_command = ["pip3", "install", dependency]
            subprocess.run(install_command, check=True)
            time.sleep(1)
            if(both_one == 'both'):
                installation_progress += 8.33333
            elif(both_one == 'one'):
                installation_progress += 14.285
            # Pass the command to HTML
            log_content.append(f'Installing package: {dependency}\n')
    except Exception as e:
        # Pass the failure message to HTML
        log_content.append(f'Installation failed: {str(e)}\n')

@app.route('/')
def index():
    return render_template('screen_1.html')

@app.route('/choose_option')
def choose_option():
    return render_template('screen_2.html')

@app.route('/display_packages', methods=['POST'])
def display_packages():
    user_choices = request.form.getlist('user_choices')
    session['user_choices'] = user_choices
    return render_template('screen_3.html', user_choices=user_choices)

@app.route('/confirm_installation', methods=['POST'])
def confirm_installation():
    return render_template('screen_4.html')

@app.route('/install_packages')
def install_packages():
    user_choices = session.get('user_choices', [])

    if 'CV' in user_choices and 'NLP' in user_choices:
        perform_cv_functionality('both')
        perform_nlp_functionality('both')

    elif 'CV' in user_choices:
        perform_cv_functionality('one')

    elif 'NLP' in user_choices:
        perform_nlp_functionality('one')

@app.route('/sucess')
def sucess():
    return render_template('screen_5.html')

@app.route('/log_content')
def get_log_content():
    global log_content
    content = ''.join(log_content)
    log_content = []  # Clear the content after fetching
    return content

@app.route('/progress')
def get_progress():
    global installation_progress
    return {'progress': installation_progress}

@app.route('/manual_shutdown')
def manual_shutdown():
    shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    if shutdown_hook is not None:
        shutdown_hook()
        return 'Server shutting down...'
    else:
        os._exit(0)  # Terminate the process
        return 'Process terminated.'

if _name_ == '_main_':
    app.run(debug=True, threaded=True)