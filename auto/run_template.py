import matplotlib.pyplot as plt
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage
import torch
import torch.nn as nn
import numpy as np
import seaborn as sns

K_P = 0.4
K_I = 0.035
K_D = 0.1
    
STEPS = 550
    
car = make_car(desired_v=20.0, dt=0.1)
'''Because the initial error is large, the proportional term initially commands strong acceleration. 
In my implementation, the derivative term also experiences a large positive change on the first timestep 
because the previous error is initialized to zero, which creates a brief startup transient. 
Once the car begins accelerating and the error starts decreasing, the derivative term becomes negative 
and opposes the acceleration command. Increasing \(K_D\) strengthens this damping effect, so the car 
approaches the target with less overshoot. The integral term is what helps eliminate the remaining 
steady-state error.'''
#WRITE CODE HERE
velocities = []
errors = []
times = []
'''learn passing in python function arguments'''

def a_des_over_time(calc_thrott):
    for i in range(STEPS):
        calc_des, error = calculate_desired_acceleration(car, K_P, K_I, K_D)
        calc_thrott = acceleration_to_throttle_percentage(calc_des, 1000, 5000)
        update(car, calc_thrott, 1000, 5000, 2.0)
        velocities.append(car["v"])
        errors.append(error)
        times.append(car["t"])

plt.figure()
plt.xlabel("time(s)")
plt.ylabel("velocity(m/s)")
plt.plot(times, velocities)
plt.figure()
plt.xlabel("time(s)")
plt.ylabel("errors(e)")
plt.plot(times, errors)
plt.show()
