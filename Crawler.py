# coding=utf-8
import json
import requests
from Stock import Stock

CRAW_URL = "https://18.push2his.eastmoney.com/api/qt/stock/kline/get?secid={}.{}&ut=fa5fd1943c7b386f172d6893dbfba10b" \
        "&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60," \
        "f61&klt=101&fqt=0&end=20500101&lmt=1 "


def current_day_stock(code):
    source = 0 if str(code).startswith("000") else 1
    url = CRAW_URL.format(source, code)
    response = requests.get(url).text
    rs_data = json.loads(response).get("data")
    k_line = str(rs_data.get("klines")[0])
    arr = k_line.split(",")
    return Stock(code, rs_data.get("name"), arr[2], arr[8])


if __name__ == "__main__":

    code = "000625"
    stock = current_day_stock(code)

    print(stock.code)
    print(stock.name)
    print(stock.price)
    print(stock.percent)
