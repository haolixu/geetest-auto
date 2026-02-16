import cv2
def detect_gap(bg_path, slider_path):
    """使用OpenCV识别缺口位置"""
    # 读取图片
    bg = cv2.imread(bg_path)  # 背景图
    tp = cv2.imread(slider_path)  # 缺口图
    # 灰度化处理
    bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    tp_gray = cv2.cvtColor(tp, cv2.COLOR_BGR2GRAY)
    # 边缘检测
    bg_edge = cv2.Canny(bg_gray, 100, 200)
    tp_edge = cv2.Canny(tp_gray, 100, 200)
    # 模板匹配
    res = cv2.matchTemplate(bg_edge, tp_edge, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc[0]  # 返回缺口x坐标
# 使用示例

