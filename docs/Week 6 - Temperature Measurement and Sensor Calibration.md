# Week 6 - Temperature Measurement and Sensor Calibration

## Slide 1

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
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
Temperature Measurement and Sensor Calibration
2
Last Week - Strain Gauge/Gage
A strain gauge is a sensor that measures deformation (strain) in an object 
by detecting changes in its resistance when stretched or compressed.
When it is stretched, its length increases and cross-sectional area 
decreases, both of which increase resistance. (The road is longer but ) 
Conversely, when it is compressed, the length shortens, area increases, and 
resistance decreases
Image from: https://www.michsci.com/what-is-a-strain-gauge/


## Slide 3

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
3
Last Week - Load Cell
A load cell is a transducer that converts applied force or weight into an 
electrical signal, typically using strain gauges to detect minute 
deformations in a mechanical structure.
Image from: https://www.anyload.com/how-does-a-load-cell-work/


## Slide 4

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
4
Last Week - Sensor Types
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


## Slide 5

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
5
Temperature Sensing
Temperature measurements are commonly used in many systems:
•
Refrigerators and ovens – maintain precise cooling or heating levels.
•
Wearable health monitors – measure body or skin temperature 
continuously.
•
Autonomous vehicles and drones – track battery and component 
temperature.


## Slide 6

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
6
History of Temperature Sensing
1600s - A Galileo thermometer is a thermometer made of a 
sealed glass cylinder containing a clear liquid and several 
glass vessels of varying density. The individual floats rise or 
fall in relation to their respective density and the density of the 
surrounding liquid as the temperature changes.
1700s - mercury thermometer is a thermometer that uses the 
thermal expansion and contraction of liquid mercury to indicate 
the temperature.
Definition and image from Wikipedia: https://en.wikipedia.org/wiki/Galileo_thermometer


## Slide 7

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
7
Thermistor and Digital Temperature Sensing
In order to sense temperature for digital systems, we generally need to convert 
temperature information first to electrical analog signal, then to digital signal.
Resistance
Temperature
Voltage
Number


## Slide 8

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
8
Thermistor – Temperature to Resistance
A thermistor is a type of resistor whose electrical resistance is highly dependent 
on temperature. It works by changing its resistance in response to temperature 
changes, with either positive or negative relation.
NTC-MF52-103 Thermistor
NTC (negative‐temperature‐coefficient) thermistors
are typically made from a sintered ceramic or 
metal‐oxide semiconductor material. 
When temperature increase, more charge carriers 
become available in the material, which reduces its 
resistance.


## Slide 9

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
9
Thermistor – Resistance to Voltage 
We can use voltage divider (details in week 2) to convert thermistor’s change in 
resistance into change in voltage.
Constant 
Resistance
Output
Voltage
Input
Voltage


## Slide 10

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
10
Thermistor – Voltage to Number
We can use analog to digital converter (ADC) and/or microcontroller to read analog 
voltage and convert it into a number that represents the temperature. 
Voltage
Number


## Slide 11

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
11
Thermistor – Example
NTC-MF52-103 thermistor has a relationship between temperature and resistance:
𝑇= a ∙ln 𝑅+ 𝑏
where R is the resistance and T is the temperature. a and b are constants.
Assume we have measured the thermistor’s resistance 
Temperature (°C)
Resistance (Ohm)
ln(R)
0
33600
10.42
20
12100
9.40
100
1280
7.15
We can use linear regression to find a and b, then:
𝑇= −30.6 ln 𝑅+ 318.7


## Slide 12

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
12
Thermistor – Example
NTC-MF52-103 thermistor has a relationship between temperature and resistance:
𝑇= a ∙ln 𝑅+ 𝑏
where R is the resistance and T is the temperature. a and b are constants.
(This is a linear approximation, for better accuracy, please check Steinhart–Hart 
equation)
To find the relation, we need several reference points from accurate resource
(such as ice as 0 °C, boiling water as 100 °C) 
Assume we have measured the thermistor’s resistance: 
Temperature (°C)
Resistance (Ohm)
ln(R)
0
33600
10.42
20
12100
9.40
100
1280
7.15
We can use linear regression to find a and b:
𝑇= −30.6 ln 𝑅+ 318.7


## Slide 13

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
13
Thermistor – Example
We can then use a voltage divider to convert the resistance change into voltage 
change
According to series resistors, we have:
𝑉𝑜𝑢𝑡=
𝑅
𝑅+10000 ∙3.3
Solve for R, we have:
𝑅= 10000𝑉𝑜𝑢𝑡
(3.3 −𝑉𝑜𝑢𝑡)
Input Voltage
3.3V
Vout
10k(Ω)
R (Ω)


## Slide 14

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
14
Thermistor – Example
We can then use microcontroller such as ESP32 to read the analog voltage from 
the previous voltage divider.
from analogio import AnalogIn
from board import A0
raw_reading = AnalogIn(A0) 
However, the analog read function will not directly give the voltage in the value of volt. 
Instead, it is representing 0-3.3V (or other reference voltages) as integers from 0-65535 (12 
bits). So we will get the voltage by:
𝑉𝑜𝑢𝑡=
3.3
65535 ∙𝑟𝑎𝑤


