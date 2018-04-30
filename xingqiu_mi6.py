# -*- coding: utf-8 -*-

import os
import time, datetime

import numpy as np
from PIL import Image

# 0 –> “KEYCODE_UNKNOWN” 
# 1 –> “KEYCODE_MENU” 
# 2 –> “KEYCODE_SOFT_RIGHT” 
# 3 –> “KEYCODE_HOME” 
# 4 –> “KEYCODE_BACK” 
# 5 –> “KEYCODE_CALL” 
# 6 –> “KEYCODE_ENDCALL” 
# KEYCODE_PAGE_UP	向上翻页键	92
# KEYCODE_PAGE_DOWN	向下翻页键	93
# KEYCODE_MOVE_HOME	光标移动到开始键	122
# KEYCODE_MOVE_END	光标移动到末尾键	123

# MI 6, 屏幕 1080*1920
MOBILE_SCREENSHOT_PATH = '/sdcard/Download/xingqiu_temp'
PC_SCREENSHOT_PATH = 'E:\\test_image'


def click_news():
    # 点击资讯
    os.system('adb shell input tap 550 1390')
    time.sleep(1)
    print('点击资讯完成')
    # 点击昨天原力结果确认
    os.system('adb shell input tap 584 1290')
    time.sleep(3)
    print('点击昨天原力确认结果完成')
    n = 0
    for i in range(3):
        if n != 0:
            # 下拉松开刷新新闻
            os.system('adb shell input swipe 484 482 484 900')
            time.sleep(5)
            print('下拉松开刷新新闻完成')
        # 点击第一条新闻
        os.system('adb shell input tap 484 482')
        time.sleep(5)
        print('点击第一条新闻完成')
        s = time.time()
        # 翻到底部
        os.system('adb shell input keyevent 123')
        # 向上翻一页
        os.system('adb shell input keyevent 92')
        # 点击查看全文
        os.system('adb shell input tap 550 414')
        time.sleep(1)
        print('点击查看全文完成')
        # 翻到顶部
        os.system('adb shell input keyevent 122')
        # 逐步向下滑动停留64秒
        c = 0
        while c < 16:
            os.system('adb shell input keyevent 20')
            time.sleep(4)
            c += 1
            print('缓慢滑动阅读正文%d' % c )
        print('阅读时间完成')
        # 翻到底部
        os.system('adb shell input keyevent 123')
        # 向上翻一页
        os.system('adb shell input keyevent 92')
        # 点击广告
        os.system('adb shell input tap 505 910')
        time.sleep(2)
        print('点击广告完成')
        # 从广告页返回到新闻页
        os.system('adb shell input keyevent 4')
        # time.sleep(3)
        # 从新闻页返回到新闻列表
        os.system('adb shell input keyevent 4')
        n += 1
        e = time.time()
        print('新闻+广告点击完成%d, %0.2f' % (n, e-s))


def screenshot():
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    # 截图地址 /sdcard/Download/xingqiu_temp
    # adb shell /system/bin/screencap -p /sdcard/Download/xingqiu_temp/1.jpg（保存到SDCard）
    # adb pull /sdcard/Download/xingqiu_temp/1.jpg E:\Android\1.jpg（保存到电脑）
    os.system('adb shell /system/bin/screencap -p %s/%s' % (MOBILE_SCREENSHOT_PATH, filename))
    os.system('adb pull /sdcard/Download/xingqiu_temp/%s %s\\%s' % (filename, PC_SCREENSHOT_PATH, filename))
    return filename


def check_diff_images(image1, image2, xy):
    x,y  = xy[0], xy[1]
    high, wight = 40, 35
    img1 = np.array(Image.open('%s\\%s' % (PC_SCREENSHOT_PATH, image1)))
    img2 = np.array(Image.open('%s\\%s' % (PC_SCREENSHOT_PATH, image2)))
    img = np.abs(img1-img2)
    status_img = img[y: y+high, x:x+wight]
    # im = Image.fromarray(status_img)
    # im.show()
    # np.any(status_img) == True # True是有变化，False 无变化
    # np.count_nonzero(status_img) == 0 # 0 是无变化, >0 有变化
    if np.count_nonzero(status_img) == 0:
        return False
    else:
        return True


def click_music():
    # 点击云音乐
    os.system('adb shell input tap 915 1390')
    time.sleep(1)
    print('点击云音乐完成')
    # 点击昨天原力结果确认
    os.system('adb shell input tap 562 1253')
    time.sleep(3)
    print('点击昨天原力确认结果完成')

    start_music_bx = 180
    n = 0
    # 第1首-第4歌
    xy_1_4_list = [(860, 1140+i*start_music_bx) for i in range(4)]
    for i, xy in enumerate(xy_1_4_list):
        # 点击第1首歌
        os.system('adb shell input tap %d %d' % xy)
        time.sleep(1)
        img1 = screenshot()
        time.sleep(60*3)
        img2 = screenshot()
        while 1:
            if check_diff_images(img1, img2, xy):
                print('音乐播放完毕')
                break
            else:
                print('继续播放20秒')
                time.sleep(20)
                img2 = screenshot()
        n += 1
        print('第%d首播放完成' % n)

    # 滑到底部
    os.system('adb shell input swipe 600 1700 600 460')
    # 第5首-第10歌
    xy_5_10_list = [(860, 765+i*start_music_bx) for i in range(6)]
    for i, xy in enumerate(xy_5_10_list):
        os.system('adb shell input tap %d %d' % xy)
        time.sleep(1)
        img1 = screenshot()
        time.sleep(60*3)
        img2 = screenshot()
        while 1:
            if check_diff_images(img1, img2, xy):
                print('音乐播放完毕')
                break
            else:
                print('继续播放20秒')
                time.sleep(20)
                img2 = screenshot()
        n += 1
        print('第%d首播放完成' % n)


def start_app():
    # 点击星球app
    os.system('adb shell input tap 189 1380') # 桌面的app位置
    os.system('adb shell input tap 566 1124') # 桌面的app位置
    # 需要root 直接通过包名启动
    # os.system('adb shell am start -D -n com.netease.blockchain/com.netease.blockchain.business.splash.SplashActivity')
    time.sleep(5)
    print('启动app完成')


def click_task():
    # 点击获取原力
    os.system('adb shell input tap 138 1252')
    time.sleep(3)
    # print('点击获取原力完成')


def del_screenshot_file():
    # 删除截图
    os.system('adb shell rm -rf %s/*' % MOBILE_SCREENSHOT_PATH)
    os.system('del %s\\*.jpg' % PC_SCREENSHOT_PATH)
    print('删除截图完成')


def main():
    start_app()  # 启动app
    click_task() # 点击获取原力
    click_news() # 点击资讯,并浏览3条, 停留60s以上, 点击广告

    # 从新闻页返回到星球任务页
    os.system('adb shell input keyevent 4')

    click_music() # 点击云音乐并播放
    # star_music()  # 点赞音乐
    time.sleep(1)
    del_screenshot_file() # 删除临时截图


main()





























# from appium import webdriver

# desired_caps = {}
# desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = '8.0.0'
# desired_caps['deviceName'] = 'MI 6'
# desired_caps['appPackage'] = 'com.netease.blockchain'
# desired_caps['appActivity'] = '.business.splash.SplashActivity'

# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
