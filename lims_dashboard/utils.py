
import os
import subprocess

def run_script(app, name, options):
    cwd=os.getcwd()
    os.chdir('{0}/uploads'.format(app.root_path))
    conf_obj=app.config['my_scripts'][name]
    command=[':']
    if conf_obj['type']=='python':
        command=[app.config['python_exec'], os.path.join(app.config['SCRIPT_FOLDER'],app.config['my_scripts'][name]['script'])]
    command.extend(options.split())

    handle=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=handle.communicate()

    os.chdir(cwd)
    return handle.returncode, out, err
