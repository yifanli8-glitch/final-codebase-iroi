# Week 4 - Digital Circuits and 555 Timer IC

## Slide 1

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
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
Digital Circuits and 555 Timer IC
2
Last Week - Capacitors
A simple capacitor (left): two conductor plates are separated by insulator 
at a distance. When voltage is applied on the two sides of the capacitor, 
the ‘+’ side will be charged with positive charge, and the other side will be 
the same amount of negative charge.
Real capacitors (right) differ from the simple model in structure because 
their plates are rolled, stacked, or layered with thin dielectric 
materials to achieve high capacitance in a compact form.
Charges (q)
Voltage (V)
Theoretical
Practice


## Slide 3

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
3
Last Week -Basic Resistor–Capacitor Circuit
Once the switch is closed (circuit powered) and the 
charging begins, the voltage across the capacitor is shown 
in this figure. 
And the τ=RC is called the time constant of this RC circuit
After switching, 0 - 4τ is called 
the transient period. And after 
4τ, the circuit enters steady 
state period as the capacitor is 
98% charged and the 
characteristic of the circuit merely 
changes with time.
Transient Period


## Slide 4

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
4
Last Week - Bipolar Junction Transistor (BJT)
Bipolar junction transistors (BJT)  are the first mass-produced transistors and 
are widely used in many circuits with different functions. There are two major 
types of BJT, NPN type and PNP type.
NPN BJT has 3 semiconductor pieces, 2 n-type semiconductors separated 
by 1 p-type semiconductor. The three terminals are called collector (c), 
base (b) and emitter (e). 
A small current in base (b) can control a large current flowing between 
collector (c) and emitter (e).


## Slide 5

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
5
This Week
•
Analog and digital Signal
•
Logic Gates
•
555 Timer


## Slide 6

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
6
Analog Signal
An analog signal is a continuously varying electrical signal that represents 
information through smooth changes in amplitude, frequency, or phase over 
time.
Analog signals are typically used in audio, video, radio transmission, and 
sensor measurements, where information varies continuously with time.


## Slide 7

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
7
Digital Signal
A digital signal is a discrete-time signal that represents information using 
distinct levels or binary values (0s and 1s, high and low voltages) instead 
of continuous variations.
Digital signals are typically used in computers, communication systems, 
and microcontroller-based electronics, where data is processed, stored, 
and transmitted in binary form.


## Slide 8

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
8
Analog VS. Digital
Feature
Analog Signal
Digital Signal
Nature
Continuous 
Discrete 
Accuracy
Represent real-world 
signals precisely
Limited by sampling 
and quantization
Noise Sensitivity
Highly affected by noise 
and distortion
more resistant to 
noise
Signal Processing
Harder to store, 
process, or copy without 
degradation
Easy to store, 
process, and 
reproduce perfectly
Transmission Distance
Signal quality degrades 
over distance
Can be regenerated 
and transmitted long 
distances


## Slide 9

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
9
In-class Practice – Is this Analog or Digital?
If I have a micro controller plotting a sine wave on a LED screen, is that 
signal analog or digital? Why?


## Slide 10

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
10
In-class Practice – Is this Analog or Digital?
If I have a micro controller plotting a sine wave on a LED screen, is that 
signal analog or digital? Why?
That signal is digital, because the microcontroller and LED screen operate 
using discrete voltage levels (binary data) — the sine wave is only 
represented digitally by sampled points, not as a continuously varying 
voltage.
It’s an analog-looking waveform, but digitally generated and displayed
— a digital representation of an analog signal.


## Slide 11

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
11
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Brightness control using a 
dimmer knob
FM/AM radio broadcasts
Music files (MP3) stored on a 
phone
Wi-Fi or Bluetooth
communication
Images displayed on LED or 
LCD screens


## Slide 12

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
12
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Analog
Brightness control using a 
dimmer knob
FM/AM radio broadcasts
Music files (MP3) stored on a 
phone
Wi-Fi or Bluetooth
communication
Images displayed on LED or 
LCD screens


