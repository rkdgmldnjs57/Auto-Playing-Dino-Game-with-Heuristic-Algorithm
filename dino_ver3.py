import pyautogui as gui
import cv2
import numpy as np
import time
import mss

sct = mss.mss()
gui.PAUSE = 0
scr_range = (2, 400, 958, 465)
px_thr = 9300  #전체 9750
px_jump = 2500  #전체 3900

time_diff = 0
detecting1 = 0
detecting2 = 0
dtime = 0.0
d2time = 0.0
jump_timing = 0
jumping = 0
jump_cnt = 0
velocity = 0

while cv2.waitKey(1) != 27 : 
   
   screen = sct.grab(scr_range)
   screen = np.array(screen)  #(, , )

   screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
   _, screen_bin = cv2.threshold(screen_gray, 150, 255, cv2.THRESH_BINARY)
   
   ROI_1 = screen_bin[:, 750:900]
   ROI_2 = screen_bin[:, 500:650]
   ROI_3 = screen_bin[:, 40:100]
   px_sum1 = np.sum(ROI_1) / 255
   px_sum2 = np.sum(ROI_2) / 255
   px_sum3 = np.sum(ROI_3) / 255
   if px_sum1 < 4875 : 
      px_sum1 = 9750 - px_sum1
      px_sum2 = 9750 - px_sum2
      px_sum3 = 3900 - px_sum3
      

   if px_sum1 < px_thr and not detecting1 :
      detecting1 = 1

   elif px_sum1 >= px_thr and detecting1 :
      dtime = time.time()
      detecting1 = 0

   if px_sum2 < px_thr and not detecting2 : 
      detecting2 = 1

   elif px_sum2 >= px_thr and detecting2:
      detecting2 = 0
      d2time = time.time()
      time_diff = d2time - dtime
      velocity = 1 / time_diff

   if px_sum3 > px_jump :
      jumping = 1
   else :
      jumping = 0
   
   if 2 * time_diff - 0.5275 < time.time() - d2time and time_diff != 0 :
      if jumping :
         print('wait..') 
         continue
      else :
         gui.press('up')
         jump_cnt += 1 
         print("%dth Jump!"%jump_cnt, round(time_diff, 3), round(velocity, 3))
         time_diff = 0
   
   if time.time() - d2time > 7 and d2time != 0 :
      tm = time.localtime(time.time())
      gui.screenshot('./screenshot/21%2d%2d%2d.png'%(tm.tm_hour, tm.tm_min, tm.tm_sec))
      gui.press('space')
      print('Saved')
      d2time = 0
      
cv2.destroyAllWindows()