#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022-07-11


Comment:
For not reading the whole data frame (99% is SNPs)
--> grep -v "SNP" file.csv > file_noSNP.csv
"""
import sys

import pandas as pd
import argparse
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster


def filter_syri(df):
    """
    Read a merged syri data frame (without SNPs)
    Filter criteria:
        - Sample of reference length is bigger than 50 bp


    :param df1: Data frame 1
    :return: Filtered data frame
    """
    print("Reading SYRI", file = sys.stderr)

    # Change data type to int
    df[1] = df[1].astype(int)
    df[2] = df[2].astype(int)
    df[6] = df[6].astype(int)
    df[7] = df[7].astype(int)
    df[15] = df[15].astype(str)
    df[14] = df[14].astype(str)




    # Rename the columns
    df = df.rename(columns={15: "ref"})
    df = df.rename(columns={14: "sample"})
    df = df.rename(columns={13: "len_sample"})
    df = df.rename(columns={12: "len_ref"})
    return df


def readList(listname):
    """
    Reading a list of accession
    :param listname: name of the list to read
    :return: list data structure of the list
    """
    ll = []
    with open(listname) as file:
        for line in file.readlines():
            ll.append(str(line.replace("\n", "")))

    return ll

def sortlist(li):
    """
    Sorts a (int,int) list that it's always (small, big) value
    :param li: List of (int, int)
    :return: List (small, big)
    """
    return [(min(x[0], x[1]), max(x[0], x[1])) for x in li]


def clusterthis(ypred, t1, t2, l1, l2, lenn):
    """
    :param ypred: cluster output
    :param t1: DataFrame1
    :param t2: DataFrame2
    :param l1: values1
    :param l2: values2
    :param lenn: len of l1
    :return: dict(clusternumb -> (name, [start, stop]))
    """
    k = dict()
    for i, y in enumerate(ypred):
        if i < len(l1):
            if y in k:
                k[y].append((t1.iloc[i].name, l1[i]))
            else:
                k[y] = [(t1.iloc[i].name, l1[i])]
        else:
            i2 = i - lenn
            if y in k:
                k[y].append((t2.iloc[i2].name, l2[i2]))
            else:
                k[y] = [(t2.iloc[i2].name, l2[i2])]
    return k


def clusterthis2(ypred, t1, t2, l1, l2, lenn):
    """
    :param ypred: cluster output
    :param t1: DataFrame1
    :param t2: DataFrame2
    :param l1: values1
    :param l2: values2
    :param lenn: len of l1
    :return: dict(clusternumb -> (name, [start, stop]))
    """
    k = dict()
    for i, y in enumerate(ypred):
        if i < len(l1):
            if y in k:
                k[y].append(i)
            else:
                k[y] = [(t1.iloc[i].name, l1[i])]
        else:
            i2 = i - lenn
            if y in k:
                k[y].append(i)
            else:
                k[y] = [(t2.iloc[i2].name, l2[i2])]
    return k

def cluster(alldf, l):
    """
    :param alldf: pandas DataFrame
    :param l: list
    :return:
    """
    print("Clustering", file = sys.stderr)
    rr = dict()

    for y in l:
        t1 = alldf.loc[alldf["sample"] == y].loc[alldf["len_sample"] != 0]
        t2 = alldf.loc[alldf["ref"] == y].loc[alldf["len_ref"] != 0]
        rr[y] = dict()
        for x in ["Chr1", "Chr2", "Chr3", "Chr4", "Chr5"]:
            dft1 = t1.loc[t1[5] == x]
            dft2 = t2.loc[t2[0] == x]

            l1 = sortlist(np.array([dft1[6], dft1[7]]).T)
            l2 = sortlist(np.array([dft2[1], dft2[2]]).T)
            print(y + "_" + x, file = sys.stderr)
            print("SV found as reference", len(l2), file = sys.stderr)
            print("SV found as sample", len(l1), file = sys.stderr)
            y_pred = fcluster(linkage(np.concatenate((l1, l2))), 10, criterion='distance')
            print(len(y_pred))
            print(len(set(y_pred)))
            rr[y][x] = clusterthis2(y_pred, dft1, dft2, l1, l2, len(l1))
            print("done\n")
    return rr

def write(rr, prefix):
    # Iterate over all genomes
    for k1, v1 in rr.items():
        with open(prefix + "_" + k1, "w") as file:
            # Iterate over chromosomes
            for k2, v2 in v1.items():
                # Iterate over all clusters
                for k3, v3 in v2.items():
                    file.write("\t".join([k1 + "_" + k2, "\t".join([str(x) for x in v3[0][1]])]) + "\n")

                    #file.write("\t".join([k1 + "_" + k2, "\t".join([str(x) for x in v3[0][1]])]) + "\t" + str(v3[0][1][1] - v3[0][1][0]) + "\t"
                               #"\t".join([str(x) for x in v3[1:]]) + "\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="fasta file", required=True)
    parser.add_argument("-o", "--out", help="output file")
    parser.add_argument("-l", "--list", help = "list of all samples to merge")
    args = parser.parse_args()
    print("testing")

    li = readList(args.list)
    print("test2")
    df = pd.read_csv(args.input, sep = "\t", header = None)
    print("test2")
    df = filter_syri(df)
    rr = cluster(df, li)
    write(rr, args.out)




