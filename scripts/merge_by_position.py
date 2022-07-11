#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022-07-11


Comment:
For not reading the whole data frame (99% is SNPs)
--> grep -v "SNP" file.csv > file_noSNP.csv
"""


import pandas as pd
import argparse
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster


def filter_syri(df1):
    """
    Read a merged syri data frame (without SNPs)
    Filter criteria:
        - Sample of reference length is bigger than 50 bp


    :param df1: Data frame 1
    :return: Filtered data frame
    """
    # Remove alignment
    df = df1.loc[df1[10].apply(lambda x: x[-2:] != "AL")]

    # Change data type to int
    df[1] = df[1].astype(int)
    df[2] = df[2].astype(int)
    df[6] = df[6].astype(int)
    df[7] = df[7].astype(int)
    df[15] = df[15].astype(str)
    df[14] = df[14].astype(str)


    # Remove SNPs
    df = df.loc[df[10] != "SNP"]
    # Remove SYN
    df = df.loc[df[10] != "SYN"]
    df = df.rename(columns={15: "sample"})
    df = df.rename(columns={14: "ref"})
    df = df.rename(columns={13: "len_sample"})
    df = df.rename(columns={12: "len_ref"})

    # Sort by length
    df = df.loc[(df["len_sample"] >= 50) | (df["len_ref"] >= 50)]
    return df


def readList(listname):
    """

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
                print(t1.iloc[i].index)
            else:
                k[y] = [(t1.iloc[i].name, l1[i])]
        else:
            i2 = i - lenn
            if y in k:
                k[y].append((t2.iloc[i2].name, l2[i2]))
            else:
                k[y] = [(t2.iloc[i2].name, l2[i2])]
    return k

def cluster(alldf, l):
    """
    :param alldf: pandas DataFrame
    :param l: list
    :return:
    """
    rr = dict()

    for y in l:
        print(y)
        t1 = alldf.loc[alldf["sample"] == y].loc[alldf["len_sample"] != 0]
        t2 = alldf.loc[alldf["ref"] == y].loc[alldf["len_ref"] != 0]
        print(len(alldf.loc[alldf["ref"] == y]))
        print(t2)
        rr[y] = dict()
        for x in ["Chr1", "Chr2", "Chr3", "Chr4", "Chr5"]:
            dft1 = t1.loc[t1[5] == x]
            dft2 = t2.loc[t2[0] == x]

            l1 = sortlist(np.array([dft1[6], dft1[7]]).T)
            l2 = sortlist(np.array([dft2[1], dft2[2]]).T)
            print("SV found as reference", len(l2))
            print("SV found as sample", len(l1))
            y_pred = fcluster(linkage(np.concatenate((l1, l2))), 10, criterion='distance')
            print(len(y_pred))
            print(len(set(y_pred)))
            rr[y][x] = clusterthis(y_pred, dft1, dft2, l1, l2, len(l1))
            print("done\n")
    return rr



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="fasta file", required=True)
    parser.add_argument("-o", "--out", help="output file")
    parser.add_argument("-l", "--list", help = "list of all samples to merge")
    args = parser.parse_args()

    li = readList(args.list)
    df = pd.read_csv(args.input, sep = "\t", header = None)
    df = filter_syri(df)
    cluster(df, li)
    print(df)
    print(li)




