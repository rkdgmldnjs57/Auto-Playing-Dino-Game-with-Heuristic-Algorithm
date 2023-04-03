import pyautogui as gui    #키보드 조작 라이브러리
import cv2                 #영상처리 라이브러리
import numpy as np         #행렬 라이브러리
import time                #시간
import mss                 #캡처 라이브러리

sct = mss.mss()
gui.PAUSE = 0
scr_range = (2, 400, 958, 465)
px_thr = 9300  #전체 9750
px_jump = 3330  #전체 3227

time_diff = 0
detecting1 = 0
detecting2 = 0
dtime = 0.0
d2time = 0.0
jump_timing = 0
jumping = 0
jump_cnt = 0
velocity = 0


while cv2.waitKey(1) != 27 :                    #시작! 무한루프
   
   screen = sct.grab(scr_range)                 #해당 영역 캡처
   screen = np.array(screen)  #(, , )           #numpy 배열로 변환

   screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)                  #opencv 사용하게 변환
   _, screen_bin = cv2.threshold(screen_gray, 150, 255, cv2.THRESH_BINARY) #임계값 기준으로 흑백(0, 1)로 변환
   
   ROI_1 = screen_bin[:, 750:900]               #첫번째 장애물 체크 지점
   ROI_2 = screen_bin[:, 500:650]               #두번째 장애물 체크 지점
   ROI_3 = screen_bin[:, 25:100]                #공룡 점프 여부 체크 지점
   px_sum1 = np.sum(ROI_1) / 255
   px_sum2 = np.sum(ROI_2) / 255
   px_sum3 = np.sum(ROI_3) / 255
   if px_sum1 < 4875 :                          #밤이면 픽셀 반전
      px_sum1 = 9750 - px_sum1
      px_sum2 = 9750 - px_sum2
      px_sum3 = 3900 - px_sum3
      

   if px_sum1 < px_thr and not detecting1 :     #임계값 이하면 detecting1 상태 1로 바꿈
      detecting1 = 1

   elif px_sum1 >= px_thr and detecting1 :      #detecting1 상태 1이고 착지상태면 시간 기록하고 상태 0으로 바꿈
      dtime = time.time()
      detecting1 = 0

   if px_sum2 < px_thr and not detecting2 :     #임계값 이하면 detecting2 상태 1로 바꿈
      detecting2 = 1

   elif px_sum2 >= px_thr and detecting2 :      #detecting2 상태 1이고 착지상태면 시간 기록하고 상태 0으로 바꿈, 시간 차이 계산하여 속도 도출
      detecting2 = 0
      d2time = time.time()
      time_diff = d2time - dtime
      velocity = 1 / time_diff

   if px_sum3 > px_jump :                       #공룡 점프 중인지 확인
      jumping = 1
   else :
      jumping = 0
   
   if 2 * time_diff - 0.5275 < time.time() - d2time and time_diff != 0 :      #2번째 지점을 지나고서 지난 시간이 일정 시간(2t-0.5275) 보다 작으면 점프
      if jumping :                                                            #현재 점프 상태이면 대기
         print('wait..') 
         continue
      else :
         gui.press('up')
         jump_cnt += 1 
         print("%dth Jump!"%jump_cnt, round(time_diff, 3), round(velocity, 3))

         time_diff = 0

   if time.time() - d2time > 7 and d2time != 0 :                              #움직임이 없을 때 화면 캡처하여 저장 후 다시 시작
      tm = time.localtime(time.time())
      gui.screenshot('./screenshot/21%2d%2d%2d.png'%(tm.tm_hour, tm.tm_min, tm.tm_sec))   
      gui.press('space')
      print('Saved')
      d2time = 0
   
cv2.destroyAllWindows()