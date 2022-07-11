#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022-07-11

@author: moinSebi

"""
import pandas as pd
import argparse
import sys

def filter_syri(df1, name_ref, name_sample, snp):
    """
    Read a merged syri data frame (without SNPs)
    Added columns:
        - len_sample: length of the variation in the sample
        - len_ref: length of the variation in the ref
        - sample: sample name
        - ref: ref name
    Filter criteria:
        - "AL" tags
        - "SNPs"
        - Sample or reference length is bigger than 50 bp


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

    # Remove SNPs
    if snp:
        df = df.loc[df[10] != "SNP"]

    # Add length of the sample and reference
    df["len_sample"] = df[7] - df[6]
    df["len_ref"] = df[2] - df[1]
    df["sample"] = name_sample
    df["ref"] = name_ref
    # Sort by length
    df = df.loc[(df["len_sample"] >= 50) | (df["len_ref"] >= 50)]
    return df


def write_self(df, outname):
    """
    :param df: pandas DataFrame
    :param outname: name of the output file
    :return: File with the outname
    """
    if outname != "-":
        with open(outname, "w") as fi:
            for x,y in df.iterrows():
                print("\t".join([str(x) for x in y.values]), file = fi)
    else:
        for x, y in df.iterrows():
            print("\t".join([str(x) for x in y.values]), file = sys.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="fasta file", required=True)
    parser.add_argument("-o", "--out", help="output file")
    parser.add_argument("-s", "--snp", help="remove SNPS", action="store_true", default=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep = "\t", header = None)
    name_ref = args.input.split("/")[-1].split("_")[0]
    name_sample = args.input.split("/")[-1].split("_")[1].split(".")[0]
    df2 = filter_syri(df, name_ref, name_sample, args.snp)
    write_self(df2, args.out)


