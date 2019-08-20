
import os
import subprocess
import traceback

import logging
logger = logging.getLogger("lims_dashboard")


def run_script(app, name, options):
    cwd = os.getcwd()
    os.chdir('{0}/uploads'.format(app.root_path))
    conf_obj = app.config['my_scripts'][name]
    command = [':']
    if conf_obj['type'] == 'python':
        try:
            python_exec = conf_obj['python_exec']
        except KeyError:  # No python exec specified in script conf
            python_exec = app.config['python_exec']

        command = [python_exec, os.path.join(app.config['SCRIPT_FOLDER'],app.config['my_scripts'][name]['script'])]
    command.extend(options.split())
    logger.info("About to run command: {}".format(" ".join(command)))

    try:
        handle = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = handle.communicate()
        returncode = handle.returncode
    except Exception:
        returncode = -1
        out = "Running the command: {}".format(" ".join(command))
        err = traceback.format_exc()

    os.chdir(cwd)
    return returncode, out, err