## Slide 13

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
13
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Analog
Brightness control using a 
dimmer knob
Analog
FM/AM radio broadcasts
Music files (MP3) stored on a 
phone
Wi-Fi or Bluetooth
communication
Images displayed on LED or 
LCD screens


## Slide 14

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
14
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Analog
Brightness control using a 
dimmer knob
Analog
FM/AM radio broadcasts
Analog
Music files (MP3) stored on a 
phone
Wi-Fi or Bluetooth
communication
Images displayed on LED or 
LCD screens


## Slide 15

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
15
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Analog
Brightness control using a 
dimmer knob
Analog
FM/AM radio broadcasts
Analog
Music files (MP3) stored on a 
phone
Digital
Wi-Fi or Bluetooth
communication
Images displayed on LED or 
LCD screens


## Slide 16

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
16
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Analog
Brightness control using a 
dimmer knob
Analog
FM/AM radio broadcasts
Analog
Music files (MP3) stored on a 
phone
Digital
Wi-Fi or Bluetooth
communication
Digital
Images displayed on LED or 
LCD screens


## Slide 17

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
17
In-class Practice –Analog or Digital?
Feature
Analog or Digital?
Temperature measured by a 
mercury thermometer
Analog
Brightness control using a 
dimmer knob
Analog
FM/AM radio broadcasts
Analog
Music files (MP3) stored on a 
phone
Digital
Wi-Fi or Bluetooth
communication
Digital
Images displayed on LED or 
LCD screens
Digital


## Slide 18

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
18
Analog VS Digital
Analog
Computer
Nature
Digital


## Slide 19

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
19
Analog VS Digital
Analog
Computer
Nature
Digital
Analog to Digital Converter
(ADC)
Digital to Analog Converter
(DAC)


## Slide 20

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
20
Analog to Digital Converter (ADC)
An Analog-to-Digital Converter (ADC) is a device that converts a 
continuous analog signal into a discrete digital representation that can 
be processed by digital systems like microcontrollers or computers.
PPG (Photoplethysmogram) Sensor
Blood Flow (analog)
Heart Rate (Digital)
ADC


## Slide 21

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
21
ADC – RC Circuit Charge Time 
An RC charge-time ADC works by measuring how long a capacitor takes 
to charge through a resistor until the voltage reaches a reference 
threshold; since the charge time depends on the input voltage, the 
microcontroller can convert that time measurement into a digital value
representing the analog input.


## Slide 22

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
22
ADC – Successive-Approximation ADC (Optional)
The Successive Approximation Register (SAR) ADC is the most frequently 
used type, because it offers an excellent balance of speed, accuracy, and 
power efficiency, making it ideal for most microcontroller and embedded 
applications.
A SAR ADC works by 
comparing the input voltage to 
a series of reference voltages 
generated by a digital-to-
analog converter (DAC) and 
using binary search logic to 
successively narrow down the 
digital value that best matches 
the input.
Gif from Wikipedia: https://en.wikipedia.org/wiki/Successive-approximation_ADC


## Slide 23

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
23
Digital to Analog Converter (DAC)
A DAC (Digital-to-Analog Converter) is a device that converts digital 
binary data into a continuous analog voltage or current signal.
Motor Torque Command
X Nm
(This is a number)
DAC
Motor Current Input
Y Amp
(This is an actual current)


## Slide 24

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
24
Pulse-Width Modulation (PWM)
Pulse-Width Modulation (PWM) is a technique that controls the 
average power delivered to a load by varying the width (duty) of digital 
pulses while keeping their frequency constant.
Left figure: https://en.wikipedia.org/wiki/Pulse-width_modulation
Right figure: https://timothylaux.com/project/lm386-guitar-amplifier/pwm-sine-wave/
High Duty
Low Duty


## Slide 25

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
25
PWM DAC
A PWM DAC is a simple digital-to-analog converter that uses pulse-
width modulation and a low-pass filter to generate a smooth analog 
voltage proportional to the PWM duty cycle.
Input
Output


