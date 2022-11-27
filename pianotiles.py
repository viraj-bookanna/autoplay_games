import pyautogui, time, keyboard, win32api, win32con

time.sleep(2)

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while not keyboard.is_pressed('q'):
    if pyautogui.pixel(400, 500) == (0, 0, 0):
        click(400, 500)
    if pyautogui.pixel(500, 500) == (0, 0, 0):
        click(500, 500)
    if pyautogui.pixel(600, 500) == (0, 0, 0):
        click(600, 500)
    if pyautogui.pixel(700, 500) == (0, 0, 0):
        click(700, 500)
