# -*- coding: utf-8 -*-
# @Time : 2026/2/16 02:05
# @Author : MyPC
# @File : 4.py
import re

import requests
from DrissionPage import ChromiumPage

def yanzm():
    # 启动浏览器
    page = ChromiumPage()
    # 直接运行js代码获取滑块图片
    slice_url = page.run_js("""
    return document.querySelector('.geetest_slice_bg').style.backgroundImage;
    """)
    # 获取背景图片
    bg_url = page.run_js("""
    return document.querySelector('.geetest_bg').style.backgroundImage;
    """)
    # 提取真实URL
    bg_url = re.findall(r'"(.*?)"', bg_url)[0]
    slice_url = re.findall(r'"(.*?)"', slice_url)[0]
    print(slice_url)
    print(bg_url)
    # 下载图片
    bg_img = requests.get(bg_url).content
    slice_img = requests.get(slice_url).content
    # 保存
    with open("bg.png", "wb") as f:
        f.write(bg_img)
    with open("slice.png", "wb") as f:
        f.write(slice_img)
    print("保存完成")
