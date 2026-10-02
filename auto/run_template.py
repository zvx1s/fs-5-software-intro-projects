import matplotlib.pyplot as plt
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage

K_P = 0.4
K_I = 0.035
K_D = 0.1
 
STEPS = 550
 
car = make_car(desired_v=20.0, dt=0.1)

#WRITE CODE HERE
velocities = []
errors = []
times = []
'''learn passing in python function arguments'''
for i in range(STEPS):
    calc_des, error = calculate_desired_acceleration(car, K_P, K_I, K_D)

    calc_thrott = acceleration_to_throttle_percentage(calc_des, 1000, 5000)
    update(car, calc_thrott, 1000, 5000, 2.0)
    velocities.append(car["v"])
    errors.append(error)
    times.append(car["t"])

plt.figure()
plt.xlabel("time(t)")
plt.ylabel("velocities(v)")
plt.plot(velocities)
plt.figure()
plt.xlabel("time(t)")
plt.ylabel("errors(e)")
plt.plot(errors)
plt.show()
