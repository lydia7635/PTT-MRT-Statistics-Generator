#! /usr/bin python3
# -*- coding: utf-8 -*-
# format reference: https://www.ptt.cc/bbs/MRT/M.1626525007.A.004.html

import argparse
import os
# from pyexcel_ods import get_data
import pyperclip
import wget
import pandas as pd
from format import *

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', help="輸入西元年或民國年", type=int)
    parser.add_argument('month', help="輸入月份", type=int)

    args = parser.parse_args()
    if args.year < 1950:
        args.year += 1911
    return args

class month_raw_data():
    def __init__(self, year, month):
        if month == 0:
            year -= 1
            month = 12
        self.time = { "year": year - 1911, "month": month }

        self.filename = wget.download(f"https://web.metro.taipei/RidershipPerStation/{year}{month:02}_cht.ods")
        self.raw = pd.read_excel(self.filename, engine='odf', sheet_name=None)
        self.remove_file()
        # print(self.raw)
        # print(self.raw['出站資料'].columns[1:])

    def remove_file(self):
        os.unlink(self.filename)

class statistics():
    def __init__(self, data):
        self.station_dict = {}
        self.station_name_list = data.raw['出站資料'].columns[1:]
        for station in self.station_name_list:
            self.station_dict[station] = {
                "curr_month": 0,
                "curr_month_rank": -1,
                
                "last_month": 0,
                "last_month_diff": 0,
                "last_month_rank": -1,

                "last_year": 0,
                "last_year_diff": 0,
                "last_year_diff_rank": -1,
            }

    def calc_avg(self, data, key):
        for station in self.station_name_list:
            date_num = data.raw['出站資料'][station].count()
            self.station_dict[station][key] += data.raw['出站資料'][station][:date_num].sum()
            self.station_dict[station][key] += data.raw['進站資料'][station][:date_num].sum()
            self.station_dict[station][key] = int(self.station_dict[station][key] / date_num + 0.5)

    def calc_diff(self, comp_key, diff_key):
        for station in self.station_dict.keys():
            curr_month_avg = self.station_dict[station]["curr_month"]
            comp_avg = self.station_dict[station][comp_key]
            self.station_dict[station][diff_key] = (curr_month_avg - comp_avg) / comp_avg * 100
    
    def print_items(self):
        for item in self.station_dict.items():
            print(item)

    def gen_rank(self, sort_key, rank_key):
        for idx, item in enumerate(sorted(self.station_dict.items(), key=lambda x: x[1][sort_key], reverse=True)):
            item[1][rank_key] = idx + 1


def main():
    args = parse_argument()
    print(f"generate MRT data from {args.year}/{args.month:02}")


    curr_month_raw = month_raw_data(args.year, args.month)
    last_month_raw = month_raw_data(args.year, args.month - 1)
    last_year_raw  = month_raw_data(args.year - 1, args.month)

    stat = statistics(curr_month_raw)

    stat.calc_avg(curr_month_raw, "curr_month")
    stat.calc_avg(last_month_raw, "last_month")
    stat.calc_avg(last_year_raw,  "last_year")

    stat.calc_diff("last_month", "last_month_diff")
    stat.calc_diff("last_year", "last_year_diff")

    stat.gen_rank("last_year_diff", "last_year_diff_rank")
    stat.gen_rank("last_month", "last_month_rank")
    stat.gen_rank("curr_month", "curr_month_rank")

    pyperclip.copy(generate_content(stat, curr_month_raw.time,
                                          last_month_raw.time,
                                          last_year_raw.time))
    print("\nCopied successfully!")

if __name__ == '__main__':
    main()