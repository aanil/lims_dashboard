import glob
import json
import os
import subprocess
import traceback
import yaml

from flask import Flask, request, render_template, url_for

app=None


def create_app(root_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]):
    global app
    app = Flask(__name__, template_folder='templates', static_folder='static', root_path=root_path)
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['my_scripts']={}
    for conf_file in glob.glob(os.path.join(app.root_path, 'conf', '*.conf')):
        with open(conf_file) as sconf:
            app.config['my_scripts'].update(yaml.load(sconf))
    return app

if not app:
    app=create_app()

@app.route('/', methods=['GET'])
def display_dashboard():
    return render_template('index.html', scripts=app.config['my_scripts'], content=None)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return '{status:"Failed"}', 400
    upfile = request.files['file']
    if upfile.filename == '':
        return '{status:"Failed"}', 400
    if upfile:
        upfile.save(os.path.join(app.config['UPLOAD_FOLDER'], upfile.filename))
        return '{status:"Success"}', 201
    return '{status:"Failed"}', 400

@app.route('/start', methods=['POST'])
def start():
    data=json.loads(request.get_data())
    code,out, err = run_script(data.get('script_name'), data.get('options'))
    if code == 0:
        return json.dumps({"status":"Success","output":out}), 200
    else:
        return json.dumps({"status":"Error","output":out, "error":err}), 500

def run_script(name, options):
    cwd=os.getcwd()
    os.chdir('{0}/uploads'.format(app.root_path))
    command = [app.config['my_scripts'][name]['command']]
    command.extend(options.split())

    handle=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=handle.communicate()

    os.chdir(cwd)
    return handle.returncode, out, err
