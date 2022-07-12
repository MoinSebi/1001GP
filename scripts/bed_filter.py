#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: moinSebi

TODO:
- Max size filter
"""
import sys
import argparse

def read_bed(filename):
    """
    Reading a BED file

    :param filename: Path to the filename
    :return:
    """
    data = dict()
    with open(filename) as file:
        for line in file.readlines():
            ls = line.split()
            mi = min(int(ls[1]), int(ls[2]))
            ma = max(int(ls[1]), int(ls[2]))
            if ls[0] in data:
                data[ls[0]].append((mi, ma, ma - mi))
            else:
                data[ls[0]] = [(mi, ma, ma - mi)]
    return data

def filter_min_size(data, minsize):
    """

    :param data: bed file content
    :param minsize: minimum size
    :return:
    """
    data2 = dict()
    for key, value in data.items():
        data2[key] = []
        for x in value:
            if x[2] >= minsize:
                data2[key].append(x)
    return data2


def write(data, what, outname):
    """

    :param data: Bed file content
    :param what: Columns to add
    :param outname: Name of the output file
    :return:
    """
    what2 = ""
    if len(what) != 0:
        what2 = "\t" + "\t".join([str(x1) for x1 in what])
    if outname is not None:
        with open(outname, "w") as fi:
            for key, value in data.items():
                for x in value:
                    print("\t".join([str(x1) for x1 in x]) + what2, file = fi)
    else:
        for key, value in data.items():
            for x in value:
                print("\t".join([str(x1) for x1 in x]) + what2, file=sys.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="BED file", required=True)
    parser.add_argument("-w", "--what", help="add these dummy columns (comma sep)")
    parser.add_argument("-s", "--size", help="Filter out everything smaller than this size", type=int)
    parser.add_argument("-o", "--out", help="output file")
    args = parser.parse_args()
    what = [str(x) for x in parser.what.split(",")]
    bed = read_bed(args.input)
    if args.size is not None:
        bed = filter_min_size(bed, int(args.size))
    write(bed, what, outname=args.out)