## Slide 26

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
26
Key Metrics of ADC and DAC
•
Resolution – number of bits (e.g., 8-bit, 12-bit, 16-bit) determining 
smallest voltage step
•
Sampling Rate (ADC) / Update Rate (DAC) – how fast it converts 
samples per second
•
Linearity – how closely output follows an ideal straight line; measures 
accuracy
•
Noise / Signal-to-Noise Ratio – measures precision and cleanliness 
of conversion


## Slide 27

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
27
Logic Gate
A logic gate is a basic digital circuit that performs a logical operation 
(such as AND, OR, or NOT) on one or more binary inputs to produce a 
single binary output.


## Slide 28

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
28
Logic Gate – Buffer and NOT
Input
Output
A
Q
0
0
1
1
Buffer
(Repeat the same voltage)
Python: if A
Input
Output
A
Q
0
1
1
0
NOT
(Inverter)
Python: if not A
Figure, tables from Wikipedia: https://en.wikipedia.org/wiki/Logic_gate


## Slide 29

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
29
Logic Gate – AND / OR
AND
Python: if A and B
OR
Python: if A or B
Figure, tables from Wikipedia: https://en.wikipedia.org/wiki/Logic_gate
Input
Output
A
B
Q
0
0
0
0
1
0
1
0
0
1
1
1
Input
Output
A
B
Q
0
0
0
0
1
1
1
0
1
1
1
1
Only output true when both 
inputs are true
Only output false when both 
inputs are false


## Slide 30

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
30
Logic Gate – NAND
Figure, tables from Wikipedia: https://en.wikipedia.org/wiki/Logic_gate
AND
Python: if A and B
Input
Output
A
B
Q
0
0
0
0
1
0
1
0
0
1
1
1
NAND
Python: if not (A and B)
Input
Output
A
B
Q
0
0
1
0
1
1
1
0
1
1
1
0


## Slide 31

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
31
Logic Gate – NOR
Figure, tables from Wikipedia: https://en.wikipedia.org/wiki/Logic_gate
OR
Python: if A or B
Input
Output
A
B
Q
0
0
0
0
1
1
1
0
1
1
1
1
NOR
Python: if not (A or B)
Input
Output
A
B
Q
0
0
1
0
1
0
1
0
0
1
1
0


## Slide 32

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
32
Logic Gate – XOR
Figure, tables from Wikipedia: https://en.wikipedia.org/wiki/Logic_gate
XOR
(Exclusive OR)
Python: 
if (a and not b) or (not a and b)
Input
Output
A
B
Q
0
0
0
0
1
1
1
0
1
1
1
0
Only output true when A and 
B are different


## Slide 33

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
33
In-class Practice
For the following logic circuit, given the input, what will be the output (0 or 1) 
of each logic IC, and why? (5 points each)


## Slide 34

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
34
In-class Practice
For the following logic circuit, given the input, what will be the output (0 or 1) 
of each logic gate, and why? (5 points each)
①NOT Gate: Input: 1 - Output: 0
②OR Gate: Input: (1, 1) - Output: 1
③AND Gate: Input: (0, 0) - Output: 0
④NAND Gate: Input: (1, 0) - Output: 1


## Slide 35

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
35
Integrated circuit (IC)
An integrated circuit (IC) is a compact electronic device that combines 
multiple components and connections such as transistors, resistors, and 
capacitors on a single semiconductor chip to perform complex functions.


## Slide 36

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
36
555 Timer – Motivation
If we want to build a circuit that will turn on the LED for 10 
seconds once we press a button? We do not want to keep 
pressing the button. 
?


## Slide 37

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
37
555 Timer
The 555 timer IC is an integrated circuit used in a variety of timer, delay, 
pulse generation, and oscillator applications. It is one of the most popular 
timing ICs due to its flexibility and price. [1]
It was invented in 1971 by Hans R. Camenzind while working for Signetics. 
The design was completed in just two weeks, and it became one of the most 
successful ICs ever made (more than one billion units sold).
The name “555” came from the three 5 kΩ resistors used in its internal 
voltage divider.
[1] Wikipedia: https://en.wikipedia.org/wiki/555_timer_IC
Camenzind noted in 1997 that “9 out of 10 of its 
applications were in areas and ways I had never 
contemplated. For months I was inundated by phone 
calls from engineers who had new ideas for using the 
device."


