# Software Onboarding Projects - Fall 2026 (fs-5 design cycle)

## PID Controller Using Python/PyTorch for Minimizing Longitudinal Error

This project displays the basic implementation of a P.I.D. controller, which focuses on maintaining longitudinal control of the car. The controller converts the `error term`, the difference between the `controlled variable` and `commanded variable`, into suitable actuator commands so that over time the error is driven to `0`. In this scenario, the P.I.D. controller is to ensure that the car's velocity converges toward a desired velocity. 

The PID controller uses 3 tuned constants in order to do so: 

1. `Proportional Gain` - Utilizes the error at the present moment to determine the required corrective response. The greater the current error is, the greater the corrective response becomes. The proportional gain responds with less intensity as the `controlled variable` approaches the `commanded variable`.

2. `Integral Gain` - Sums up the input total over time, so it has memory of what has happened before. The integrator path will continue to display activation so long as `steady state error` exists within the system. Initially, when the system achieves the target and continues to move past it, this is called `overshoot`, which lowers the output of the integrator.

3. `Derivative Gain` - Produces a measure of the rate of change of the error. Uses the rate of change of the error term to determine how fast the `controlled variable` is approaching the `commanded variable`. It can prematurely lower the strength of actuators in order to mitigate `overshoot`.

## P.I.D. Controller Diagram
![A diagram of a P.I.D. controller by MATLAB](image.png)
For more information: https://www.mathworks.com/discovery/pid-control.html

## P.I.D. Controller Installation & Implementation

1. Clone this repository.
2. Install numpy: https://numpy.org/install/
3. Install matplotlib: https://matplotlib.org/stable/install/index.html
4. Install PyTorch: https://pytorch.org/get-started/locally/
5. Run the following files respectively: `pid_template.py`, `run_template.py`, `run_template_copy.py`
6. Observe all graph predictions.


## Tuning and Implementation


## Known Issues (Work In Progress)

This project is still ongoing, as the linear regression model in PyTorch, specifically the training loop, needs to be completed.









- [Autonomous Team Onboarding Projects](auto)

