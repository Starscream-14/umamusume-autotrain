import time
import random
import cv2
import numpy as np
import pyautogui

pyautogui.FAILSAFE = True

def search_and_click(image_path, confidence_threshold=0.6):

    try:
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        template = cv2.imread(image_path)
        if template is None:
            print(f"[Error] Image file '{image_path}' not found in the folder!")
            return False

        h, w, _ = template.shape

        result = cv2.matchTemplate(
            screenshot_cv, template, cv2.TM_CCOEFF_NORMED
        )
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(f"[Debug] Searching button... Highest similarity score: {max_val:.2f}")

        if max_val >= confidence_threshold:
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2

            time.sleep(random.uniform(0.3, 0.7))
            pyautogui.moveTo(
                center_x, 
                center_y, 
                duration=random.uniform(0.25, 0.55), 
                tween=pyautogui.easeInOutQuad
            )
            time.sleep(random.uniform(0.15, 0.35))
            pyautogui.click()
            
            print(
                f"[Success] Clicked '{image_path}' at coordinates ({center_x}, {center_y}) "
                f"[Accuracy: {max_val * 100:.1f}%]"
            )
            time.sleep(random.uniform(0.8, 1.5))
            return True
        else:
            return False

    except Exception as e:
        print(f"[Detector Error]: {e}")
        return False


def click_use_button_relative_to_item(item_image_path, x_distance_to_use=-60, confidence_threshold=0.4):

    try:
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        template = cv2.imread(item_image_path)
        if template is None:
            print(f"[Error] Image file '{item_image_path}' not found in the folder!")
            return False

        h, w, _ = template.shape

        result = cv2.matchTemplate(
            screenshot_cv, template, cv2.TM_CCOEFF_NORMED
        )
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(f"[Debug] Finding item box '{item_image_path}'... Highest similarity score: {max_val:.2f}")

        if max_val >= confidence_threshold:
            item_center_y = max_loc[1] + h // 2
            use_button_x = max_loc[0] + w + x_distance_to_use
            use_button_y = item_center_y

            time.sleep(random.uniform(0.3, 0.7))
            pyautogui.moveTo(
                use_button_x, 
                use_button_y, 
                duration=random.uniform(0.25, 0.55), 
                tween=pyautogui.easeInOutQuad
            )
            time.sleep(random.uniform(0.15, 0.35))
            pyautogui.click()
            
            print(
                f"[Success] Item found! Dynamically clicked 'Use' button at ({use_button_x}, {use_button_y}) "
                f"[Item Match Accuracy: {max_val * 100:.1f}%]"
            )
            time.sleep(random.uniform(0.8, 1.5))
            return True
        else:
            return False

    except Exception as e:
        print(f"[Relative Clicker Error]: {e}")
        return False