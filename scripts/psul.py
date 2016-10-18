import argparse
import pprint
import logging

from LIMS2DB.classes import ProjectSQL
from genologics_sql.utils import get_configuration, get_session
from genologics_sql.tables import Project as DBProject


def main(args):

    mainlog=get_logger('psullogger')
    couch = load_couch_server(conf)
    lims_db = get_session()
    host=get_configuration()['url']
    if args.name:
        pj_id=lims_db.query(DBProject.luid).filter(DBProject.name ==args.name).scalar()
    else:
        pj_id=args.pid

    P = ProjectSQL(lims_db, mainlog, pj_id, host, couch)

    if args.test:
        pp = pprint.pprint(P.obj)
    else:
        P.save()

def load_couch_server(config_file):
    """loads couch server with settings specified in 'config_file'"""
    try:
        stream = open(config_file,'r')
        db_conf = yaml.load(stream)['statusdb']
        url = db_conf['username']+':'+db_conf['password']+'@'+db_conf['url']+':'+str(db_conf['port'])
        couch = couchdb.Server("http://" + url)
        return couch
    except KeyError:
        raise RuntimeError("\"statusdb\" section missing from configuration file.")

def get_logger(name)
    mainlog = logging.getLogger(name)
    mainlog.setLevel(level=logging.ERROR)
    mfh = logging.StreamHandler()
    mft = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mfh.setFormatter(mft)
    mainlog.addHandler(mfh)
    return mainlog


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="pid")
    parser.add_argument("-n", dest="name")
    parser.add_argument("-x", dest="test", action='store_true')
    args = parser.parse_args()
    if args.pid is None and args.name is None:
        pa.error("at least one of -p and -n is required")
    else:
        main(args)
