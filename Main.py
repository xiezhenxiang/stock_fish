import configparser  # 加载config.ini
import os
import sys
import threading
import time
import tkinter as tk  # 图形界面

import keyboard
import psutil as psutil

from Crawler import current_day_stock


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
            row = 0
            for code in codes:
                stock = current_day_stock(code)
                arr = code_map.get(code)
                arr[0].set(stock.name)
                arr[1].set(stock.price)
                arr[2].set(stock.percent)
                row += 1

        if current_time > '1510':
            window_off(None)
        time.sleep(refresh_interval)


# 右键重新加载，重新运行本程序，重新加载config.ini
def reload(event):
    os.execvp(sys.executable, [sys.executable] + sys.argv)


def window_off(event):
    parent = psutil.Process(os.getpid())
    kill_process_and_its_children(parent)
    sys.exit(0)


def kill_process_and_its_children(p):
    p = psutil.Process(p.pid)   # p might be Python's process, convert to psutil's process
    if len(p.children())>0:
        print('有子进程')
        for child in p.children():
            if hasattr(child,'children') and len(child.children())>0:
                kill_process_and_its_children(child)
            else:
                kill_process(child)
    else:
        print('无子进程')
    kill_process(p)


def kill_process(p):
    try:
        print('正在发送terminate命令到进程:', os.getpid(), '-->', p.pid)
        p.terminate()
        _, alive = psutil.wait_procs([p,], timeout=0.1)    # 先等 100ms
        if len(alive):
            _, alive = psutil.wait_procs(alive, timeout=3.0)  # 再等 3s
            if len(alive):
                print('\t (R1) 很遗憾, 进程不服从terminate信号, 正在发送kill-9命令到进程:', os.getpid(), '-->', p.pid)
                for p in alive: p.kill()
            else:
                print('\t (R2) 进程成功结束')
        else:
            print('\t (R2) 进程成功结束')
    except Exception as e:
        print(e)


def command(event):
    # 使用 post()在指定的位置显示弹出菜单
    menu.post(event.x_root, event.y_root)


def window_hide(event):
    window.withdraw()


def window_show(event):
    window.deiconify()


def move_window(event):
    window.geometry('+{0}+{1}'.format(window.winfo_pointerx(), window.winfo_pointery()))


def add_label(str_val, row, column):
    tk.Label(window, textvariable=str_val, font=("新罗马", 9), fg="#aaaaff", bg=window['bg']).grid(row=row, column=column, sticky="w")


def init_window():
    # 置顶窗口
    window.wm_attributes('-topmost', True)
    # 窗口背景色
    # window.config(background ="#aaaaef")
    # 窗口透明度
    transparence = conf.get('window', 'transparence')
    window.attributes("-alpha", transparence)
    # 使背景色透明
    window.wm_attributes('-transparentcolor', window['bg'])
    # 窗口宽度固定，高度固定
    # 长度和高度都不允许调整，同时最大化按钮会被禁用
    window.resizable(False, False)
    # 隐藏标题栏
    window.overrideredirect(True)
    # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕右下角
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (1000, 1000, (screenwidth - 155), (screenheight - 130))
    # 设置窗口大小和位置
    window.geometry(size_geo)
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


def str_var(value):
    return tk.StringVar(value=value)


if __name__ == "__main__":
    # 读取配置文件
    conf = configparser.ConfigParser()
    conf.read("config.ini", "utf-8-sig")
    # 数据刷新间隔,单位:秒
    refresh_interval = int(conf.get('window', 'refresh_interval'))
    codes = conf.get('monitor', 'stock_codes').split(",")
    window = tk.Tk()
    init_window()
    # 创建右键菜单
    menu = tk.Menu(window, tearoff=False)
    menu.add_command(label="重载", command=reload)
    menu.add_command(label="退出", command=window_off)

    code_map = {}
    row = 0
    for code in codes:
        stock = current_day_stock(code)
        arr = [str_var(stock.name), str_var(stock.price), str_var(stock.percent)]
        add_label(arr[0], row, 0)
        add_label(arr[1], row, 1)
        add_label(arr[2], row, 2)
        code_map.setdefault(code, arr)
        row += 1

    thread = threading.Thread(target=refresh)
    thread.start()

    window.mainloop()
