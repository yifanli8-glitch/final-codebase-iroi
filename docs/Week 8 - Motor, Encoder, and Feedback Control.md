# Week 8 - Motor, Encoder, and Feedback Control

## Slide 1

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
Techin 512
Introduction to Sensors and Circuits
University of Washington
Haonan Peng
2025 Autumn
1


## Slide 2

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
2
Last Week - Photoplethysmogram (PPG or Pleth)
A PPG (Photoplethysmography) sensor is an optical device used to measure 
blood volume changes in the microvascular tissue, by emitting light into the 
skin and detecting the amount of light reflected or absorbed, which varies with 
the pulsatile flow of blood.
PPG is used in smartwatches, fitness trackers, and medical monitors to 
measure heart rate, blood oxygen (SpO₂), and vascular health.
Left image from: https://slatesafety.com/revolutionizing-workplace-safety-ppg-sensors/ 
Right image from: https://www.ansys.com/blog/modeling-human-skin-and-optical-heart-rate-sensors


## Slide 3

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
3
Last Week - Low-Pass Filter – Moving Average
For a moving average filter, a larger time window in a moving average filter 
gives smoother output. However, larger time window can also result in loss of 
signal details and peaks. For different signal, we should test for optimized window 
size.


## Slide 4

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
4
This week
• Motors
• Encoder sensors
• Feedback control


## Slide 5

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
5
Motors and Linear Actuators
Left image from: https://twen.rs-online.com/web/p/dc-motors/2389721?srsltid=AfmBOooyLjgnmpmOUglCgofkci2phKSbbSaSI6wzCzfH3_E0gN0O4Ryl
Right image from: https://www.progressiveautomations.com/products/linear-actuator-with-potentiometer
A motor converts electrical energy into rotational motion
by generating torque through electromagnetic interactions.
A linear actuator converts electrical energy into straight-
line motion, typically using mechanisms such as motors 
with screw drives, gears, or electromagnetic forces.


## Slide 6

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
6
Force and Torque
image from: https://nationwideautotransportation.com/blog/role-torque-cars/
Force is a push or pull that changes an object’s accleleration, 
described by magnitude and direction. 
Torque is the rotational equivalent of force—how much a 
force causes an object to twist, depending on both the force 
and the distance it is applied from the pivot point.


## Slide 7

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
7
Basic DC motor and how it works
image from: https://scienceready.com.au/pages/operation-of-a-simple-dc-motor?srsltid=AfmBOopIrYIpTaaUr7NjtenYflouPfYMRTPmYXD4H5vMtQTm7aDK1QsK
A basic DC motor works by sending current through a coil
inside a magnetic field, which creates an electromagnetic 
force that pushes the coil to rotate; a commutator switches 
the current direction every half-turn so the torque keeps 
driving the motor in the same direction.
Larger current -> larger torque and force.


## Slide 8

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
8
Stepper Motor 
image from: https://www.phidgets.com/docs/Stepper_Motor_and_Controller_Guide?srsltid=AfmBOoomw4KDaCnGfE1m40vYh-ZEHQcm1DxvNc2mW46cXkaJ9ke9Z9G_
A stepper motor is a motor that moves in precise, fixed 
angular increments (“steps”) by energizing coils in 
sequence, allowing accurate position control without 
needing a feedback sensor.


## Slide 9

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
9
Servo Motor 
image from: https://soldered.com/categories/actuators/stepper-servo-motors/?srsltid=AfmBOoovG-PWlGdQ6L_814GmoilYENFEnp5Iyl_hHrjbqn7rL7iO3nSv
A servo motor is a motor with a built-in feedback system 
that continuously measures its position and adjusts itself so it 
can hold or move to a commanded angle accurately and 
quickly.


## Slide 10

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
10
Incremental Control VS Absolute Control
0 M
5 M
10 M
Move forward for 5 M
Move to 5 M
Incremental control commands 
movement by specifying changes relative 
to the current position.
Absolute control commands movement 
by specifying a target position referenced 
to a fixed coordinate system


