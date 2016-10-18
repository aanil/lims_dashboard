import argparse
import pprint
import logging

from LIMS2DB.classes import ProjectSQL
from genologics_sql.utils import get_configuration, get_session
from genologics_sql.tables import Project as DBProject


def main(args):

    mainlog = logging.getLogger('psullogger')
    mainlog.setLevel(level=logging.ERROR)
    mfh = logging.StreamHandler
    mft = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mfh.setFormatter(mft)
    mainlog.addHandler(mfh)

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
