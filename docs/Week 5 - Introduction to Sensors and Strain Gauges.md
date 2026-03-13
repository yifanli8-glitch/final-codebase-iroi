# Week 5 - Introduction to Sensors and Strain Gauges

## Slide 1

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
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
Introduction to Sensors and Strain Gauges
2
Midterm Course Evaluation Feedbacks
• Difficulty, lack of fundamental knowledges
• More/less technical details, further self-study materials
• Lab instructions hard to follow, step-by-step instruction
• Detailed requirements in lab manuals easy to miss
• Long and fast-paced lectures, should be more interactive
• More breaks
• Make the final project teamwork


## Slide 3

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
3
Last Week - Analog VS Digital
Analog
Computer
Nature
Digital
Analog to Digital Converter
(ADC)
Digital to Analog Converter
(DAC)


## Slide 4

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
4
Last Week - Logic Gate
A logic gate is a basic digital circuit that performs a logical operation 
(such as AND, OR, or NOT) on one or more binary inputs to produce a 
single binary output.


## Slide 5

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
5
Last Week - 555 Timer
If we want to build a circuit that will turn on the LED for 10 seconds once we 
press a button? 
We can use 555 Timer in monostable mode.
Applications also include: automatic light or fan delay, camera flash timers
555 Timer 
Monostable Mode


## Slide 6

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
6
Internet of Things (IOT) and Robots
IoT and robotic systems are interconnected technologies that sense and collect 
data from the environment, process it intelligently, and then perform actions
through actuators to interact with the physical world.
Sensing
Processing
Decision
Making
Actuation


## Slide 7

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
7
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


## Slide 8

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
8
Sensor Types
Environmental Sensors
•
Temperature – thermistor, type K thermocouple, DS18B20 (one wire)
- Applications: air conditioners, refrigerators  
•
Humidity - measure moisture in the air (e.g., DHT22, SHT31)
- Applications: greenhouses, air humidifier
•
Pressure - detect air or fluid pressure (e.g., BMP280, MPX5010)
- Applications: car tire pressure monitors
•
Light - measure brightness or intensity (e.g., lux meter, photodiode)
- Applications: smartphone brightness control
•
Sound - detect sound levels (e.g., microphone, sound module)
- Applications: auto lights
Thermistor
One-wire 
Temperature Sensor
BMP 280 
Pressure Sensor
Lux Meter
dB Sound Meter


## Slide 9

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
9
Sensor Types
Motion / Position Sensors
•
Accelerometer – measures acceleration or tilt (e.g., ADXL345)
- Applications: vehicle crash detection
•
Gyroscope – measures angular velocity (e.g., MPU6050)
- Applications: drones
•
Proximity sensor – detects nearby objects (e.g., IR or ultrasonic sensor)
- Applications: parking sensors
•
Encoder – measures rotation angle or position (e.g. AEDT-9810)
- Applications: robotics, joint control
Accelerometer
Gyroscope
IR Distance 
Sensor
Encoder


## Slide 10

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
10
Sensor Types
Chemical / Biological Sensors
•
Gas sensor – detects gases like CO₂, CO, or methane (e.g., MQ series)
- Applications: smoke detectors, air purifiers
•
pH sensor – measures acidity or alkalinity of liquids
- Applications: in pool monitors, brew control
•
ECG sensor – measures the electrical activity of the heart  
-Applications: heart rate and rhythm monitoring, wearable health devices.
•
PPG sensor – detect blood volume changes
- Applications: smartwatches and fitness trackers, blood oxygen levels (SpO₂)
Gas Sensor
ph Sensor
ECG Sensor
PPG Sensor


## Slide 11

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
11
Sensor Types
Robotics Sensors
•
Ultrasonic sensor – measures distance using sound waves; 
- Applications: obstacle avoidance and range detection
•
Lidar – measures precise distances by timing reflected laser pulses
- Applications: mapping and autonomous navigation
•
Camera – captures visual images
-Applications: object recognition, tracking, navigation 
•
Encoders – measure wheel or joint rotation
- Applications: joint control, odometry
•
Force / Torque sensors: detect interaction forces
- Applications: robotic arms and grippers for precise manipulation
Ultrasonic Sensor 
Lidar
RGBD Camera
Strain Gauge


## Slide 12

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
12
How to choose sensors?
Accuracy and resolution
Accuracy determines how close the measurement is to the true value, 
while its resolution defines the smallest detectable change — both 
should match the precision needs of your application without unnecessary 
cost or complexity.


## Slide 13

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
13
How to choose sensors?
Frequency
Frequency response or sampling rate should be high enough to 
accurately capture the fastest changes in the measured signal without 
distortion or loss of information.
Fast Flying
Slow Movement


## Slide 14

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
14
How to choose sensors?
Direct and Indirect Measurement
When choosing between direct and indirect measurement, consider 
whether the sensor can measure the desired quantity itself or must 
infer it from related variables, balancing accuracy, complexity, and 
practicality.
Arterial Line
(direct, but intrusive)
Blood Cuff
(indirect, non-intrusive)


