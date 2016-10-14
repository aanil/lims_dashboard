
import os
import subprocess

def run_script(app, name, options):
    cwd=os.getcwd()
    os.chdir('{0}/uploads'.format(app.root_path))
    command = [os.path.join(app.config['SCRIPT_FOLDER'],app.config['my_scripts'][name]['command'])]
    command.extend(options.split())

    handle=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=handle.communicate()

    os.chdir(cwd)
    return handle.returncode, out, err
