import couchdb
import yaml
import argparse
import os


def main(args):
    with open(args.conf, 'r') as conf_f:
        conf = yaml.load(conf_f, Loader=yaml.SafeLoader)
    db_conf = conf['statusdb']
    url = "https://{0}:{1}@{2}".format(db_conf['username'], db_conf['password'], db_conf['url'])
    s = couchdb.Server(url)
    db_conf = conf['statusdbdev']
    url = "https://{0}:{1}@{2}".format(db_conf['username'], db_conf['password'], db_conf['url'])
    sd = couchdb.Server(url)
    db = s['charon']
    dbd = sd['charon']
    ids = []

    if "_" in args.project:
        v = db.view("project/name")
        for row in v[args.project]:
            pid = row.value
    else:
        pid = args.project

    v = db.view("project/projectid")
    for row in v[pid]:
        ids.append(row.id)
    v = db.view("sample/sampleid")
    for row in v[[pid, 'A']:[pid, 'ZZ']]:
        ids.append(row.id)
    v = db.view("libprep/libprepid")
    for row in v[[pid, 'A' 'A']:[pid, 'ZZ', 'ZZ']]:
        ids.append(row.id)
    v = db.view("seqrun/seqrunid")
    for row in v[[pid, 'A', 'A', 'A']:[pid, 'ZZ', 'ZZ', 'ZZ']]:
        ids.append(row.id)

    for i in ids:
        doc = db.get(i)
        docd = dbd.get(i)
        if not docd:
            docd = {}
            for key in list(doc.keys()):
                if key != '_rev':
                    docd[key] = doc[key]
        dbd.save(docd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="project", required=True)
    parser.add_argument("-c", dest="conf", default="{0}/conf/LIMS2DB/post_process.yaml".format(os.environ["HOME"]))
    args = parser.parse_args()
    main(args)