## Slide 11

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
11
DC motor VS Stepper Motor VS Servo Motor
Left image from: https://scienceready.com.au/pages/operation-of-a-simple-dc-motor?srsltid=AfmBOopIrYIpTaaUr7NjtenYflouPfYMRTPmYXD4H5vMtQTm7aDK1QsK
DC Motor
Pros
•Simple, inexpensive, widely 
available
•Smooth continuous rotation
•Easy to control speed
Cons
•No inherent position control
•Requires external sensors 
for precise motion
•Less accurate without 
feedback
Stepper Motor
Pros
•precise, discrete steps
•No feedback sensor needed
•High torque at low speeds
Cons
•Can lose steps under heavy 
load 
•Less efficient and can run hot
•Limited speed
Servo Motor
Pros
•Accurate position control
•High torque, fast response
•Maintains position under 
varying load
Cons
•More expensive
•More complex control 
signals
•Limited rotation range 
(typically 0–180°)


## Slide 12

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
12
Brushed motor VS Brushless Motor
Right image from: https://www.maxongroup.com/en-us/drives-and-systems/brushless-dc-motors
Brushed Motor
Pros
•
Simple and inexpensive
•
Easy to control
•
Good torque at low speeds
Cons
•
Shorter lifespan
•
Electrical noise and heat
•
Lower efficiency and speed
Brushless Motor (BLDC)
Pros
•
High efficiency, high speed, long lifespan
•
low maintenance and low electrical noise
•
Precise control and better performance 
under varying loads
Cons
•
Expensive
•
Complex control


## Slide 13

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
13
AC Motors
image from: https://en.wikipedia.org/wiki/AC_motor
An AC motor uses alternating current to create a rotating magnetic field 
that drives the rotor, making it efficient, durable, and suitable for 
continuous high-power operation.
AC motors are typically used in high-power, constant-speed, industrial 
or household applications (fans, pumps, compressors, appliances) 
because they are efficient, robust, and easy to run from the AC mains.
DC motors are preferred in applications requiring variable speed, 
portable battery power, or fine control (robots, drones, small devices), 
because their speed and torque are easier to adjust electronically.


## Slide 14

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
14
Power Supply for Motors
image from: https://www.makerfabs.com/l298n-motor-driver-board.html?srsltid=AfmBOootbjG7L8Ec3RKXdeSu3KDgckvatIfNKVd1g68ytDMyAZoaR1gk
Compared with microcontrollers and sensors which often need 3.3V or 5V 
power, motors often need larger voltage and draws much larger 
current and cannot be provided by USB. Thus, in prototyping, we 
should consider giving motor a separate stronger power supply.   
Motor Driver 
Board 
5V
USB
12V
12V
Control
Command


## Slide 15

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
15
Motor Drivers
image from: https://www.makerfabs.com/l298n-motor-driver-board.html?srsltid=AfmBOootbjG7L8Ec3RKXdeSu3KDgckvatIfNKVd1g68ytDMyAZoaR1gk
A motor driver board is an electronic module that allows a microcontroller (like 
Arduino, ESP32, Raspberry Pi) to safely control motors by providing the required 
voltage, current, and switching signals that the microcontroller itself cannot supply.
The L298N motor drivers let a microcontroller control the direction and speed of 
two DC motors by providing high-current, high-voltage switching using simple logic 
and PWM inputs.
Higher PWM Duty -> higher motor torque 
L298N
Motor Driver 
Power 
Supply
MCU
PWM Signal 
Motor 1
Motor 2


## Slide 16

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
16
Gear Ratio for Motors
Some motors come with gear box of a certain ratio.
A motor gearbox uses gears to reduce speed and increase torque, 
allowing the motor to drive heavier loads more effectively.
Example: a gear ratio of 3:1 will ideally make the output torque about 3×
larger and the output speed about 3× slower.
Larger gear ratio -> larger torque, lower speed, larger friction.
Small or zero gear ratio -> small torque, fast speed, small friction (fast 
response).
Motor
Gear
Box
image from: https://www.amazon.com/dp/B0CW1TCCTL?ref=ppx_yo2ov_dt_b_fed_asin_title


