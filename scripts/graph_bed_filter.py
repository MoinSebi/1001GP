#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/20/22

@author: moinSebi

"""
import pandas as pd
import argparse

def read_bed(filename):
    df = pd.read_csv(filename, sep = "\t", header = None)
    return df

def filter_df(df):
    df = df.loc[(df[7] > 50) | ((df[7] == 0) & (df[8] > 50))]
    return df


def write_df(df, outname):
    with open(outname, "w") as file:
        for key, value in df.iterrows():
            print("\t".join([str(x) for x in [value[0], value[1], value[2]]]), file = file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="graph BED file", required=True)
    parser.add_argument("-o", "--output", help = "Output file name (can also be -)", required=True)
    args = parser.parse_args()

    data = read_bed(args.input)
    data2 = filter_df(data)
    write_df(data2, args.output)
