import time
import random
from firebase import firebase

fb = firebase.FirebaseApplication("Enter Your Firebase Realtime-Database URL")

while True:

    measured_temp = random.randint(20,40)
    print(measured_temp)
    
    if(measured_temp <= 24):
        fb.put("HOME", 'AC_STATUS', 0)
    elif (measured_temp >= 31):
        fb.put("HOME", 'AC_STATUS', 27)
    else :
        k = measured_temp - 27
        fb.put("HOME", 'AC_STATUS', 27 - k)
        
    time.sleep(5)