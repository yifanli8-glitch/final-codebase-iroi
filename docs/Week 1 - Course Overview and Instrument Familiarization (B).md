# Week 1 - Course Overview and Instrument Familiarization (B)

## Slide 1

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
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
Course Overview and Instrument Familiarization
Instructor
Haonan Peng (UW Electrical & Computer Engineering)
Office Hours Tuesday & Wednesday 5:30–6:30 PM (in person), other times by 
appointment
Reader/Graders
Rebecca Huang
Cherry M Roy
Prototyping Labs Specialist: Zubin A Assadian
Schedule
Section A: Tuesday, 1:30–5:30 PM (lecture + lab)
Section B: Wednesday, 1:30–5:30 PM (lecture + lab)
2
Course Logistics


## Slide 3

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
3
Haonan Peng
Ph.D. Candiate, Electrical & Computer Engineering at UW
M.S. Mechanical Engineering, University of Washington
B.S. Mechanical Engineering, Central South University
Surgical Robotics
Cable-driven Accuracy
Haptic Feedback
Computer Vision


## Slide 4

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
Rebecca Huang
4
MSTI C8 student at UW
B.S. Integrated Design and Media, New York
University
HCI
UX Research & Design


## Slide 5

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
5
Cherry Mathew Roy
M.S. Technology Innovation, University of Washington
BTech. Mechanical Engineering, APJ Abdul Kalam Technological University
Product Management 
UX Design
Entrepreneurship
Product Design
Automobiles


## Slide 6

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
6
Let’s Start with AI
ChatGPT
Claude
Gemini 
LLaMA
Stable Diffusion
Large Language Model
Large Language Model
Large Language Model
Large Language Model
Generative Image Model


## Slide 7

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
7
The Bitter Lesson
by Prof. Richard Sutton (University of Alberta)
The bitter lesson states that in AI, methods leveraging computation and 
general learning algorithms consistently outperform approaches relying on 
human knowledge or handcrafted solutions.
Data
& Computation >
Human Knowledge 
& Engineering
"All models are wrong, but some are useful“ (wiki)
--George Box


## Slide 8

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
8
Internet of Things (IOT) and Robots
IoT and robotic systems are interconnected technologies that sense and collect 
data from the environment, process it intelligently, and then perform actions
through actuators to interact with the physical world.
Sensing
Processing
Decision
Making
Actuation


## Slide 9

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
9
Can or Will Data and AI solve IoT and Robotics?
Inspired by Prof. Ken Goldberg (UC Berkeley) 
Large data has solved language.
Large data has solved vision.
Can large data solve IoT and Robotics?
Watch the debate: Data Will Solve Robotics and 
Automation: True or False?
On 2025 IEEE International Conference on 
Robotics and Automation (ICRA)
https://www.youtube.com/watch?v=PfvctjoMPk8&t=
258s


## Slide 10

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
10
Can Data and AI solve IoT and Robotics?
Opinions from Prof. Abhishek Gupta (UW CSE)
•
The bitter lesson assumes data is cheap and abundant., which is 
usually true for language and vision.
•
For IoT and robotics, along with compute scale, we need to find data 
sources that scale cheaply. Scale must be considered both 
computationally and economically, while capturing the "complexity" 
of the real world.
Social Media
1–2 billion posts daily worldwide
Free
Surgical Robot
Only ~30 around the world
$300000


## Slide 11

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
11
Can AI Replace Sensors?
What is the weight?
Computer Vision AI: object classification, size… 
Weight Scale: direct measurement


## Slide 12

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
12
Sensors for AI
•
Data acquisition – AI needs data
•
Ground truth – better training data, better model
•
Environmental awareness – real-time input for AI
•
Safety – detect anomalies, collisions, emergency stop


## Slide 13

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
13
What are circuits?
Circuits are networks of interconnected electrical components (resistors, 
LEDs, sensors) forming closed paths that guide and control the flow of charge 
to perform functions like:
➢Powering sensors – providing proper and stable voltage
➢Filtering noises – smoothing the sensor readings
➢Amplifying signals – improving resolution of the sensor reading


## Slide 14

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
14
What are sensors?
A sensor is often defined as a device that receives and responds to a 
signal or stimulus. The stimulus is the quantity, property, or condition that 
is sensed and converted into electrical signal [1]. 
1 FRADEN, JACOB (2004). HANDBOOK OF MODERN SENSORS (3rd ed.). New York: Springer. p. 1. ISBN 0-387-00750-4.
Environment / 
Object
Temperature
Light
…
Sensor
Analog / Digital
Measurements
Processor
Load Cell
One-wire 
Temperature Sensor


