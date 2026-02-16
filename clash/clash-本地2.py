# -*- coding: utf-8 -*-
import os
import time
import cv2
import numpy as np
import pyautogui
from juli import detect_gap
from quekou import yanzm
from clash本地 import send_success_email
def find_button_on_screen2(template_path, confidence=0.8):
    if not os.path.exists(template_path):
        print(f"❌ 模板文件不存在: {template_path}")
        return False, None, None
    # 1. 截取全屏（返回 PIL Image）
    screenshot = pyautogui.screenshot()
    # 转为 OpenCV 格式 (BGR)
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # 2. 读取模板
    template = cv2.imread(template_path)
    if template is None:
        print("❌ 无法加载模板图像")
        return False, None, None
    # 3. 模板匹配
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        print(f"✅ 找到按钮！位置: ({center_x}, {center_y})，匹配度: {max_val:.2f}")
        return True, center_x, center_y
    else:
        print(f"⚠️ 未找到按钮（最高匹配度: {max_val:.2f} < {confidence}）")
        return False, None, None

if __name__ == "__main__":
    while True:
        try:
            time.sleep(3)
            found2, x2, y2 = find_button_on_screen2("join.png", confidence=0.8)
            if found2:
                pyautogui.click(x2, y2)
            else:
                print("识别失败")

            time.sleep(10)
            yanzm()
            gap_pos = detect_gap("bg.png", "slice.png")
            print(f"需要滑动的距离：{gap_pos}px")
            template_path = "huadong.png"
            found, x, y = find_button_on_screen2(template_path, confidence=0.8)
            if found:
                print(f"滑动按钮坐标：({x}, {y})")
                pyautogui.moveTo(x, y, duration=0.1)
                pyautogui.mouseDown()
                pyautogui.moveRel(gap_pos, 0, duration=0.5)  # 向右移动100像素
                pyautogui.mouseUp()
                send_success_email()
            else:
                print("识别失败")
        except Exception as e:
            print(f"任务出错: {e}")

        print("等待 30 分钟...")
        time.sleep(30 * 60)  # 30 分钟 = 1800 秒
