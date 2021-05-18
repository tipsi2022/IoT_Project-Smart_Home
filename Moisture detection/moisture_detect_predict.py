import time
import random
import numpy as np
import pandas as pd
from firebase import firebase

df = pd.read_csv(r'moisture_para.csv')

slope = df['slope']
intercept = df['intercept']

fb = firebase.FirebaseApplication("Enter Your Firebase Realtime-Database URL")

while True:
    x_sensors = np.zeros(3)
    for i in range(3):
        x_sensors[i] += random.uniform(0.1, 5)

    x_sensors_temp = np.average(x_sensors)

    x = 1.0/x_sensors_temp
    moisture_predict = slope*x + intercept
    print(moisture_predict[0])
  
    if (moisture_predict[0] < 0.15):
        fb.put("HOME" , 'SPRINKLER_STATUS', 'ON')
    else:
        fb.put("HOME" , 'SPRINKLER_STATUS', 'OFF')
        
    time.sleep(10)