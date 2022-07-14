#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022-07-11

Comment:
Run for all files with and safe everything in one file:
parallel .syri_naming_filtering.py -i $1 > sum.txt ::: /ebio/abt6_projects8/1001g_plus_scaffolding/data/syri/1_SyRI_ALLvsALL_v1-6/*/*.syri.ou
"""
import pandas as pd
import argparse
import sys

def add_features(df, name_ref, name_sample):
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


    :param df: Data frame 1
    :return: Filtered data frame
    """


    # Change data type to int
    df[1] = df[1].astype(int)
    df[2] = df[2].astype(int)
    df[6] = df[6].astype(int)
    df[7] = df[7].astype(int)

    # Add length of the sample and reference
    df["len_sample"] = df[7] - df[6]
    df["len_ref"] = df[2] - df[1]
    df["sample"] = name_sample
    df["ref"] = name_ref
    # Sort by length
    return df

def filter_size(df, size = 50):
    df = df.loc[(df["len_sample"] >= size) | (df["len_ref"] >= size)]
    return df

def filter_al(df1):
    df = df1.loc[df1[10].apply(lambda x: x[-2:] != "AL")]
    return df

def filter_snps(df):
    df = df.loc[df[10] != "SNP"]
    return df

def filter_syn(df):
    df = df.loc[df[10] != "SYN"]
    return df


def filter_hdr(df):
    df = df.loc[df[10] != "HDR"]
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
    parser.add_argument("-f", "--filter", help = "size filter [default 50bp]", default=50)
    parser.add_argument("-a", "--al", help = "remove alignment [default on]", action="store_false", default=True)
    parser.add_argument("-s", "--snp", help="remove SNPS [default on]", action="store_false", default=True)
    parser.add_argument("--syn", help="remove syntenic regions [default on]", action="store_false", default=True)
    parser.add_argument("--hdr", help = "remove HDR [default off]", action = "store_true")

    args = parser.parse_args()

    # Read the DataFrame
    df = pd.read_csv(args.input, sep = "\t", header = None)


    name_ref = args.input.split("/")[-1].split("_")[0]
    name_sample = args.input.split("/")[-1].split("_")[1].split(".")[0]

    if args.al:
        df = filter_al(df)
    if args.syn:
        df = filter_syn(df)
    if args.hdr:
        df = filter_hdr(df)
    if args.snp:
        df = filter_snps(df)
    df2 = add_features(df, name_ref, name_sample)

    if args.filter is not None:
        print("Filtering", file = sys.stderr)
        df2 = filter_size(df2, int(args.filter))

    write_self(df2, args.out)