## Slide 38

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
38
555 Timer – How to locate pins
Most IC chips use a small a dot, notch, or bevel to label point 1 or top. Then 
the pins are numbered counter clock-wise when looking top down.
[1] Wikipedia: https://en.wikipedia.org/wiki/555_timer_IC
Top
Top
Pin 1 (GROUND)


## Slide 39

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
39
555 Timer – Functions of Pins
•
Pin 1 (GND): Connects to the negative (ground) supply.
•
Pin 2 (TRIG): Trigger input; starts timing when voltage drops below 1/3 Vcc.
•
Pin 3 (OUT): Output pin; goes high or low depending on timing state.
•
Pin 4 (RESET): Resets the timer when pulled low (active low).
•
Pin 5 (CTRL V): Control voltage; adjusts threshold (usually connected to 
ground through a 0.01 µF capacitor).
•
Pin 6 (THRESH): Threshold input; ends timing when voltage exceeds 2/3 Vcc.
•
Pin 7 (DISCH): Discharge pin; connected to timing capacitor to control 
charge/discharge.
•
Pin 8 (Vcc): Positive power supply (typically +5 V to +15 V).


## Slide 40

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
40
555 Timer – Inside
A 555 Timer IC consists of: 3X 5kΩ resistors, 1 bipolar junction transistor 
(BJT), 2 operational amplifier, one flip-flop (multiple logic gates), and an 
output driver (for stronger output). The timing function also need external 
capacitors.
[1] Image from: https://www.electronics-tutorials.ws/waveforms/555_timer.html
Operational amplifier


## Slide 41

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
41
555 Timer – Monostable Mode
In monostable mode, the 555 timer produces a single output pulse of 
fixed duration each time it is triggered, with the pulse width determined by 
an external resistor and capacitor. The output duration is determined by:
𝑡= ln 3 ∙𝑅∙𝐶
Figure from Wikipedia: https://en.wikipedia.org/wiki/555_timer_IC
Negative (or active-low) pulse
Input (trigger)
Output


## Slide 42

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
42
555 Timer - Motivation
If we want to build a circuit that will turn on the LED for 10 seconds once we 
press a button? 
We can use 555 Timer in monostable mode.
Applications also include: automatic light or fan delay, camera flash timers
555 Timer 
Monostable Mode


## Slide 43

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
43
555 Timer - Motivation
If we want to blink LED with a controllable frequency and 
duty, how can we do it? Assuming the size and cost of 
microcontroller or signal generator is not acceptable.
?


## Slide 44

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
44
555 Timer – Astable Mode
In astable mode, the 555 timer continuously charges and discharges a 
capacitor, producing a repeating square wave output whose frequency and 
duty cycle are set by external resistors and a capacitor. In this mode, external 
trigger is not needed.
Figure from Wikipedia: https://en.wikipedia.org/wiki/555_timer_IC
The frequency f of the output pulse is determined by:
𝑓=
1
ln(2) ∙𝑅1 + 2𝑅2 ∙𝐶
And the duty is determined by:
𝐷𝑢𝑡𝑦(%) = 𝑅1 + 𝑅2
𝑅1 + 2𝑅2
∙100
In astable mode, the 555 timer works like 
an oscillator, rather than a timer.


## Slide 45

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
Digital Circuits and 555 Timer IC
45
555 Timer – Astable Mode
In astable mode, the 555 timer works like an oscillator that outputs pulses with 
controllable frequency and duty.
Applications include
Doorbells – create sound tones and modulated signals.
Flashing bicycle lights – use 555 as LED blinkers
Clock pulses for digital circuits
Figure from Wikipedia: https://en.wikipedia.org/wiki/555_timer_IC
555 Timer 
Astable Mode
