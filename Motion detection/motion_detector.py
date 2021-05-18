import cv2
import time
from firebase import firebase
from datetime import datetime
  

fb = firebase.FirebaseApplication("Enter Your Firebase Realtime-Database URL")

static_back = None
  
motion_list = [ None, None ]
  
video = cv2.VideoCapture('Enter your mobile cameras URL/video')

while True:
    ret, frame = video.read()
    
    motion = 0
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back = gray
        continue
  
    diff_frame = cv2.absdiff(static_back, gray)
  
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
  
    cnts,_ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
  
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1
  
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
  
    motion_list.append(motion)
  
    motion_list = motion_list[-2:]
  
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        a = datetime.now()
  
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        b = datetime.now()
        
        if (b - a).total_seconds() > 6:
            if (datetime.now().month == 11) or (datetime.now().month == 12) or datetime.now().month == 1 or datetime.now().month == 2:
                if not ((datetime.now().hour < 18 and (datetime.now().hour) >= 8)):
                    fb.put("HOME", 'LED_STATUS', 'ON')
            else:
                if (datetime.now().hour < 18 and (datetime.now().hour) >= 8):
                    fb.put("HOME", 'FAN_STATUS', 'ON')
                else:
                    fb.put("HOME", 'LED_STATUS', 'ON')
                    fb.put("HOME", 'FAN_STATUS', 'ON')
  
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)  
  
    key = cv2.waitKey(1)
    if key == ord('q'):
        if motion == 1:
            b = datetime.now()
        
            if (b - a).total_seconds() > 6:
                if (datetime.now().month == 11) or (datetime.now().month == 12) or datetime.now().month == 1 or datetime.now().month == 2:
                    if not ((datetime.now().hour < 18 and (datetime.now().hour) >= 8)):
                        fb.put("HOME", 'LED_STATUS', 'ON')
                else:
                    if (datetime.now().hour < 18 and (datetime.now().hour) >= 8):
                        fb.put("HOME", 'FAN_STATUS', 'ON')
                    else:
                        fb.put("HOME", 'LED_STATUS', 'ON')
                        fb.put("HOME", 'FAN_STATUS', 'ON')
            break

    
video.release()
cv2.destroyAllWindows()