#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022-07-11
"""
import argparse
from scipy.cluster.hierarchy import linkage, fcluster
import numpy as np
import sys


def read_bed(filename):
    """
    Reading a BED file

    :param filename: Path to the filename
    :param typ: "g" = Graph; "a" = Anna; "s" = Syri
    :return:
    """
    print("Reading the file", file  = sys.stderr)
    data = dict()
    with open(filename) as file:
        for line in file.readlines():
            ls = line.split()
            if ls[0] in data:
                data[ls[0]].append([min(int(ls[1]), int(ls[2])), max(int(ls[1]), int(ls[2])), str(ls[3])])
            else:
                data[ls[0]] = [[min(int(ls[1]), int(ls[2])), max(int(ls[1]), int(ls[2])), str(ls[3])]]
    return data

def cluster(data: dict, dis = 10):
    """
    Wrapper function around clustering start, end positions
    :param data: dict(fasta_entry -> [(start, end)]
    :param dis: distance in clustering
    :return:
    """
    print("Clustering: {}".format(len(data)), file  = sys.stderr)
    dataschmata = dict()
    for key, value in data.items():
        valu = [(x[0], x[1]) for x in value]
        valu2 = np.array(list(set(valu)))
        y_pred = fcluster(linkage(valu2), dis, criterion='distance')
        dd = cluster1(y_pred, valu)
        print("Chr:Entries:RDup:Cluster\t", ":".join([key, str(len(value)),  str(len(valu2)),  str(len(dd))]), file  = sys.stderr)

        okey = merge_typ(dd, value)
        dataschmata[key] = [test(dd, valu), okey]
    return dataschmata


def test(cluster2index: dict, valuu):
    o = dict()
    for key, val in cluster2index.items():
        o[key] = valuu[val[0]]
    return o


def merge_typ(cluster2index: dict, value):
    o = dict()
    for key, val in cluster2index.items():
        o[key] = []
        for x in val:
            o[key].append(value[x][2])

    okey = dict()
    for key, val in o.items():
        okey[key] = "".join(sorted(list(set(val))))

    return okey


def cluster1(ypred: list, value):
    """
    Merge all entries which are in the same cluster

    :param ypred: cluster list
    :return: cluster2index: dict(cluster_id -> [index])
    """
    cluster2index = dict()
    for i, x in enumerate(ypred):
        if x in cluster2index:
            cluster2index[x].append(i)
        else:
            cluster2index[x] = [i]
    return cluster2index

def write_self(data, outname):
    """
    :param df: pandas DataFrame
    :param outname: name of the output file
    :return: File with the outname
    """
    if outname != "-":
        with open(outname, "w") as fi:
            for key, value in data.items():
                for key2, value2 in value[0].items():
                    print("\t".join([str(key), str(value2[0]), str(value2[1]), str(value[1][key2])]), file = fi)
    else:
        for key, value in data.items():
            for key2, value2 in value[0].items():
                print("\t".join([str(key), str(value2[0]), str(value2[1]), str(value[1][key2])]), file=sys.stdout)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="graph BED file", required=True)
    parser.add_argument("-o", "--output", help = "Output file name (can also be -)", required=True)
AA    parser.add_argument("-d", "--distance", help = "Distance of merge", type=int)
    args = parser.parse_args()

    bed_total = read_bed(args.input)
    if args.distance is not None:
        k = cluster(bed_total, int(args.distance))
    else:
        k = cluster(bed_total)

    write_self(k, args.output)

