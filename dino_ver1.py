import pyautogui as gui
import cv2
from PIL import ImageGrab
import numpy as np

#gui.press('up')
#gui.press('down')

scr_range = (2, 350, 958, 465)
px_thr = 17000
block_state = 0

while cv2.waitKey(10) != 27 : 
   screen = ImageGrab.grab(scr_range)
   screen = np.array(screen)  #(, , )

   screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
   _, screen_bin = cv2.threshold(screen_gray, 150, 255, cv2.THRESH_BINARY)
   ROI_1 = screen_bin[:, 800:950]
   ROI_2 = screen_bin[:, 200:350]
      #cv2.rectangle(screen, (2, 350), (958, 465), (255, 0, 0), 2)
   px_sum1 = np.sum(ROI_1) / 255
   px_sum2 = np.sum(ROI_2) / 255
   cv2.imshow('window', ROI_1)
   cv2.imshow('window2', ROI_2)
   print(px_sum1, px_sum2)

   if px_sum2 < px_thr and not block_state :
      block_state = 1
   else : 
      block_state = 0

   if block_state == 1 :
      gui.press('up')


cv2.waitKey(0)
cv2.destroyAllWindows()