## Slide 17

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
17
How to choose motor
•
Required torque (how much force)
•
Required speed
•
Load type (constant or varying)
•
Size and weight
•
Power supply availability (voltage and current limits)
•
Noise and vibration limits
•
Gear ratio
•
Precision and control


## Slide 18

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
18
Encoder Sensor (Optical)
An encoder is a sensor that measures the rotation or position of a motor shaft 
by generating pulses or digital signals, allowing a system to track speed, 
direction, and precise angular position.
An optical encoder uses a light source and a patterned disc to generate 
light–dark pulses as the disc rotates, allowing precise measurement of position, 
speed, and direction based on how the light is interrupted.
A and B channels are used to determine the direction of rotation. I channel (index) 
is to indicate a new round start or zero (home) positon.
Left image from: https://no.farnell.com/en-NO/broadcom/aedb-9140-a13/incremental-encoder-mod-
optical/dp/1161087?srsltid=AfmBOorw6_zvXVs6IWP85OXDuxvCLr4Aa1xR_X9rVEqVUvjhbXR72IEq
Right image from: https://www.applied-motion.com/s/article/difference-between-optical-and-capacitive-encoders


## Slide 19

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
19
Encoder Sensor (Magnetic)
A magnetic encoder uses a rotating magnet and magnetic sensors to detect 
changes in the magnetic field, allowing it to measure rotation or position even in 
dusty, oily, or high-vibration environments.
Optical encoders: better accuracy and resolution, sensitive to dust and oil
Magnetic encoders: less accuracy and resolution, robust to dust and oil
Left image from: https://www.maccon.com/rotary-linear-encoders/magnetic-encoders/bogen.html
Right image from: https://www.hsmagnets.com/blog/universal-magnetic-rotary-encoders/


## Slide 20

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
20
Parameters of Encoders
•Resolution: counts per revolution or CPR (count per round)
•Accuracy: how close the measurement is to the true position
•Repeatability: how consistently it returns the same reading under the same motion
•Maximum speed: highest RPM (rounds per minute) the encoder can measure
•Power requirements: operating voltage and current
•Environmental robustness: dust, oil, temperature, vibration tolerance


## Slide 21

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
21
Encoder Index and Zero Calibration
Many encoders are incremental (no index “I” channel), which means that 
they will always start with 0 reading and count for incremental rotation 
when powered on, and do not know the absolute position.
In order to know absolute position, we should choose encoders with 
index. Alternatively, we can also start the power or register zero when the 
motor is in home location. For example, it is like turn the clock back to 0 
before starting the timing.


## Slide 22

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
22
Encoder Counter Chip
An encoder counter chip is an integrated circuit that takes the high-speed 
pulse signals from an encoder and reliably counts them, providing the 
microcontroller with clean position, direction, and speed information 
without overloading its CPU.
Example: If I have an encoder with 10000 CPR (count per round), and 
encoder counter counted 1000. it means that the motor has rotated 36 deg. 
1000
counts
36
degree


## Slide 23

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
23
Motor Control - Motivation
Assume we want to use a basic DC motor to rotate a bar for exactly 90 
deg to open a lid and maintain the position. 
We can control the torque of the motor, but in real practice, the lid has 
inertia and joint has friction. Thus, it can be difficult to accurately control 
the lid and maintain 90 deg open.
(In fact, a servo motor can easily do it in real practice. But assume we 
have to use basic DC motor since servo motors may not always be 
available.)
Motor


