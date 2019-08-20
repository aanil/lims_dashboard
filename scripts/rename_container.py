import argparse

from genologics.lims import Lims
from genologics.entities import Container
from genologics.config import BASEURI, USERNAME, PASSWORD


def main(args):
    lims = Lims(BASEURI, USERNAME, PASSWORD)
    cont = Container(lims, id=args.flowcell)
    cont.name = cont.id
    cont.put()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--flowcell", dest="flowcell")
    args = parser.parse_args()
    main(args)
