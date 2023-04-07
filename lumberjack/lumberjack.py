import pyautogui, time, keyboard, random

move_left = [160, 600]
move_right = [330, 600]
sample = "C:/Users/UnKNOWN/Documents/project/sample.png"

# barrier = pyautogui.screenshot(region=(284, 250, 100, 120))
# barrier.save("C:/Users/UnKNOWN/Documents/project/sample_xx.png")
# exit()
# s=pyautogui.locate(sample, "C:/Users/UnKNOWN/Documents/project/sample_xx.png", confidence=0.75, grayscale=False)
# print(s)
# exit()
time.sleep(2)

pyautogui.press(' ')
while not keyboard.is_pressed('q'):
    time.sleep(0.001)
    if pyautogui.locateOnScreen(sample, region=(115, 250, 100, 120), confidence=0.75, grayscale=False) != None:
        pyautogui.press('right', 2, random.choice([0.09, 0.10]))
        print('->')
        continue
    if pyautogui.locateOnScreen(sample, region=(284, 250, 100, 120), confidence=0.75, grayscale=False) != None:
        pyautogui.press('left', 2, random.choice([0.09, 0.10]))
        print('<-')
        continue
    pyautogui.press('right', 2, random.choice([0.09, 0.10]))
    print('--')