## Slide 15

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
15
What are sensors?
Not all sensors have to convert physical quantities into electrical signals. 
Broadly speaking, a sensor is any device or material that converts 
information from the environment into a recognizable or usable 
form.
But for IoT and robotic systems, sensors are almost always designed 
to output electrical signals.
pH test strips
Mercury/alcohol thermometers


## Slide 16

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
16
What can sensors do?
Ambient Fire Detecting Exit Sign
Can we have an Exit sign that can detect fire and light up automatically?
Example from Techin 515 2022S, credit: Chen-Yin, Teja, Tiffany, Saif


## Slide 17

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
17
What can sensors do?
Ambient Fire Detecting Exit Sign
Can we have an Exit sign that can detect fire and light up automatically?
Example from Techin 515 2022S, credit: Chen-Yin, Teja, Tiffany, Saif


## Slide 18

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
18
What can sensors do?
Robot arm control
How can we accurately control the pose of a surgical robot arm?


## Slide 19

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
19
What can sensors do?
Robot arm control
How can we accurately control the pose of a surgical robot arm?
[1]
[1]
1 https://www.youtube.com/watch?v=pja_n8ThDsU
https://www.sensortips.com/featured/what-are-rotary-optical-rotary-encoders/
https://www.e-jpc.com/products/encoders/
Leader Controller 
Follower Surgical Robot
Encoder (Optical)


## Slide 20

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
20
What can sensors do?
Robot arm control
How can we accurately control the pose of a surgical robot arm?


## Slide 21

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
21
In Class Practice
What sensors are there in your cell phone? Try to name as many as you can.
Also think about 
1) what information they measure 
2) the applications of these measurements


## Slide 22

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
22
In Class Practice
Sensor
Information Measured
Applications
Camera
Vision
Photography, Face ID
Accelerometer
Linear acceleration
motion detection, step 
counting
Gyroscope
Angular velocity / orientation
image stabilization, gesture 
recognition
Proximity Sensor
distance from objects
Screen off during calls
Microphone
Voice, sound
Voice calls
Light Sensor
Intensity of surrounding light
Auto brightness
Touchscreen 
Capacitive changes across 
the screen
touch input
Thermometers 
Device and battery 
temperature
Device protection, battery 
management
1) How many sensors are there in your cell phone? Try to name as many as you can 
2) What information do they measure? 
3) What are the applications of these measurements?


## Slide 23

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
23
Course Overview
Section A: Tuesdays, 1:30pm - 5:20pm
Section B: Wednesdays, 1:30pm - 5:20pm
1 hour class + 3 hour lab (lab reports due after 1 week)
Grading:
50% Labs and reports (team-based work)
45% Final Project (individual work) 
5%   Lab and code check (individual interview)
Communication:
Microsoft Teams for most questions, emails for grading related questions 
(please include [TECHIN 512] in title so that your email gets priority)
All details on Canvas (Section A)
All details on Canvas (Section B)


## Slide 24

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
24
Course Objectives
1.
Apply engineering thinking skills to design, build, and manage sensor- and 
circuit-based projects.
2.
Specify and evaluate requirements for sensor systems.
3.
Design and analyze DC, RC, and digital circuits.
4.
Apply temperature, force, and biomedical sensors in functional systems.
5.
Implement calibration and error compensation techniques.
6.
Implement feedback control techniques.
7.
Integrate sensors with microcontrollers (ESP32/Arduino) for data collection 
and processing, such as filtering.
8.
Demonstrate and communicate technical results through a final project.
Accuracy
Reliability
Efficiency


## Slide 25

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
25
Course Schedule (details on Canvas)
Week Date
Topic
Lab
1
9/24
No class in the first week
No lab in the first week
2
9/30 & 10/1 Sensors and Circuits in Action
Lab 1 Get to know the Instruments
Assigned: Final Project Take-Home Assignment 1
3
10/7 & 10/8 DC Circuit and Microcontroller
Lab 2 Build DC Circuits and Voltage Dividers
Due: Lab 1 report
4
10/14 & 
10/15
RC Circuit and Power Management
Lab 3 Build Resistor–Capacitor Circuits
Due: Lab 2 report
Due: Fina Project Take-Home Assignment 1
Assigned: Final Project Take-Home Assignment 2
5
10/21 & 
10/22
555 Timer and Logic Circuit
Lab 4 Implement 555 Timers and control delay
Due: Lab 3 report
6
10/28 & 
10/29
Sensors Overview and Load Cells
Lab 5 Implement Strain Gage and Load Cell for Force Measurement
Due: Lab 4 report
Due: Final Project Take-Home Assignment 2
Assigned: Final Project Take-Home Assignment 3
7
11/4 & 11/5 Temperature Sensing and Calibration Lab 6 Implement Temperature Sensors
Due: Lab 5 report
8
11/14 & 
11/12
Biosensors and Filtering
Lab 7 Implement Photoplethysmogram Sensor and Measure Heart Rate
Due: Lab 6 report
Due: Final Project Take-Home Assignment 3
Assigned: Final Project Take-Home Assignment 4
9
11/18 & 
11/19
Encoders, Motors, and PID Control
Lab 8 Control Motors with Encoder Feedback
Due: Lab 7 report
10
11/25 & 
11/26
Guest lecture (TBD)
In-class work on the project
Due: Lab 8 report
Due: Final Project Take-Home Assignment 4
11
12/2 & 12/3 Final project presentations
Due: Final project report (12/5)


