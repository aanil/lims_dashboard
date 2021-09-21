#!/usr/bin/env python
import sys
from argparse import ArgumentParser
import subprocess
import logging


def makeBarcode(barcode):
    """ Construct label with sampleName as human readable and barcode """
    lines = []
    lines.append("^XA")  # start of label
    # download and store format, name of format,
    # end of field data (FS = field stop)
    lines.append("^DFFORMAT^FS")
    lines.append("^LH0,0")  # label home position (label home = LH)
    # AF = assign font F, field number 1 (FN1),
    # print text at position field origin (FO) rel. to home
    lines.append("^FO40,20^AFN 78,39^FN1^FS")
    # BC=barcode 128, field number 2, Normal orientation,
    # height 70, no interpreation line.
    lines.append("^XZ")  # end format

    lines.append("^XA")  # start of label format
    lines.append("^XFFORMAT^FS")  # label home position
    lines.append("^FN1^FD{0}^FS".format(barcode))  # this is the printed barcode
    lines.append("^XZ")
    return lines


def getArgs():
    desc = (" Prints the text on zebra barcode printer")
    parser = ArgumentParser(description=desc)
    parser.add_argument('-n', '--name', nargs='+', type=str, default='test',
                        help=('Prints a label with the given text'))
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
    log = get_logger("print_label")
    if isinstance(args.name, list):
        args.name = " ".join(args.name)
    lines = makeBarcode(args.name)
    lp_args = ["lp"]
    lp_args.extend(["-d", "Zebra"])
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
        stdout,stderr = sp.communicate()  # Will wait for sp to finish
        log.info('printed label {0} .'.format(args.name))
        log.info('lp stdout: {0}'.format(stdout))
        log.info('lp stderr: {0}'.format(stderr))
        sp.stdin.close()
    else:
        print("\n".join(lines))
        print(lp_args)


if __name__ == '__main__':
    arguments = getArgs()
    main(arguments)
