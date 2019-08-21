import glob
import os
import yaml
import logging


from flask import Flask

from lims_dashboard.routes import my_bp


def create_app(root_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], python=None):
    app = Flask(__name__, root_path=root_path)
    UPLOAD_FOLDER = os.path.join(root_path, 'uploads')
    SCRIPT_FOLDER = os.path.join(root_path, 'scripts')
    app.config['python_exec'] = python
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SCRIPT_FOLDER'] = SCRIPT_FOLDER
    app.config['my_scripts'] = {}
    for conf_file in glob.glob(os.path.join(root_path, 'conf', '*.conf')):
        with open(conf_file) as sconf:
            app.config['my_scripts'].update(yaml.load(sconf, Loader=yaml.SafeLoader))

    app.register_blueprint(my_bp)
    return app


def setup_logger():
    logger = logging.getLogger("lims_dashboard")
    logger.setLevel("INFO")
    loghandler = logging.StreamHandler()
    loghandler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(loghandler)


setup_logger()

app = None
if not app:
    python_exec = "{0}/anaconda/envs/lims_dashboard/bin/python".format(os.environ["HOME"])
    app = create_app(python=python_exec)
