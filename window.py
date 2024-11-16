import pyautogui
import pygetwindow as gw
import time
import cv2
import os
import numpy as np

def find_window(window_title):
    result = []
    window_list = gw.getWindowsWithTitle(window_title)
    window_count = len(window_list)
    if window_count == 0:
        return False
    for temp_window in window_list:
        if temp_window.title != window_title or temp_window.left < 0:
            # 不是NIKKE窗口或窗口最小化跳过
            continue
        else:
            result.append(temp_window)

    if len(result) == 0:
        print("游戏窗口最小化")
        return False
    else:
        # print(result[0])
        return result[0]

def capture_window(window):
        window.activate()
        # time.sleep(0.1)
        # 获取窗口在屏幕上的位置和大小
        x, y, width, height = window.left, window.top, window.width, window.height
        # 使用 pyautogui 截图
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        # # 保存截图
        # screenshot.save('screen.png')
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot

def save_screenshot(window):
    window.activate()
    # time.sleep(0.1)
    # 获取窗口在屏幕上的位置和大小
    x, y, width, height = window.left, window.top, window.width, window.height
    # 使用 pyautogui 截图
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # 保存截图
    screenshot.save('screen'+ str(i) +'.png')
# capture_window("NIKKE")

# i = 0
# while True:
#     capture_window("NIKKE", str(i))
#     time.sleep(0.5)
#     i += 1


def compare_panduan(screenshot,template,threshold):
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # print(template.shape)
    # x = template.shape[0] + max_loc[0]
    # y = template.shape[1] + max_loc[1]
    # loc_1 = (x, y)
    # print(max_val)
    # print(max_loc)
    # cv2.rectangle(result_pic, max_loc, loc_1,(0, 255, 0),1,4)
    # cv2.imshow("image",result_pic)
    # cv2.waitKey(0)

    if max_val > threshold:
        return max_loc[0], max_loc[1]
    else:
        return False


def compare_direction(cp_region,direction_dict):
    result_ar = []
    direction_ar = []
    for key, value in direction_dict.items():
        for img_temp in value:
            result = cv2.matchTemplate(cp_region, img_temp, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # print(max_val)
            direction_ar.append(key)
            result_ar.append(max_val)

    # print(direction_ar[result_ar.index(max(result_ar))])
    # print(max(result_ar))

    if max(result_ar) > 0.5:
        direction_result = direction_ar[result_ar.index(max(result_ar))]
        pyautogui.press(direction_result)
        print("==========================")
        print("press " + direction_result)


        # direction_piclist.append(img)


    # cv2.imshow("image", cp_region)
    # cv2.waitKey(0)

def init(window):
    while True:
        screenshot = capture_window(window)
        if not compare_panduan(screenshot, panduan, 0.7):
            print ("未找到判断区域")
        else:
            x, y = compare_panduan(screenshot, panduan, 0.7)
            print(x)
            print(y)
            return x, y



window = find_window("NIKKE")
window.activate()
time.sleep(0.1)
panduan = cv2.imread('pic/panduan.png')
direction_dict = {"left":[], "right":[], "up":[], "down":[]}
for filename in os.listdir("pic/direction"):
    # print(filename)
    direction = filename.split(".")[0].split('_')[0]
    img_temp = cv2.imread("pic/direction" + '/' + filename)
    if direction == "left":
        direction_dict["left"].append(img_temp)
    elif direction == "right":
        direction_dict["right"].append(img_temp)
    elif direction == "up":
        direction_dict["up"].append(img_temp)
    elif direction == "down":
        direction_dict["down"].append(img_temp)
    else:
        print("存在不是方向的截图模板")
        break

# test = cv2.imread('screen18.png')

# i = 1
# while True:
#     # t = time.time()
#     save_screenshot(window)
#     i=i+1
#     # print(time.time() - t)

x, y = init(window)
panduan_region_x = x - 10
panduan_region_y = y
x2 = panduan.shape[1] + panduan_region_x
y2 = panduan.shape[0] + panduan_region_y


while True:
    screenshot = capture_window(window)
    # cv2.imshow("1", screenshot)
    # cv2.waitKey(0)
    cp_region = screenshot[panduan_region_y:y2, panduan_region_x:x2]
    # cv2.imshow("1", cp_region)
    # cv2.waitKey(0)
    # cp_region = test[panduan_region_y:y2, panduan_region_x:x2]
    compare_direction(cp_region, direction_dict)



