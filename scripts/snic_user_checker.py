import argparse
import yaml
import os
import imp

def main(args):
    with open(args.sconf) as config_file:
        config = yaml.load(config_file, Loader=yaml.SafeLoader)

    snic_check_module = imp.load_source('snic_check',"{0}/src/standalone_scripts/statusdb_snicuser_checker.py".format(os.environ["HOME"]))
    result = snic_check_module.snic_check(args.email, config['SNIC'])

    print('<b>{}</b> present in SNIC: <span class="label label-{}">{}</span>'.format(args.email, 'success' if result else 'danger', result))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check_email', dest='email')
    parser.add_argument("-sc", dest="sconf", default="{0}/conf/snic_cred.yaml".format(os.environ["HOME"]))
    args = parser.parse_args()
    if args.email is None:
        raise argparse.ArgumentError('--check_email is required')
    else:
        main(args)
