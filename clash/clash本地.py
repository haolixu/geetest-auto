# -*- coding: utf-8 -*-
import cv2
import pyautogui
import numpy as np
import os, time
import yagmail

# 邮件配置（建议后续改用环境变量）
SENDER_EMAIL = "xx@qq.com"
SENDER_PASSWORD = "xxxxx"  # QQ邮箱授权码
RECEIVER_EMAIL = "xx@qq.com"

def send_success_email():
    try:
        yag = yagmail.SMTP(user=SENDER_EMAIL, password=SENDER_PASSWORD, host='smtp.qq.com')
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yag.send(
            to=RECEIVER_EMAIL,
            subject='[Clash] 按钮已点击',
            contents=f'成功滑动！\n时间：{current_time}'
        )
        print("✅ 邮件已发送")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")

def find_button_on_screen(template_path, confidence=0.8):
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


# ===== 使用示例 =====
while True:
    found, x, y = find_button_on_screen("join.png", confidence=0.80)
    if found:
        print("🎉 桌面屏幕上存在 Join 按钮！")
        print(x,y)
        send_success_email()
        stop_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"发送时间：{stop_time} ...")
        break
    else:
        print("❌ 桌面屏幕上未发现 Join 按钮")
    # 等待 60 秒（即 1 分钟）后再次执行
    time.sleep(3)
