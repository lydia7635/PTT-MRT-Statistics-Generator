#! /usr/bin python3
# -*- coding: utf-8 -*-
# format reference: https://www.ptt.cc/bbs/MRT/M.1626525007.A.004.html

import argparse
import os
from pyexcel_ods import get_data
import pyperclip
import wget
from format import *

def process_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', help="輸入西元年或民國年", type=int)
    parser.add_argument('month', help="輸入月份", type=int)
    return parser.parse_args()

class month_data():
    def __init__(self, year, month):
        self.filename = wget.download(f"https://web.metro.taipei/RidershipPerStation/{year}{month:02}_cht.ods")
        self.stat = get_data(self.filename)
        self.date_num = len(list(filter(lambda x: x, self.stat['出站資料']))) - 1

    def remove_file(self):
        os.unlink(self.filename)

class station_data():
    def __init__(self):
        self.station_dict = {}

    def initialize(self, data):
        # {station: [this_month, last_month, last_year, last_year_diff,
        #   this_month_rank, last_month_rank, last_year_rank]}
        for station in data.stat['出站資料'][0][1:]:
            self.station_dict[station] = [0, 0, 0, 0, -1, -1, -1]

    def calc_avg(self, data, list_idx):
        for date in range(data.date_num):
            for idx, station in enumerate(data.stat['出站資料'][0][1:]):
                self.station_dict[station][list_idx] += data.stat['出站資料'][date+1][idx+1]
            for idx, station in enumerate(data.stat['進站資料'][0][1:]):
                self.station_dict[station][list_idx] += data.stat['進站資料'][date+1][idx+1]
                
        for station in self.station_dict.keys():
            self.station_dict[station][list_idx] = int(self.station_dict[station][list_idx] / data.date_num + 0.5)

    def calc_diff(self, this_month_avg_idx, last_avg_idx, last_diff_idx):
        for station in self.station_dict.keys():
            this_month_avg = self.station_dict[station][this_month_avg_idx]
            last_avg = self.station_dict[station][last_avg_idx]
            self.station_dict[station][last_diff_idx] = (this_month_avg - last_avg)/last_avg * 100
    
    def print_items(self):
        for item in self.station_dict.items():
            print(item)

    def sort_and_rank(self, sort_idx, rank_idx):
        for idx, item in enumerate(sorted(self.station_dict.items(), key=lambda x: x[1][sort_idx], reverse=True)):
            item[1][rank_idx] = idx + 1


def main():
    args = process_argument()

    if args.year < 1950:
        args.year += 1911

    print(f"data from {args.year}/{args.month:02}")

    this_month = month_data(args.year, args.month)
    if args.month - 1 > 0:
        last_month = month_data(args.year, args.month - 1)
    else:
        last_month = month_data(args.year - 1, 12)
    last_year  = month_data(args.year - 1, args.month)

    dict = station_data()
    dict.initialize(this_month)

    dict.calc_avg(this_month, 0)
    dict.calc_avg(last_month, 1)
    dict.calc_avg(last_year,  2)

    dict.calc_diff(0, 2, 3)

    dict.sort_and_rank(3, 6)
    dict.sort_and_rank(1, 5)
    dict.sort_and_rank(0, 4)

    pyperclip.copy(generate_content(dict, args.year - 1911, args.month))
    print("\nCopied successfully!")
    
    this_month.remove_file()
    last_month.remove_file()
    last_year.remove_file()

if __name__ == '__main__':
    main()