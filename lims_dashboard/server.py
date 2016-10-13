import glob
import json
import os
import subprocess
import yaml

from flask import Flask, request, render_template, url_for

app = Flask(__name__, template_folder='../templates', static_folder='../static')

UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

app.config['my_scripts']={}
for conf_file in glob.glob(os.path.join(app.root_path, '..', 'conf', '*.conf')):
    with open(conf_file) as sconf:
        app.config['my_scripts'].update(yaml.load(sconf))

app.debug=True

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
    out=run_script(data.get('script_name'), data.get('options'))
    return json.dumps({"status":"Success","output":out}), 200

def run_script(name, options):
    cwd=os.getcwd()
    os.chdir('../uploads')
    command = [app.config['my_scripts'][name]['command']]
    command.extend(options.split())
    try:
        out=subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        out=e.output

    os.chdir(cwd)
    return out