## Slide 15

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
15
Thermistor – Transfer Function Calibration
Transfer Function Calibration is the process of determining the mathematical 
relationship between a sensor’s raw output and the actual physical quantity, 
allowing accurate conversion from digital readings to real-world values.
To sum up, we have the pipeline of how to use thermistor to convert temperature 
information to a number in a microcontroller. 
In contrast, if we get a raw reading from the microcontroller, we can also convert it 
into a value of temperature.
Resistance
Temperature
Voltage 
(analog)
Number 
(digital voltage)


## Slide 16

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
16
Transfer Function Calibration - Example
If we have a raw reading in the microcontroller to be 30000, what is the 
temperature?
Recall that:
From raw reading to voltage:
𝑉𝑜𝑢𝑡=
3.3
65535 ∙𝑟𝑎𝑤
From voltage to resistance:
𝑅= 10000𝑉𝑜𝑢𝑡
(3.3 −𝑉𝑜𝑢𝑡)
From resistance to temperature:
𝑇= −30.6 ln 𝑅+ 318.7


## Slide 17

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
17
Transfer Function Calibration - Example
If we have a raw reading in the microcontroller to be 30000, what is the 
temperature?
Recall that:
From raw reading to voltage:
𝑉𝑜𝑢𝑡=
3.3
65535 ∙𝑟𝑎𝑤= 𝟏. 𝟓𝟏𝑽
From voltage to resistance:
𝑅= 10000𝑉𝑜𝑢𝑡
(3.3 −𝑉𝑜𝑢𝑡) = 𝟖𝟒𝟑𝟓. 𝟕𝜴
From resistance to temperature:
𝑇= −30.6 ln 𝑅+ 318.7 = 𝟒𝟐. 𝟏℃


## Slide 18

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
18
One Wire Temperature Sensor - DS18B20
The DS18B20 is a digital temperature sensor that provides highly accurate temperature 
readings through the One-Wire communication protocol, requiring only a single data line 
for connection.
It offers a measurement range of −55 °C to +125 °C with up to 0.0625 °C resolution, making 
it ideal for IoT, environmental monitoring, and embedded systems.
Inside the sensor, a silicon diode changes predictably with temperature — its forward 
voltage decreases by about 2 mV per °C — and the DS18B20 measures this voltage 
change electronically, then converts it into a precise digital temperature reading through its 
internal circuit.


## Slide 19

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
19
Adjustment Calibration (Error Compensation)
In real practice, sensor readings generally has errors. We can test the 
characteristics of the error and make compensation. This is called adjustment 
calibration. 
For example, if a temperature sensor always reads 5 °C on ice and 105 °C on 
boiling water, it has a bias of + 5 °C. We can simply add - 5 °C to all sensor 
readings to compensate the bias.
Image from: https://www.dracal.com/en/calibration-or-adjustment/


## Slide 20

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
20
Adjustment Calibration (Error Compensation)
Common types of error in sensors include:
Bias (Offset) Error – the output is consistently higher or lower than the true value 
by a fixed amount. For example, sensor reads are always 5 °C more.
Scale (Gain) Error – the slope of the sensor’s response differs from the ideal; 
readings change proportionally but incorrectly. For example, sensor reads are 
always 1.2 times larger.
For these two type of error, we can use linear regression to compensate.
Resistance
Temperature


## Slide 21

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
21
Adjustment Calibration (Error Compensation)
Nonlinearity – the output does not follow a straight line relative to the input across 
the measurement range.
Conventionally, we can use polynomial regression, piecewise linear calibration, 
and lookup table to compensate. If the Nonlinearity is very complex, we can also 
train a neural network for compensation.
Left image from: https://www.dracal.com/en/calibration-or-adjustment/,
Right image from: Peng, Haonan, et al. "Efficient data-driven joint-level calibration of cable-driven surgical robots." npj Robotics 2.1 (2024): 1-16.


## Slide 22

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
22
Adjustment Calibration (Error Compensation)
Drift – slow change in sensor output over time, even when the true input is constant. 
For example, the sensor reads + 1 °C per hour (reads 1 °C after 1 hour, 2 °C after 2 
hour, et cetera).
If the drift is linear with time, we can use linear regression. Otherwise, we should 
consider nonlinear compensation, such as polynomial regression.
Figure from: Peng, Haonan, et al. "Efficient data-driven joint-level calibration of cable-driven surgical robots." npj Robotics 2.1 (2024): 1-16.
Time (hour)


## Slide 23

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
23
Adjustment Calibration (Error Compensation)
Noise – random fluctuations in the output due to electrical or environmental 
interference.
To compensate for noise, we usually need to apply filters (refer to week 7 slides).


## Slide 24

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Temperature Measurement and Sensor Calibration
24
Adjustment Calibration (Error Compensation)
Cross-Sensitivity – the sensor responds unintentionally to other variables (e.g., 
temperature affecting pressure readings).
To compensate for cross-sensitivity, we can use multivariable calibration, dummy 
sensor, or Wheatstone bridges (refer to week 5 slides).
