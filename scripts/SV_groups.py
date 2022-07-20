#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/20/22

@author: moinSebi

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

def grouping(data):
    data2 = dict()
    count = 0
    for key, value in data.items():
        data2[key] = dict()
        open_start = 0
        open_end = 0
        count = 0
        mem = []
        print(len(value), file=sys.stderr)
        for x in value:
            if x[1] < open_end:
                # member
                if x[2] < open_end:
                    mem.append(x)
                else:
                    open_end = x[2]
                    mem.append(x)
            else:
                data2[key][count] = [open_start, open_end, mem]
                open_start = x[1]
                open_end = x[2]

                #print(open_start, open_end)
                mem = [x]
                count += 1
    return data2

def print_fast(data, filename):
    with open(filename, "w") as file:
        for key, value in data.items():
            for i, (key2, value2) in enumerate(value.items()):
                if i != 0:
                    print(";".join([",".join([str(x) for x in y]) for y in value2[2]]))
                    print(key, key2, "\t".join([str(x) for x in [value2[0], value2[1]]]) + "\t" + ";".join([",".join([str(x) for x in y]) for y in value2[2]]), file = file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="graph BED file", required=True)
    parser.add_argument("-o", "--output", help = "Output file name (can also be -)", required=True)
    args = parser.parse_args()
    data = read_bed(args.input)
    o = grouping(data)
    print_fast(o, args.output)

