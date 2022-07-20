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
            mi = min(int(float(ls[1])), int(float(ls[2])))
            ma = max(int(float(ls[1])), int(float(ls[2])))
            if ls[0] in data:
                data[ls[0]].append([ma - mi, mi, ma]+ ls[3:])
            else:
                data[ls[0]] = [[ma - mi, mi, ma] + ls[3:]]
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
            if x[0] >= minsize:
                data2[key].append(x)
    return data2

def splitting(data, outname, what, number = 10):
    """
    Splitting the output - wrapper around write function
    :param data: bed data
    :param outname: Name of the output file
    :param what: see write function
    :param number: number of entries in file
    :return:
    """
    split = dict()
    count = 0
    for index, (key, value) in enumerate(data.items()):
            if index % number == 0 and index != 0:
                write(split, what, outname + "split" + str(count))
                split = dict()
                count += 1
            split[key] = value
    write(split, what, outname + "split" + str(count))


def write(data, what, outname):
    """
    Write file function
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
                    print(key + "\t" + "\t".join([str(x1) for x1 in x[1:]]) + what2, file = fi)
    else:
        for key, value in data.items():
            for x in value:
                print(key + "\t" + "\t".join([str(x1) for x1 in x[1:]]) + what2, file=sys.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="BED file", required=True)
    parser.add_argument("-w", "--what", help="add these dummy columns (comma sep)")
    parser.add_argument("-s", "--size", help="Filter out everything smaller than this size", type=int)
    parser.add_argument("--split", help = "Split with THIS many entries per file", type=int)
    parser.add_argument("-o", "--out", help="output file")
    args = parser.parse_args()
    what = []
    if args.what != None:
        what = [str(x) for x in args.what.split(",")]
    print("Reading BED file", file = sys.stderr)
    bed = read_bed(args.input)
    if args.size is not None:
        print("Filter by size", file=sys.stderr)
        bed = filter_min_size(bed, int(args.size))
    print("Writing output file", file=sys.stderr)
    if args.split is not None:
        splitting(bed, args.out, what, args.split)
    else:
        write(bed, what, outname=args.out)
