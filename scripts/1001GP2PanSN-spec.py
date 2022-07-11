#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022-07-11
"""

import argparse
import sys


def readFasta(filename):
    """

    :param filename: string
    :return: list of [header, fasta] entries
    """
    data = []
    header = ""
    fasta = ""
    with open(filename) as file:
        for x in file.readlines():
            if x.startswith(">"):
                if len(header) != 0:
                    data.append([header, fasta])
                fasta = ""
                header = x
            else:
                fasta += x.replace("\n", "")
        data.append([header, fasta])
    return data


def newHeader(sample, data, dell, numb):
    """
    Adds delimiter and haplotyp as a header


    :param sample: Sample name
    :param data: Fasta data
    :param dell: Delimitier data
    :return: Modified [header, sequence] list
    """
    for x in data:
        x[0] = sample + dell + "1" + dell + x[0].replace(">", "").split("_")[numb-1]


def writeFasta(outname, data):
    """
    Write a new fasta
    :param outname: Name of the output file
    :param data: Data which is written
    :return: New file with filename
    """
    with open(outname, "w") as file:
        for x in data:
            file.write(">" + x[0].replace("\n", "") + "\n")
            file.write(x[1].replace("\n", "") + "\n")


def readList(listname):
    """

    :param listname: name of the list to read
    :return: list data structure of the list
    """
    ll = []
    with open(listname) as file:
        for line in file.readlines():
            ll.append(line)

    return ll


def check_list(data, ll):
    """
    Check if the data (data) and the given list are of the same size

    :param data: Data
    :param ll: List
    :return: bool if same size
    """
    return len(data) == len(ll)


def add_haplo(data, deli):
    for x in data:
        x[0] = x[0].replace(">", "").split("_")[0] + deli + "1" + deli + x[0].replace(">", "").split("_")[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="fasta file", required=True)
    parser.add_argument("-o", "--out", help="output file", required=True)
    parser.add_argument("-s", "--sample", help="If not set, take sample name")
    parser.add_argument("-d", "--delimiter", help="delimiter", default="#")
    parser.add_argument("-c", "--chromosome", help="Take chromosome name from this index (sep by '_')", default = 1)
    parser.add_argument("-n", "--near", help = "Near perfect (only missing haplotype)", action="store_true")
    args = parser.parse_args()

    data = readFasta(args.input)
    if args.near is not None:
        print("Running in near perfect mode", file = sys.stderr)
        add_haplo(data, args.delimiter)
    else:
        print("Getting sample name from file name", file=sys.stderr)
        name = ".".join(args.input.split("/")[-1].split(".")[:-1])
        if args.sample is not None:
            name = args.sample
        chromosome = 1
        if args.chromosome is not None:
            chr = int(args.chromosome)
        if chr == 0:
            print("ERROR - 0 not allowed", file = sys.stderr)
        newHeader(name, data, args.delimiter, chr)

    print("Writing output fasta", file = sys.stderr)
    writeFasta(args.out, data)