## Slide 24

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
24
Motor Control – Feedforward Control
If we do not have any sensor we can use feedforward control. 
Feedforward control predicts the system’s required input based on a 
model and applies it directly, without waiting for feedback, to achieve the 
desired output.
Feedforward control has fast response with no delay, but it requires 
accurate model (often very difficult) of the system (frictions, inertias, and 
so on).
In real practice, feedforward control can often hardly be very accurate.
Feedforward
Controller
Input Control 
Command
Shaped Control 
Command
System & 
Process
Output
(Desired Angle)
(Motor Torque)
(Actual Rotation)


## Slide 25

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
25
Motor Control – Feedback Control
If we have sensor that can take direct or indirect measurements of the output, 
we can use feedback control. 
Feedback control measures the system’s actual output and continuously 
adjusts the input to reduce the error between the measured value and 
the desired value.
In real practice, feedback control is often preferred when sensor is available.
Feedback
Controller
Input Control 
Command
Shaped Control 
Command
System & 
Process
Output
(Desired Angle)
(Motor Torque)
(Actual Rotation)
Feedback
(Measured Rotation)


## Slide 26

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
26
Motor Control – Feedback Control
Pros
•Automatically corrects 
disturbances and uncertainties
•Robust even when the system 
model is imperfect
•Provides stable, accurate 
performance over time
Cons
•Slower response due to sensing 
and correction
•Can become unstable if tuned 
poorly
•Requires sensors and continuous 
measurement
Feedback
Controller
Input Control 
Command
Shaped Control 
Command
System & 
Process
Output
(Desired Angle)
(Motor Torque)
(Actual Rotation)
Feedback
(Actual Rotation measured by Sensor)


## Slide 27

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
27
Basic Feedback Control
Feedback
Controller
Input Control 
Command
Shaped Control 
Command
System & 
Process
Output
(Desired Angle)
(Motor Torque)
(Actual Rotation)
Feedback
(Actual Rotation measured by Sensor)
The basic feedback control is simple. For example, if we command the 
rotation to be 90 deg but the encoder sensor measured the actual rotation of 
80 deg. We can then command the motor to rotate 10 deg more.
However, this basic feedback control can be inaccurate due to the imperfect 
system (rotates 80 when commanded 90), especially if the goal is dynamic 
(keeps changing over time).


## Slide 28

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
28
Proportional-Integral-Derivative (PID) Feedback Control
PID control adjusts a system’s input using three terms—proportional, 
integral, and derivative—to reduce error quickly, eliminate steady-state 
offset, and smooth the response.
PID is simple, robust, and widely effective for achieving stable and 
accurate control in many systems without needing a detailed mathematical 
model.
PID can be hard to tune, may perform poorly on highly nonlinear or fast-
changing systems, and can become unstable if parameters are chosen 
incorrectly.
Image from: https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller


## Slide 29

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
29
Proportional-Integral-Derivative (PID) Feedback Control
PID control has 3 terms:
P-term: The proportional term reacts to the current error, providing 
immediate correction based on how far the system is from the target.
I-term: The integral term reacts to accumulated past error, removing 
steady-state offsets that P alone cannot eliminate.
D-term: The derivative term reacts to the rate of change of error, predicting 
future behavior to reduce overshoot and improve stability.
Kp, Ki, and Kd are coefficients P gain, I gain, and D gain, respectively.
Image from: https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller
Shaped Control 
Command
P-term
I-term
D-term


## Slide 30

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
30
Proportional-Integral-Derivative (PID) Feedback Control
anti-windup
In practice, many control systems are digital (not continuous). So in each 
control loop, we have our input command rk and measured output yk. k is the 
current control loop No. So that the error is:
𝑒𝑘= 𝑟𝑘−𝑦𝑘
Then we have the PID shaped control to be:
In real practice, we should also pay attention to the filtering of D-term and 
anti-windup if I-term.
P-term
I-term
D-term
Control loop 
interval


