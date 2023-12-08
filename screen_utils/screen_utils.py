from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api
import win32con
import os
import win32gui


class ScreenUtils:
    def __init__(self):
        pass

    def click(self, x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.5)
        return

    def scroll(self, x, y, scroll_amt):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, scroll_amt, 0)
        return

    def get_tfm_window_pos(self):
        window = win32gui.FindWindow(None, 'Teamfight Manager')
        win_x, win_y, win_r, win_b = win32gui.GetWindowRect(window)
        pos = [win_x, win_y, win_r, win_b]
        
        return pos

    # Click New Test button
    def click_new_test(self):
        new_img = os.path.join(os.path.dirname(__file__), 
                            'gui_pics', 'new_test.png')
        win_pos = self.get_tfm_window_pos()
        win_region = (win_pos[0], win_pos[1],
                        win_pos[2], win_pos[3])
        new_location = pyautogui.locateOnScreen(new_img, region = win_region,
                                    confidence = 0.7)
        
        if new_location != None:
            new_test_x, new_test_y = pyautogui.center(new_location)
            self.click(new_test_x, new_test_y)
            return
        else:
            return False

    # Locate close test button
    def locate_close(self):
        close_img = os.path.join(os.path.dirname(__file__), 
                            'gui_pics', 'close.png')
        win_pos = self.get_tfm_window_pos()
        win_region = (win_pos[0], win_pos[1],
                        win_pos[2], win_pos[3])
        close_location = pyautogui.locateOnScreen(close_img,
                                                region = win_region,
                                                confidence = 0.7)
        if close_location != None:
            return close_location
        else:
            return False
    
    def click_close(self):
        if self.locate_close():
            close_loc = self.locate_close()
            close_x, close_y = pyautogui.center(close_loc)
            self.click(close_x, close_y)
            return
        else:
            print('close not found')
            return False

    # Click Start Test button
    def click_start_test(self):
        start_img = os.path.join(os.path.dirname(__file__), 
                            'gui_pics', 'start_test.png')
        win_pos = self.get_tfm_window_pos()
        win_region = (win_pos[0], win_pos[1],
                        win_pos[2], win_pos[3])
        start_location = pyautogui.locateOnScreen(start_img, 
                                                region = win_region,
                                                confidence = 0.7)
        start_location = pyautogui.center(start_location)
        if start_location:
            start_x, start_y = start_location
            self.click(start_x, start_y)
        else:
            print('start not found')
            return False

    def get_char_icon_pos(self, character):
        # Character variables
        char_img_string = character + '.png'
        char_img = os.path.join(os.path.dirname(__file__), 
                            'character_pics', char_img_string)
    
        # Get tfm window position and region
        win_pos = self.get_tfm_window_pos()
        win_region = (win_pos[0], win_pos[1],
                        win_pos[2], win_pos[3])
        
        # Check if character is on screen
        char_location = pyautogui.locateOnScreen(char_img, region = win_region,
                                    confidence = 0.9)
        if char_location != None:
            #print(f'{character} is visible')
            return pyautogui.center(char_location)
        else:
            #print(f'{character} not visible')
            return False

    def find_char(self, char):
        if self.get_char_icon_pos(char) != False:
            char_pos_x, char_pos_y = self.get_char_icon_pos(char)
            return [char_pos_x, char_pos_y]
        else:
            return False

    def find_and_click_char(self, char):
        amt_scrolled = 0
        # Scroll down if character not found
        win_pos = self.get_tfm_window_pos()
        win_region = (win_pos[0], win_pos[1], win_pos[2], win_pos[3])
        center_window = pyautogui.center(win_region)
        center_x, center_y = center_window
        center_x = int(center_x * 0.7)
        center_y = int(center_y * 0.7)
        while self.find_char(char) == False:
            if keyboard.is_pressed('q'):
                break
            self.scroll(center_x, center_y, -500)
            amt_scrolled += 500
            time.sleep(0.3)
        
        char_pos = self.find_char(char)
        self.click(char_pos[0], char_pos[1])
        
        # Scroll back to top
        self.scroll(center_x, center_y, amt_scrolled)
        time.sleep(0.5)
        return

    def find_score(self):
        # Wait for close button to appear after simulation
        while self.locate_close() == False:
            if keyboard.is_pressed('q'):
                break
            time.sleep(0.5)
        time.sleep(0.5)

        # Screenshot scoreboard
        win_pos = self.get_tfm_window_pos()
        win_len = win_pos[2] - win_pos[0]
        win_height = win_pos[3] - win_pos[1]

        l_edge = int((0.423 * win_len) + win_pos[0])
        r_edge = int((0.574 * win_len) + win_pos[0])
        t_edge = int((0.435 * win_height) + win_pos[1])
        b_edge = int((0.538 * win_height) + win_pos[1])
        width = r_edge - l_edge
        height = b_edge - t_edge

        img = pyautogui.screenshot(region = (l_edge, t_edge, width, height))
        img.save('screenshot.png')

    def find_winner(self, image):
        # Color is (104, 255, 1)
        # Region is L*.423, L*.574
        #           H*.435, H*.538
        width, height = image.size
        left_half_width = width // 2

        for x in range(0, left_half_width, 1):
            for y in range(0, height, 1):
                r, g, b = image.getpixel((x, y))
                # If any pixel is green then winner is blue
                if r == 104 and g == 255 and b == 1:
                    print('winner is blue')
                    return 'Win'
        print('winner is red')
        return 'Loss'
