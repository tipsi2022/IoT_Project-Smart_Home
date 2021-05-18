import numpy as np
import pandas as pd
from scipy import stats

file = r'Enter Your File Location'
df = pd.DataFrame()
df = pd.read_csv(file)

container_mass = 22.75 
soil_mass_dry = 24.74 
soil_vol = 200 

rho_s = (soil_mass_dry/1000.0)/(soil_vol*np.power(10.0,-6.0)) 
rho_w = 997.0 

soil_masses = np.subtract(df['Soil Masses'],container_mass) 
cap_sensor_readings =  np.array(df['Sensor Reading'])

theta_g = (soil_masses - soil_mass_dry)/soil_mass_dry 
theta_v = ((theta_g*rho_s)/rho_w) 

x_for_training = 1.0/cap_sensor_readings 
slope, intercept, r_value, p_value, std_err = stats.linregress(x_for_training, theta_v)
print(slope)
print(intercept)

temp = pd.DataFrame(columns = ["slope", "intercept"])
temp = temp.append({"slope":slope ,"intercept":intercept}, ignore_index = True)
print(temp)

temp.to_csv("moisture_para.csv")