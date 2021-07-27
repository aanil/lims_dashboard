#!/usr/bin/env python
# -*- coding: utf-8 -*-

from genologics.lims import *
from genologics.config import BASEURI, USERNAME, PASSWORD
import couchdb
import os
import yaml

import argparse
from argparse import ArgumentParser

DESC = """Query all plates in LIMS with project ID
"""

# Only 96 well plates are queried. We don't consider tubes or sequencing flow cells.
PLATE_TYPE = '96 well plate'

# Only plates in the following steps are queried
PROCESS_TYPE = [
    'Purification',
    'CA Purification',
    'End repair, size selection, A-tailing and adapter ligation (TruSeq PCR-free DNA) 4.0',
    'Purification (ThruPlex)',
    'Amplify Adapter-Ligated Library (SS XT) 4.0',
    'Amplify Captured Libraries to Add Index Tags (SS XT) 4.0',
    'RAD-seq Library Indexing v1.0',
    'Ribosomal cDNA Depletion and 2nd Amplification (SMARTer Pico) 4.0',
    'Library Normalization (Illumina SBS) 4.0',
    'Library Normalization (HiSeq X) 1.0',
    'Library Normalization (MiSeq) 4.0',
    'Library Normalization (NovaSeq) v2.0',
    'Library Pooling (Finished Libraries) 4.0',
    'Sample Placement (Size Selection)',
    'Applications Finish Prep',
    'Size Selection (Pippin)',
    'Pre-Pooling (Illumina SBS) 4.0',
    'Library Pooling (HiSeq X) 1.0',
    'Pre-Pooling (MiSeq) 4.0',
    'Pre-Pooling (NovaSeq) v2.0',
    'Aliquot Samples for Caliper/Bioanalyzer',
    'Aliquot Samples for Qubit/Bioanalyzer'
]

# Default file header
HEADER = [
    'Plate ID',
    'Plate Name',
    'LIMS step',
]


# Read in plate database file.
def read_plate_database(db):
    database = []
    for docid in db.view('_all_docs'):
        i = docid['id']
        database.append(i)
    return database


# Update database
def update_plate_database(lims, db):
    # Fetch existing plates in couchdb
    database = read_plate_database(db)
    # Fetch all containers in LIMS
    containers = lims.get_containers(type=PLATE_TYPE)
    all_containers_in_lims = []
    for i in containers:
        all_containers_in_lims.append(i.id)
    # Get a list of new containers that have not been imported in couchdb
    new_container_ids = list(set(all_containers_in_lims) - set(database))

    # Prepare an input dictionary for importing to couchdb
    if new_container_ids != []:
        new_entry = []
        for id in new_container_ids:
            process_name = ''
            container_name = ''
            project_list = []
            artifacts = lims.get_artifacts(containerlimsid=id)
            if artifacts != []:
                container_name = artifacts[0].container.name
                for artifact in artifacts:
                    try:
                        if artifact.parent_process.type.name in PROCESS_TYPE:
                            if artifact.parent_process.type.name == 'Size Selection (Pippin)' and artifact.parent_process.parent_processes()[0].type.name != 'Library Pooling (RAD-seq) v1.0':
                                process_name = ''
                            elif artifact.parent_process.type.name == 'Purification' and artifact.parent_process.parent_processes()[0].type.name != 'Enrich DNA fragments (TruSeq RNA) 4.0':
                                process_name = ''
                            else:
                                process_name = str(artifact.parent_process.type.name)
                        else:
                            process_name = ''
                        for sample in artifact.samples:
                            project_list.append(str(sample.name).split('_')[0])
                    except AttributeError:
                        process_name = 'Sample Plate'
                        for sample in artifact.samples:
                            project_list.append(str(sample.name).split('_')[0])
                    except Exception:
                        process_name = ''
                        for sample in artifact.samples:
                            project_list.append(str(sample.name).split('_')[0])
                project_list = list(set(project_list))
            new_entry.append({'_id': id, 'name': container_name, 'process': process_name, 'projects': project_list})
        # Import to couchdb
        db.update(new_entry)
    return db


# Query database with project ID
def query_plate_database(db, project):
    results = []
    for row in db.view('_all_docs'):
        if project in db[row.id]['projects'] and db[row.id]['process'] != '':
            results.append([row.id, db[row.id]['name'], db[row.id]['process'], ','.join(db[row.id]['projects'])])
    return results


# Read in database and query project
def main(lims, db, project):
    db = update_plate_database(lims, db)
    results = query_plate_database(db, project)

    if len(results) == 0:
        print("No plate found for project {}.".format(project))
        return 0
    else:
        print('<table class="table table-striped">')
        print('<tr><th>Plate ID</th><th>Plate Name</th><th>Source</th><th>Projects</th></tr>')
        for i in results:
            print("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(i[0], i[1], i[2], i[3]))
        print("</table>")


if __name__ == "__main__":
    parser = ArgumentParser(description=DESC)
    parser.add_argument('-p', '--project', default='P9804', dest='project', help='Project ID for querying plates')
    parser.add_argument(
        '--config',
        default="{0}/conf/LIMS2DB/post_process.yaml".format(os.environ["HOME"]),
        help="The config file for the script, by default '~/conf/LIMS2DB/post_process.yaml'"
        )
    args = parser.parse_args()
    lims = Lims(BASEURI, USERNAME, PASSWORD)
    lims.check_version()
    with open(args.config) as conf_file:
        conf = yaml.safe_load(conf_file)
    db_conf = conf['statusdbdev']
    url = "http://{0}:{1}@{2}:{3}".format(db_conf['username'], db_conf['password'], db_conf['url'], db_conf['port'])
    couchserver = couchdb.Server(url)
    dbname = "plates"
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)
    main(lims, db, args.project)
