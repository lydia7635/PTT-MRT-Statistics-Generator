import const

def get_month_rank_diff(this_month_rank, last_month_rank):
    if this_month_rank < last_month_rank:
        rank_diff = f"\033[1;31;44m↑{last_month_rank-this_month_rank:2}\033[0m"
    elif this_month_rank > last_month_rank:
        rank_diff = f"\033[1;32;44m↓{this_month_rank-last_month_rank:2}\033[0m"
    else:
        rank_diff = f"\033[1;44m   -\033[0m"
    return rank_diff

def get_station(station):
    station_str = const.STATION_NAME[station]
    return station_str

def get_diff_rank(last_year_diff, last_year_diff_rank):
    rank_str = ""
    if last_year_diff_rank <= 10 and last_year_diff > 0:
        rank_str = f"\033[1;35m▲{last_year_diff_rank}\033[m"
    elif last_year_diff_rank > const.STATION_NUM - 10 and last_year_diff < 0:
        rank_str = f"\033[1;32m▼{const.STATION_NUM + 1 - last_year_diff_rank}\033[m"
    return rank_str

def generate_content(dict, year, month):
    content = f'''        　       　台北捷運{year}年{month:02}月各站進出旅運量日平均

      　        　　    {year}年{month:02}月  {year}年{month-1:02}月  本月    {year-1}年{month:02}月  本月
    　     　　          日平均     日平均   較上月    日平均  較去年同期
  　  　　               進出量     進出量    增減     進出量    增減
　　　名次   車站名      (人次)     (人次)    (％)     (人次)    (％)
────────────────────────────────────
'''

    for idx, item in enumerate(sorted(dict.station_dict.items(), key=lambda x: x[1][0], reverse=True)):
        month_rank_diff = get_month_rank_diff(item[1][4], item[1][5])
        this_month_rank = item[1][4]
        station = get_station(item[0])
        this_month_avg = item[1][0]
        last_month_avg = item[1][1]
        last_month_diff = (this_month_avg - last_month_avg)/last_month_avg * 100
        last_year_avg = item[1][2]
        last_year_diff = item[1][3]
        last_year_rank = get_diff_rank(item[1][3], item[1][6])

        content += f" {month_rank_diff} {this_month_rank:3}  {station}  {this_month_avg:7,}    {last_month_avg:7,}  {last_month_diff:6.2f}    {last_year_avg:7,}  {last_year_diff:6.2f} {last_year_rank}\n"
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

   
3. 第一次整理，若資料有錯誤或是排名錯誤，請來信告知，會盡快修改。

4. 本文採用 cosmic 、 kuso10582 、 Wusher 及 ntuce016 板友的格式。'''

    return content