## Slide 15

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
15
How to choose sensors?
Power Consumption
When selecting a sensor, its power consumption should match the 
system’s energy budget, especially for battery-powered or portable 
devices, to ensure efficient and sustained operation.
Smart Exit
(Indoor with wired power)
Wild Animal Detection
(Battery powered)


## Slide 16

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
16
Strain Gauge/Gage
A strain gauge is a sensor that measures deformation (strain) in an object 
by detecting changes in its resistance when stretched or compressed.
When it is stretched, its length increases and cross-sectional area 
decreases, both of which increase resistance. (The road is longer but ) 
Conversely, when it is compressed, the length shortens, area increases, and 
resistance decreases
Image from: https://www.michsci.com/what-is-a-strain-gauge/


## Slide 17

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
17
Strain Gauge/Gage
Applications
•
Structural monitoring – measure stress or deformation in bridges, 
buildings, and aircraft structures.
•
Weight measurement – kitchen weight scale
•
Robotics – sense applied forces or joint motion
•
Biomedical devices – detect muscle movement or mechanical strain in 
wearable sensors
Right Image from: Zizoua, C., et al. "Detecting muscle contractions using strain gauges." Electronics Letters 52.22 (2016): 1836-1838.
Torque Sensor


## Slide 18

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
18
Strain Gauge/Gage
How to read strain gauge – simple example using voltage divider
A strain gauge can be read using a voltage divider by connecting it in 
series with a fixed resistor and applying a constant voltage; as the gauge’s 
resistance changes with strain, the output voltage changes proportionally, 
allowing measurement of strain through the voltage variation.
In the below figure, we will have – larger deformation of the strain gauge 
(stretch by larger force), larger resistance, resulting in larger output 
voltage (we can read on microcontroller).
Image from: https://www.michsci.com/what-is-a-strain-gauge/
Constant 
Resistance
Output
Voltage
Input
Voltage


## Slide 19

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
19
Strain Gauge/Gage
Influence of Temperature
Temperature affects strain gauges because it can change both the 
material’s resistance and the substrate’s dimensions, causing 
measurement errors unrelated to actual strain.
When temperature increase, strain gauge also has increased resistance.
To reduce the influence of temperature:
•
Using temperature-compensated strain gauges – made with materials 
whose thermal expansion and resistivity match the test specimen.
•
Wheatstone bridge configuration – where adjacent gauges experience 
the same temperature but opposite strain, canceling thermal drift.
•
Adding dummy gauges – unstrained but exposed to the same 
temperature, to correct for temperature-induced resistance changes.
Image from: https://www.michsci.com/what-is-a-strain-gauge/


## Slide 20

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
20
Strain Gauge/Gage
Other Factors of Influence
•
Temperature – affects material properties, resistance, and electronic behavior.
•
Humidity – can alter insulation, capacitance, or cause corrosion.
•
Mechanical vibration or shock – introduces noise or shifts sensor alignment.
•
Electromagnetic interference (EMI) – distorts signals in wired or electronic 
sensors. Especially for long wires and wires near motors.
•
Aging and wear – sensor materials and components degrade over time.
•
Environmental contamination – dust, oil, or light interference affects 
readings.


## Slide 21

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
21
Load Cell
A load cell is a transducer that converts applied force or weight into an 
electrical signal, typically using strain gauges to detect minute 
deformations in a mechanical structure.
Image from: https://www.anyload.com/how-does-a-load-cell-work/


## Slide 22

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
22
How Load Cell Works (Optional)
In a load cell, a Wheatstone Bridge precisely measures small resistance 
changes from strain gauges by balancing four resistive arms, producing a 
differential voltage proportional to the applied load.
Wheatstone Bridge is used because it amplifies sensitivity to small 
resistance changes, provides temperature compensation, and allows 
accurate differential voltage measurement
Image from: https://www.anyload.com/how-does-a-load-cell-work/
Wheatstone Bridge


## Slide 23

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
23
Load Cell
Direction of Measurement and Overload
Load cell can only measure the force that is perpendicular it. In application, 
we should ensure that the force that we want to measure is applied 
perpendicularly on the load cell.
Most of sensors have working range. Overloading the sensor may cause
permanent damage to the sensor.
Image from: https://www.anyload.com/how-does-a-load-cell-work/
Force
Force


## Slide 24

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
24
Load Cell Platform
The load cell platform is a simple application of load cell, which can measure 
weight. 
The HX711 is a analog-to-digital converter (ADC) specifically designed for 
load cells and strain gauges.
HX 711 ADC


## Slide 25

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
25
Load Cell
Application - Parallel Force Actuation System for Surgical Robot
A parallel robotics system controls cable tension based on load cell force 
(cable tension feedback), which can “teach” surgical robot how to sense 
external force.
Fixing 
Frame
DC
Motor
Cable 
Reel
Load 
Cell


## Slide 26

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Introduction to Sensors and Strain Gauges
26
Load Cell
Application - Parallel Force Actuation System for Surgical Robot
A parallel robotics system controls cable tension based on load cell force 
(cable tension feedback), which can “teach” surgical robot how to sense 
external force.
