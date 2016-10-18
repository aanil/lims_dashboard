import json
import os


from flask import request, render_template, Blueprint, current_app, send_file
from lims_dashboard.utils import run_script


my_bp= Blueprint("main_app", __name__)

@my_bp.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@my_bp.route('/favicon.ico')
def send_icon():
    return send_file(os.path.join('static','favicon.ico'))

@my_bp.route('/')
def display_dashboard():
    return render_template('index.html', scripts=current_app.config['my_scripts'], content=None)


@my_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return '{status:"Failed"}', 400
    upfile = request.files['file']
    if upfile.filename == '':
        return '{status:"Failed"}', 400
    if upfile:
        upfile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], upfile.filename))
        return '{status:"Success"}', 201
    return '{status:"Failed"}', 400

@my_bp.route('/start', methods=['POST'])
def start():
    data=json.loads(request.get_data())
    code,out, err = run_script(current_app, data.get('script_name'), data.get('options'))
    if code == 0:
        return json.dumps({"status":"Success","output":out}), 200
    else:
        return json.dumps({"status":"Error","output":out, "error":err}), 500
