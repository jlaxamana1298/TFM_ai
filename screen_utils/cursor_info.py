import pyautogui
import keyboard
import time


def main():
    while keyboard.is_pressed('q') == False:
        pyautogui.displayMousePosition()
        time.sleep(1)


if __name__ == '__main__':
    main()