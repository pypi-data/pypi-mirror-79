"""
    @Author hlj

    @Date 2020/9/10 19:14

    @Describe  

"""
# coding: cp936
import datetime

import win32gui
import win32con
import time
from pyttsx3 import speak


class TestTaskbarIcon:
    def __init__(self):
        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"
        wc.hbrBackground = win32con.COLOR_BTNFACE + 1  # 这里颜色用法有点特殊，必须+1才能得到正确的颜色
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy}
        classAtom = win32gui.RegisterClass(wc)
        #        WS_OVERLAPPED：产生一个层叠的窗口，一个层叠的窗口有一个标题栏和一个边 框。
        #
        #        WS_CAPTION： 创建一个有标题栏的窗口。
        #
        #        WS_SYSMENU：创建一个在标题栏上带有系统菜单的窗口，要和WS_CAPTION类 型一起使用。
        #
        #        WS_THICKFRAME： 创建一个具有可调边框的窗口。
        #
        #        WS_MINIMIZEBOX：创建一个具有最小化按钮的窗口，必须同时设定WS_ SYSMENU类型。
        #
        #        WS_MAXIMIZEBOX：创建一个具有最大化按钮的窗口，必须同时设定WS_ SYSMENU类型。
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU | win32con.WS_CAPTION | win32con.WS_THICKFRAME  | win32con.WS_MAXIMIZEBOX
        self.hwnd = win32gui.CreateWindow(classAtom, "hlj", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        self.startRunTime = datetime.datetime.now()

    # 展示窗口消息
    def showMsg(self, title, msg):
        nid = (self.hwnd,  # 句柄
               0,  # 托盘图标ID
               win32gui.NIF_INFO,  # 标识
               0,  # 回调消息ID
               0,  # 托盘图标句柄
               "test",  # 图标字符串
               msg,  # 气球提示字符串
               0,  # 提示的显示时间
               title,  # 提示标题
               win32gui.NIIF_INFO  # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    # 提示语音
    def speak(self, flag, title, msg):
        if flag == 0:
            # startRunTime = time.time()
            # 后面带微秒
            # starttime = datetime.datetime.now()
            # # Thu Apr  7 10:05:21 2016
            # starttime = time.asctime(time.localtime(time.time()))
            # 格式化成2016-03-20 11:45:39形式
            starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('\33[33m'+title+',开始时间为' + str(starttime) + msg + '\33[0m')
            speak(title+'开始时间为' + str(starttime) + msg)
        elif flag == 1:
            endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('\33[33m'+title+',结束时间为' + str(endtime) + msg + '\33[0m')
            speak(title+',结束时间为' + str(endtime) + msg)
            endRunTime = datetime.datetime.now()
            totalTime = endRunTime - self.startRunTime
            days = totalTime.days
            seconds = totalTime.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            print('\33[34m程序运行总时间' + str(endRunTime - self.startRunTime) + '\33[0m')
            speak('程序运行总时间' + str(days) + '天' + str(hours) + '小时' + str(minutes) + '分钟' + str(seconds) + '秒')

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        # Terminate the app.
        win32gui.PostQuitMessage(0)

    # 关闭窗口
    def destroy(self):
        win32gui.DestroyWindow(self.hwnd)


if __name__ == '__main__':
    t = TestTaskbarIcon()
    t.showMsg("Sir.lenjou您有新的文件下载", "下载开始")
    t.speak(0, "Sir.lenjou您有新的文件下载", "下载开始")
    time.sleep(1)
    t.showMsg("Sir.lenjou您有新的文件下载", "下载结束")
    t.speak(1, "Sir.lenjou您有新的文件下载", "下载结束，请查看")
    t.destroy()


