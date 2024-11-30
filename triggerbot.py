import pyautogui
import cv2
import numpy as np

# Диапазон сильных красных оттенков
lower_red1 = np.array([0, 150, 150])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 150, 150])
upper_red2 = np.array([180, 255, 255])

CENTER_BOX_SIZE = 5

def red_filter_with_edges(frame):
    """Фильтр, который выделяет только сильные красные оттенки и добавляет контуры."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    red_filtered = cv2.bitwise_and(frame, frame, mask=red_mask)
    gray = cv2.cvtColor(red_filtered, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    return edges, red_filtered

def is_red_in_center(mask):
    return np.any(mask > 0)

def main():
    screen_width, screen_height = pyautogui.size()

    # Вычисляем координаты центра экрана
    center_x, center_y = screen_width // 2, screen_height // 2
    half_box = CENTER_BOX_SIZE // 2

    # Захватываем только центральную область экрана
    region = (
        center_x - half_box,
        center_y - half_box,
        CENTER_BOX_SIZE,
        CENTER_BOX_SIZE,
    )
    while True:
        # Получаем размеры экрана

        screenshot = pyautogui.screenshot(region=region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        edges, red_filtered = red_filter_with_edges(frame)
        if is_red_in_center(edges):
            pyautogui.click()  


if __name__ == "__main__":
    main()
