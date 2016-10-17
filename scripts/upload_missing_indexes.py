#! /usr/bin/env python
import argparse
import subprocess

from genologics.entities import *
from genologics.lims import *
from genologics.config import BASEURI, USERNAME, PASSWORD


def main(args):
    lims=Lims(BASEURI, USERNAME, PASSWORD)
    hostname=BASEURI.split("//")[-1]
    outfile="custom_indexes.xml"
    indexes=[]
    with open(args.file) as f:
        indexes=[x.strip() for x in f.readlines()]


    to_upload=[]
    for idx in indexes:
        lims_rt=lims.get_reagent_types(name=idx)
        if not lims_rt:
            to_upload.append(idx)

    if to_upload:
        xml=make_xml(to_upload)

        with open(outfile, 'w') as of:
            of.write(xml)
        command=['scp',outfile, 'glsjboss@{}:/opt/gls/clarity/tools/config-slicer/'.format(hostname)]
        subprocess.call(command)
        command=['ssh', 'glsjboss@{}'.format(hostname),'""/opt/gls/clarity/bin/java -jar /opt/gls/clarity/tools/config-slicer/config-slicer-3.0.24.jar -k /opt/gls/clarity/tools/config-slicer/{of} -o import -s {hn} -u {un} -p {pw}""'.format(of=outfile,hn=hostname,un=USERNAME,pw=PASSWORD)]
        subprocess.call(command)
        print "Uploaded {} indexes".format(len(indexes))
    else:
        print "All the indexes in {} are already in the LIMS".format(args.file)



def make_xml(idxs):
    opentag='<config ApiVersion="v2,r20" ConfigSlicerVersion="3.0-compatible">\n<ReagentTypes>\n'
    closetag='</ReagentTypes>\n</config>'
    entries=[]
    for idx in idxs:
        entry="""<rtp:reagent-type xmlns:rtp="http://genologics.com/ri/reagenttype" name="{s}">
    <special-type name="Index">
        <attribute value="{s}" name="Sequence"/>
    </special-type>
    <reagent-category>Custom index</reagent-category>
</rtp:reagent-type>
""".format(s=idx)
        entries.append(entry)

    return"{}\n{}\n{}".format(opentag, '\n'.join(entries), closetag)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file")
    args = parser.parse_args()
    main(args)
