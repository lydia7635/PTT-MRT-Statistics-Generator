import const

def get_month_rank_diff_sign(curr_month_rank, last_month_rank):
    if curr_month_rank < last_month_rank:
        rank_diff = f"\033[1;31;44m↑{last_month_rank-curr_month_rank:2}\033[0m"
    elif curr_month_rank > last_month_rank:
        rank_diff = f"\033[1;32;44m↓{curr_month_rank-last_month_rank:2}\033[0m"
    else:
        rank_diff = f"\033[1;44m   -\033[0m"
    return rank_diff

def get_station(station):
    station_str = const.STATION_NAME[station]
    return station_str

def get_year_diff_rank_sign(last_year_diff, last_year_diff_rank):
    rank_str = ""
    if last_year_diff_rank <= 10 and last_year_diff > 0:
        rank_str = f"\033[1;35m▲{last_year_diff_rank}\033[m"
    elif last_year_diff_rank > const.STATION_NUM - 10 and last_year_diff < 0:
        rank_str = f"\033[1;32m▼{const.STATION_NUM + 1 - last_year_diff_rank}\033[m"
    return rank_str

def generate_content(stat, curr_month_time, last_month_time, last_year_time):
    content = f'''        　       　台北捷運{curr_month_time["year"]}年{curr_month_time["month"]:02}月各站進出旅運量日平均

      　        　　    {curr_month_time["year"]}年{curr_month_time["month"]:02}月  {last_month_time["year"]}年{last_month_time["month"]:02}月  本月    {last_year_time["year"]}年{last_year_time["month"]:02}月  本月
    　     　　          日平均     日平均   較上月    日平均  較去年同期
  　  　　               進出量     進出量    增減     進出量    增減
　　　名次   車站名      (人次)     (人次)    (％)     (人次)    (％)
────────────────────────────────────
'''

    for idx, item in enumerate(sorted(stat.station_dict.items(), key=lambda x: x[1]["curr_month"], reverse=True)):
        station = get_station(item[0])
        curr_month_avg = item[1]["curr_month"]
        last_month_avg = item[1]["last_month"]
        last_year_avg = item[1]["last_year"]
        
        curr_month_rank = item[1]["curr_month_rank"]
        last_month_rank = item[1]["last_month_rank"]
        month_rank_diff_sign = get_month_rank_diff_sign(curr_month_rank, last_month_rank)
        
        last_month_diff = item[1]["last_month_diff"]
        last_year_diff = item[1]["last_year_diff"]
        last_year_diff_rank = item[1]["last_year_diff_rank"]
        last_year_diff_rank_sign = get_year_diff_rank_sign(last_year_diff, last_year_diff_rank)

        content += f" {month_rank_diff_sign} {curr_month_rank:3}  {station}  {curr_month_avg:7,}    {last_month_avg:7,}  {last_month_diff:6.2f}    {last_year_avg:7,}  {last_year_diff:6.2f} {last_year_diff_rank_sign}\n"
        if idx % 10 == 9:
            content += "\n"

    content += '''────────────────────────────────────

1. 資料來源：台北捷運公司
     https://www.metro.taipei/cp.aspx?n=FF31501BEBDD0136

   計算方式：
     （入站+出站）/營運日數　

2. \033[44m    \033[m色塊內「\033[1;31m↑\033[m」及「\033[1;32m↓\033[m」分別表示該車站名次比上月上升及下降（數字為排
   名數）；「\033[1;35m▲\033[m」及「\033[1;32m▼\033[m」分別表示運量比去年同期成長及衰退最多之車站（數
  字為依成長或衰退百分比排名之名次）。

3. 本文採用 cosmic 、 kuso10582 、 Wusher 及 ntuce016 板友的格式。'''

    return content