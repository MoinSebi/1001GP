#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: moinSebi
"""
import argparse
import sys


def read_annafile(filename):
    """

    :param filename: File name
    :return: data [line.split()]
    """
    data = []
    with open(filename) as file:
        for i, line in enumerate(file.readlines()):
            if i != 0:
                ls = line.split()
                data.append(ls)
    return data

def write_output(filename, data):
    """

    :param filename: File name
    :param data: data from read_annafile
    :return: file with file name
    """
    if filename != None:
        with open(filename, "w") as file:
            for x in data:
                print(x[3] + "_Chr" + x[0] + "\t" + x[1] + "\t" + x[2], file = file)
    else:
        for x in data:
            print(x[3] + "_Chr" + x[0] + "\t" + x[1] + "\t" + x[2], file=sys.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="anna result file", required=True)
    parser.add_argument("-o", "--out", help="output file")
    args = parser.parse_args()