## Slide 26

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
26
Course Policy
Use of AI Tools
Usage of AI tools such as ChatGPT is allowed in both the labs and the project. It can be very beneficial
for engineers to utilize AI for better solutions and productivity. However, for your learning experience and
outcome, it is important that you understand the AI-provided solution and can add your own value to the
AI solution. 5% of the overall grade of this course will be based on an individual lab/code check,
which is a short individual interview with the instructor. During the interview, the instructor will ask
questions about technical details and code (you write, not the provided ones) in the labs.
•
Add your own value to AI outputs
•
Use AI for learning and productivity, NOT for completing assignments ASAP


## Slide 27

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
27
Final Project
All details on Canvas (Section A)
All details on Canvas (Section B)


## Slide 28

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
28
Voltage
Voltage (V or U) is defined as the difference in electric potential between two 
points. The unit for voltage is named volt (V).
In physics, an object has potential energy because it has a potential to do work, 
relative to other objects, such as compressed springs, a ball on a hill, and charged 
batteries.


## Slide 29

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
29
Current
An electric current (I) is the speed (or rate) of the flow of electric charge past a point 
or a surface. The unit of electric current is the ampere(A).


## Slide 30

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
30
Resistance
Resistance is a physical quantity that describes the ability of a substance to impede 
current flow. The unit of resistance is Ohm(Ω).


## Slide 31

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
31
Power Supply
•
Power circuits and sensors
•
Provide protection against shortcut (batteries cannot)
Always set current limit first! 
Recommendation: start with 0.3A and increase when necessary


## Slide 32

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
32
Shortcut (Dangerous!)
In circuits, a shortcut (often just called a short) means that two points that should have a 
voltage difference between them are connected by a very low-resistance path.
In other words, shortcut means power and ground directly connected.
Shortcut can create huge current and heat, burn wires and power supply.


## Slide 33

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
33
Oscilloscope
•
Capture signal (voltage)
•
Waveform visualization
•
Applications: debugging 
circuits, signal analysis, 
fault detection


## Slide 34

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
34
Signal Generator
•
Generate waveform (voltage)
•
Applications: testing, 
calibration, prototyping, circuit 
stimulation


## Slide 35

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
35
Oscilloscope & Signal Generator VS. Microcontroller
Many microcontrollers can also generate waveforms and measure 
voltage, why do we still need oscilloscope & signal generator ?
Feature
Oscilloscope & Signal Generator 
Microcontroller
Accuracy
High precision, calibrated
Limited
Speed / Bandwidth
Very high (MHz–GHz)
Low (kHz–few MHz)
Signal Quality
true waveform
low-noise output
Noisy, needs filtering
Convenience
Instant use, built-in functions
Requires coding and 
external tools for display
Size
Huge
Small
Use Case
Debugging circuit, calibration
Embedded systems, 
prototyping IoT and Robot
Cost
>$500
<$30


## Slide 36

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
36
Digital Multimeter (DMM)
Measures:
•
DC/AC voltage
•
DC/AC current
•
Resistance
•
Temperature
•
And so on…


## Slide 37

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
37
Measuring Voltage
DC Power Supply
Resistor
What is the voltage across the resistor?
Recommendation: using red 
wire for power (positive), 
black wire for ground 
(negative)


## Slide 38

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
38
Measuring Voltage
What is the voltage across the resistor?


## Slide 39

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
39
Measuring Current
What is the current through the resistor?


## Slide 40

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Course Overview and Instrument Familiarization
40
Measuring Voltage VS Measuring Current
Voltage Measurement
(Parallel)
DMM NOT in the loop
Current Measurement
(Series)
DMM in the loop
