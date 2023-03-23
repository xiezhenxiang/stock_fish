import configparser  # 加载config.ini
import os
import sys
import threading  # 多线程模块
import time
import tkinter as tk  # 图形界面

import keyboard  # 全局热键

from Crawler import current_day_stock


# 右键重新加载，重新运行本程序，重新加载config.ini
def reload(event):
    os.execvp(sys.executable, [sys.executable] + sys.argv)


def window_off(event):
    window.destroy()
    exit()


def command(event):
    # 使用 post()在指定的位置显示弹出菜单
    menu.post(event.x_root, event.y_root)


def window_hide(event):
    window.withdraw()


def window_show(event):
    window.deiconify()


def move_window(event):
    window.geometry('+{0}+{1}'.format(window.winfo_pointerx(), window.winfo_pointery()))


def refresh():
    while True:
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        if str(hour).__len__() == 1:
            hour = '0' + str(hour)
        if str(minute).__len__() == 1:
            minute = '0' + str(minute)

        current_time = (str(hour) + str(minute))
        if '0930' <= current_time <= '1500':
            list_data3 = []
            list_data4 = []
            for e in codes:
                stock = current_day_stock(e)
                list_data3.append(str(stock.price))
                list_data4.append(str(stock.percent))
            for i, item in enumerate(list_data3):
                col_box3.delete(i)
                col_box3.insert(i, item)
            for i, item in enumerate(list_data4):
                col_box4.delete(i)
                col_box4.insert(i, item)
        if current_time > '1510':
            window_off(None)
        time.sleep(refresh_interval)


if __name__ == "__main__":

    # 创建窗口
    window = tk.Tk()
    # 读取配置文件
    conf = configparser.ConfigParser()
    conf.read("config.ini", "utf-8-sig")
    # 数据刷新间隔,单位:秒
    refresh_interval = int(conf.get('window', 'refresh_interval'))
    codes = conf.get('monitor', 'stock_codes').split(",")
    transparence = conf.get('window', 'transparence')

    window.title('try fish')
    # 窗口透明度
    window.attributes("-alpha", transparence)
    # 窗口背景色
    window.config(background ="black")
    # 置顶窗口
    window.wm_attributes('-topmost', True)
    width = 220
    height = 19 * len(codes)
    # 窗口宽度固定，高度固定
    # 长度和高度都不允许调整，同时最大化按钮会被禁用
    window.resizable(False, False)
    # 隐藏标题栏
    window.overrideredirect(True)
    # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕右下角
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width - 155), (screenheight - height - 33))
    # 设置窗口大小和位置
    window.geometry(size_geo)

    col_data1 = []
    col_data2 = []
    col_data3 = []
    col_data4 = []
    for code in codes:
        stock = current_day_stock(code)
        col_data1.append(stock.code)
        col_data2.append(stock.name)
        col_data3.append(str(stock.price))
        col_data4.append(str(stock.percent))

    # 创建文本控件
    col_box1 = tk.Listbox(window, width=int(55), height=height, relief="ridge", background="#aaaaff")

    col_box2 = tk.Listbox(window, width=int(55), height=height, relief="ridge", background="#aaaaff")
    col_box3 = tk.Listbox(window, width=int(55), height=height, relief="ridge", background="#aaaaff")
    col_box4 = tk.Listbox(window, width=int(55), height=height, relief="ridge", background="#aaaaff")
    col_box1.place(x=0)
    col_box2.place(x=55)
    col_box3.place(x=width * 0.5)
    col_box4.place(x=width * 0.75)

    for i, item in enumerate(col_data1):
        col_box1.insert(i, item)
    for i, item in enumerate(col_data2):
        col_box2.insert(i, item)
    for i, item in enumerate(col_data3):
        col_box3.insert(i, item)
    for i, item in enumerate(col_data4):
        col_box4.insert(i, item)

    t1 = threading.Thread(target=refresh)
    t1.start()

    # 创建右键菜单
    menu = tk.Menu(window, tearoff=False)
    menu.add_command(label="重载", command=reload)
    menu.add_command(label="退出", command=window_off)
    # 鼠标右键单击
    window.bind("<Button-3>", command)
    # 全局热键 Alt+1
    # window.bind("<Escape>",window_hide)
    keyboard.add_hotkey('alt+1', window_hide, args=('From global keystroke',))
    keyboard.add_hotkey('alt+2', window_show, args=('From global keystroke',))
    keyboard.add_hotkey('alt+5', reload, args=('From global keystroke',))
    keyboard.add_hotkey('alt+6', window_off, args=('From global keystroke',))

    # 把窗口禁用掉，不允许拖动、缩放
    window.attributes("-disabled", True)
    # 鼠标拖动窗体
    # window.bind("<B1-Motion>", move_window)
    window.mainloop()
