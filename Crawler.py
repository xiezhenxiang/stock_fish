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
    #name = getFirstLetter(rs_data.get("name"))
    name = rs_data.get("name")
    return Stock(code, name, arr[2], arr[8])


# 中文获取首字母(第一个文字)
def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'A'
        if asc >= -20283 and asc <= -19776:
            return 'B'
        if asc >= -19775 and asc <= -19219:
            return 'C'
        if asc >= -19218 and asc <= -18711:
            return 'D'
        if asc >= -18710 and asc <= -18527:
            return 'E'
        if asc >= -18526 and asc <= -18240:
            return 'F'
        if asc >= -18239 and asc <= -17923:
            return 'G'
        if asc >= -17922 and asc <= -17418:
            return 'H'
        if asc >= -17417 and asc <= -16475:
            return 'J'
        if asc >= -16474 and asc <= -16213:
            return 'K'
        if asc >= -16212 and asc <= -15641:
            return 'L'
        if asc >= -15640 and asc <= -15166:
            return 'M'
        if asc >= -15165 and asc <= -14923:
            return 'N'
        if asc >= -14922 and asc <= -14915:
            return 'O'
        if asc >= -14914 and asc <= -14631:
            return 'P'
        if asc >= -14630 and asc <= -14150:
            return 'Q'
        if asc >= -14149 and asc <= -14091:
            return 'R'
        if asc >= -14090 and asc <= -13119:
            return 'S'
        if asc >= -13118 and asc <= -12839:
            return 'T'
        if asc >= -12838 and asc <= -12557:
            return 'W'
        if asc >= -12556 and asc <= -11848:
            return 'X'
        if asc >= -11847 and asc <= -11056:
            return 'Y'
        if asc >= -11055 and asc <= -10247:
            return 'Z'
        return ''


# 中文获取首字母(所有文字)
def getFirstLetter(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        charLst.append(single_get_first(l))
    return ''.join(charLst)


if __name__ == "__main__":
    code = "000625"
    stock = current_day_stock(code)

    print(stock.code)
    print(stock.name)
    print(stock.price)
    print(stock.percent)