## Slide 31

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
31
PID Feedback Control – Tuning Parameters
Tuning P, I and D gains is very important to achieve accurate and stable 
control. A general suggestion is:
Start with P-only: Increase Kp until the system responds quickly but begins 
to oscillate—this gives you a sense of system sensitivity. 
Add I to remove steady-state error: Increase Ki slowly until the system 
reaches the target without persistent offset, but stop before oscillations.
Add D to stabilize: Increase Kd to reduce overshoot and smooth the 
response, but avoid too much since it amplifies noise.
Advanced PID tuning methods: Ziegler–Nichols method, Cohen–Coon 
method
Image from: 
https://en.wikipedia.org/wiki/Proportional%E2%80%9
3integral%E2%80%93derivative_controller


## Slide 32

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
32
PID Feedback Control – P Gain
P-term: The proportional term reacts to the current error, providing 
immediate correction based on how far the system is from the target.
If P gain is too large, we may have oscillation. If P gain is too mall, the 
system may be slow on response to control command.


## Slide 33

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
33
PID Feedback Control – I Gain
I-term: The integral term reacts to accumulated past error, removing 
steady-state offsets that P alone cannot eliminate.
If I gain is too large, we may have larger overshooting. If I gain is too mall, 
the system may have steady-state error.


## Slide 34

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
34
PID Feedback Control – D Gain
D-term: The derivative term reacts to the rate of change of error, predicting 
future behavior to reduce overshoot and improve stability.
If D gain is too large, we may have oscillation. If I gain is too mall, the system 
may have larger overshoot.


## Slide 35

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
35
Control Theory (Optional)
Control theory studies how to regulate the behavior of dynamic systems—
keep a system stable, accurate, and responsive despite disturbances.
Example Application
IoT: Control a heater to maintain constant temperature
Robotics: Accurate robot arm joint rotations for manipulation
Further study: Control Bootcamp video series (Prof. Steve Brunton UWME)
Image from: https://erc-bpgc.github.io/handbook/automation/ControlTheory/Control_Theory/


## Slide 36

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
36
Control Theory – Stability (Optional) 
Stability describes whether a system naturally stays near or returns to an 
equilibrium (such as a desired position, speed, or output) after being 
disturbed.
A system is stable if small disturbances cause outputs that remain bounded 
and eventually settle back toward equilibrium.
A system is unstable if disturbances grow over time, driving the output 
away from equilibrium.
Stable
Unstable


## Slide 37

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
37
Control Theory – Observability (Optional) 
Observability describes whether a system’s internal states can be 
determined from its outputs over time.
If we can reconstruct the full internal behavior using only the sensors we 
have, the system is observable.
If some internal states can never be inferred from measurements, the 
system is not observable.
For example, if a drove has both gyroscope and accelerometer, we can 
obtain the full position, velocity, orientation – observable.
Image from: https://www.wired.com/2017/05/the-physics-of-drones/
However, if a drove only has accelerometer, 
we can only know the acceleration but not 
orientation – not observable.


## Slide 38

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
38
Control Theory – Controllability (Optional) 
Controllability describes whether a system’s inputs can move the internal 
state to any desired state within finite time.
If the actuators can drive the system anywhere we want (within its model), 
the system is controllable.
If some states cannot be influenced by the inputs, the system is not 
controllable.
For example, HVAC systems are controllable with both heating and cooling, 
while a fridge is not fully controllable since it only has cooling.
Left Image from: https://envigaurd.com/topics/hvac-system-working-principle/
Right image from: https://www.cuisinart.com/3.1-cu.-ft.-compact-fridge/CCF-31.html?srsltid=AfmBOooBYYi_O0woKedgilb8vY3zTrH4N_52n37cw0Eed26Wul9yUo79
HVAC
(controllable)
Fridge
(not controllable)


## Slide 39

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Motor, Encoder, and Feedback Control
39
Announcements
• Guest Lecture on Nov. 25 (Tue): Dr. Sosnovskaya
Zoom Link: https://washington.zoom.us/j/91015797291
• Please check your Canvas grades and contact 
Haonan if there is anything wrong in lab teams 
grading.
