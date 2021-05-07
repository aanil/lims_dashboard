#!/usr/bin/env python
from __future__ import print_function

from argparse import ArgumentParser
import subprocess
import logging


def makeNSampleNameBarcode(samples_number):
    """ Construct label with sampleName as human readable and barcode """
    lines = []
    lines.append("^XA")  # start of label
    # download and store format, name of format,
    # end of field data (FS = field stop)
    lines.append("^DFFORMAT^FS")
    lines.append("^LH0,0")  # label home position (label home = LH)
    # AF = assign font F, field number 1 (FN1),
    # print text at position field origin (FO) rel. to home
    lines.append("^FO360,20^AFN 78,39^FN1^FS")
    # BC=barcode 128, field number 2, Normal orientation,
    # height 70, no interpreation line.
    lines.append("^FO70,5^BCN,70,N,N^FN2^FS")
    lines.append("^XZ")  # end format

    for nb in range(1, samples_number+1):
        lines.append("^XA")  # start of label format
        lines.append("^XFFORMAT^FS")  # label home position
        lines.append("^FN1^FDSample_{0}^FS".format(nb))  # this is the printed barcode
        lines.append("^FN2^FDSample_{0}^FS".format(nb))  # this is text next to the barcode
        lines.append("^XZ")
    return lines


def getArgs():
    desc = (" Prints up to 96 barcodes on zebra barcode printer")
    parser = ArgumentParser(description=desc)
    parser.add_argument('--number', type=int, default=96,
                        help=('Prints X labels, from sample_1 to sample_X'))
    parser.add_argument('--test', action="store_true",
                        help=('only prints the file and the lp command'))
    return parser.parse_args()


def get_logger(name):
    mainlog = logging.getLogger(name)
    mainlog.setLevel(level=logging.INFO)
    mfh = logging.StreamHandler()
    mft = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mfh.setFormatter(mft)
    mainlog.addHandler(mfh)
    return mainlog


def main(args):
    log = get_logger("zebra_quiagen_barcodes")
    lines = makeNSampleNameBarcode(args.number)
    lp_args = ["lp"]
    lp_args.extend(["-h", "homer2.scilifelab.se:631"])
    lp_args.extend(["-d", "zebrabarcode"])
    if not args.test:
        lp_args.append("-")  # lp accepts stdin if '-' is given as filename
        logging.info('Ready to call lp for printing.')
        if sys.version_info[0] == 3:
            sp = subprocess.Popen(lp_args,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  encoding='utf8')
            sp.stdin.write(str('\n'.join(lines), 'utf-8'))
        elif sys.version_info[0] == 2:
            sp = subprocess.Popen(lp_args,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            sp.stdin.write(unicode('\n'.join(lines), 'utf-8'))
        logging.info('lp command is called for printing.')
        stdout, stderr = sp.communicate()  # Will wait for sp to finish
        log.info('printed {0} labels.'.format(args.number))
        log.info('lp stdout: {0}'.format(stdout))
        log.info('lp stderr: {0}'.format(stderr))
        sp.stdin.close()
    else:
        print("\n".join(lines))
        print(lp_args)


if __name__ == '__main__':
    arguments = getArgs()
    main(arguments)
