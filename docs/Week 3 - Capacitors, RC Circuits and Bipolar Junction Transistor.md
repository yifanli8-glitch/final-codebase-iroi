# Week 3 - Capacitors, RC Circuits and Bipolar Junction Transistor

## Slide 1

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
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
RC Circuits and BJTs
2
Last Week - Ohm’s Law
In a closed circuit, for each resistor, we have:
𝐼= 𝑉
𝑅
Where I is the current go through it, V is the voltage across it, and R is the resistance.
I =0.5A
10 Ω
5 V


## Slide 3

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
3
Last Week - Series VS Parallel Resistors
Series Resistors
•
Same current
•
Different voltage
•
Larger resistance (sum)
400 Ω
8V
Parallel Resistors
•
Different current
•
Same voltage
•
Smaller resistance
+
-
+
-
+
-
+
-


## Slide 4

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
4
Week 3 – RC Circuits and BJTs
•
Capacitors
•
Resistor–Capacitor Circuit (RC circuit)
•
Bipolar Junction Transistor (BJT)


## Slide 5

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
5
Triboelectric Effect
Triboelectric Effect describes electric charge transfer between 
two objects when they contact or slide against each other.
From Wikipedia: https://en.wikipedia.org/wiki/Triboelectric_effect


## Slide 6

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
6
Charge
There are three particles in atoms, protons (positive charged), neutrons 
(neutral) and electrons (negative charged). 1 electron carries 1 negative 
elementary charge.
The unit of charge is coulomb (C), 1 C means ~6.24×1018 elementary charges
Electrons are matter, but charge is a representation of energy.
Like charges repel each other, and opposite charges attract each other.


## Slide 7

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
7
Capacitors and Capacitance
A capacitor is an electronic component that stores and releases 
electrical energy (charge) by accumulating opposite charges on two 
conductive plates separated by an insulator.
Capacitance is the ability of a component or system to store electric 
charge per unit voltage, the unit is farads (F).
1 F means that the capacitor can storage 1 C (coulomb, 6.24×1018 
charges) under 1 V (volt). 
The relation among capacitance, charge 
and voltage:
𝐶(𝑐𝑎𝑝𝑎𝑐𝑖𝑡𝑎𝑛𝑐𝑒,𝐹) =
𝑄(𝑐ℎ𝑎𝑟𝑔𝑒,𝐶)
𝑉(𝑣𝑜𝑙𝑡𝑎𝑔𝑒,𝑉)
Under the same voltage, the larger 
capacitance, the more charge can be 
stored.


## Slide 8

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
8
Capacitors and Capacitance
Farads (F) is a large unit, we will frequently see:
•
mF (milli) = 1×10-3 F
•
μF (micro) = 1×10-6 F
•
nF (nano) = 1×10-9 F
•
pF (pico) = 1×10-12 F


## Slide 9

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
9
How do capacitors work?
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


## Slide 10

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
10
Capacitor Charging and Discharging
If there are charge stored in capacitor, it can output a voltage, like battery. 
Similar to battery, we can charge and discharge capacitors:
•
Charging: connect capacitor to a voltage source so that current flows 
in and electric charge stores.
•
Discharging: connect capacitor to a circuit loop that allows current 
flow out and charge released from the capacitor.
Charging
Discharging


## Slide 11

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
11
Capacitor VS Battery
Capacitor
•
stores energy electrostatically
(like spring pressed, same energy)
•
low energy capacity
•
Applications: filtering, timing, 
energy buffering
Battery
•
stores energy chemically
(different energy)
•
high energy capacity
•
Applications: long-term 
energy supply and portable 
power


## Slide 12

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
12
Basic Resistor–Capacitor (RC) Circuit
A basic resistor–capacitor (RC) circuit is a simple network where a 
resistor and capacitor are connected together, allowing the capacitor to 
charge or discharge through the resistor over time, creating an 
exponential voltage change.
1) At beginning (only this moment), once 
switch closed, the capacitor begins to 
charge and has no voltage across it (like a 
wire), and current is I=V/R
2) During charging, the charge and 
voltage of capacitor increase, and the 
current decrease.
3) After fully charged, the voltage of the 
capacitor is equal to the power supply, 
and the current is 0.


## Slide 13

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
13
Basic Resistor–Capacitor (RC) Circuit
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


## Slide 14

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
14
Basic Resistor–Capacitor (RC) Circuit
Example
Given the power supply 5V, and the resistor and capacitor as the following 
figure shows. Find the time constant of this RC circuit. Assuming the switch 
is closed at t=0, when will the voltage of the capacitor reach 2.5V? (τ=RC)
Transient Period


## Slide 15

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
15
Basic Resistor–Capacitor (RC) Circuit
Example
Given the power supply 5V, and the resistor and capacitor as the following 
figure shows. Find the time constant of this RC circuit. Assuming the switch 
is closed at t=0, when will the voltage of the capacitor reach 2.5V? (τ=RC)
Solution:
First time constant is 
τ = RC = 10kΩ x 100μF = 1x104Ω x 1x10-4F = 1s
When t = 0.7τ = 0.7s, the capacitor is 50% 
charged 2.5V.
Transient Period


## Slide 16

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
16
Discharging of Capacitor in RC Circuits 
Discharging in a basic resistor–capacitor (RC) circuit occurs when the 
stored energy in the capacitor is released through the resistor, causing the 
voltage across the capacitor to decrease exponentially over time.
1) At beginning (only this moment), once 
switching, the capacitor begins to 
discharge and has voltage equal to 
power supply U, and current is I=V/R
2) During discharging, the charge and 
voltage of capacitor decrease, and the 
current decrease.
3) After fully discharged, the voltage of 
the capacitor is 0, and the current is 0.


## Slide 17

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
17
Discharging of Capacitor in RC Circuits 
Once the switch is closed (circuit powered) and the 
discharging begins, the voltage across the capacitor is 
shown in this figure. 
And the τ=RC is called the time constant of this RC circuit
After switching, 0 - 4τ is called 
the transient period. And after 
4τ, the circuit enters steady 
state period as the capacitor is 
98% charged and the 
characteristic of the circuit merely 
changes with time.
Transient Period


## Slide 18

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
18
Steady-state Analysis VS Transient Analysis
Steady-state analysis examines a circuit’s behavior after all transient 
effects have settled, while transient analysis studies how the circuit 
responds and changes during the period immediately after a disturbance or 
switching event.
I =0.5A
Do NOT 
change over time
Change over time


## Slide 19

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
19
Euler's number “e” (optional)
Assume I have $N loan and 100% annual simple interest, after one year, I 
need to repay:
𝑀= 𝑁∗1 + 100% = 2𝑁
In contrast, if we have compound interest with frequency of 3, after one 
year, I need to repay:
𝑀= 𝑁∗1 + 100%
3
3
= 2.37𝑁
Finally, if we have compound interest with infinite frequency, after one 
year, I need to repay:
𝑀= 𝑁∗lim
𝑛→∞1 + 100%
𝑛
𝑛
≈2.718𝑁≈𝑒∗𝑁
The constant number 𝒆≈𝟐. 𝟕𝟏𝟖, is called Euler's number, the base of the 
natural logarithm and exponential function.
It can be seen that ‘e’ represents the natural law of continuous 
increase. Unlike number ‘10’ or ‘100’ which are defined logarithm bases for 
convenience, ‘e’ is discovered.


## Slide 20

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
20
Ordinary Differential Equation (ODE) (optional)
https://www.youtube.com/watch?v=BjvkBLfvkqY
The voltages in the in RC circuit is:
U = 𝑅𝐼+ 𝑉𝑐= 𝑅𝐶
𝑑𝑉𝑐
𝑑𝑡+ 𝑉𝑐
The only unknown variable in (1) is the voltage across the capacitor Vc.  
This is an ordinary differential equation (ODE). The solution of this ODE is:
𝑉𝑐= 𝑈(1 −𝑒−1
𝑅𝐶𝑡)
Solving ODE can be useful in engineering analysis and not very difficult. If 
you want to know more, there is a series of videos from Prof. Steve Brunton 
of UW ME. (https://www.youtube.com/watch?v=BjvkBLfvkqY)


## Slide 21

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
21
Ordinary Differential Equation (ODE) (optional)
Example –Cooling Coffee
Do you observe that for fresh brewed hot coffee, we do not need to wait for 
long time until it is drinkable (i.e. cooling from 90 °C (𝑇0) to 55 °C), but it will 
wait for much longer time until the coffee is room temperature (i.e. cooling 
from 55 °C to 20 °C (𝑇𝑟𝑜𝑜𝑚))?
By Newton’s law of cooling, the speed of cooling can be computed by:
𝑑𝑇𝑐𝑜𝑓
𝑑𝑡
= −𝑘𝑇𝑐𝑜𝑓−𝑇𝑟𝑜𝑜𝑚
Where k is the cooling rate constant depends on factors like surface area, 
air flow, cup material


## Slide 22

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
22
Ordinary Differential Equation (ODE) (optional)
Example –Cooling Coffee
90 °C
20 °C
55 °C
Time
If we solve this ODE, we have:
𝑇𝑐𝑜𝑓(𝑡) = 𝑇0 −𝑇𝑟𝑜𝑜𝑚𝑒−𝑘𝑡
If we plot this out, we can find out that it is similar to capacitor discharging
𝑉𝑐(𝑡) = 𝑈𝑒−1
𝑅𝐶𝑡


## Slide 23

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
23
Transistors
A transistor is a semiconductor device used to amplify or switch 
electrical signals and power. It is one of the basic building blocks of 
modern electronics (from Wikipedia).
•Smartphones and computers – millions of transistors form processors 
and memory chips.
•Power adapters and chargers – use transistors for voltage regulation 
and switching.
•Televisions and radios – rely on transistors for signal amplification and 
switching.
•Cars – use transistors in engine control units, sensors, and infotainment 
systems.


## Slide 24

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
24
Diodes
A diode is an electronic component that allows current to flow in only one 
direction, acting as a one-way valve for electricity.
An ideal diode should show zero resistance if forward voltage is applied, 
and should show infinite resistance if reverse voltage is applied.
The N-type semiconductor tends to give (donate) electrons, while the 
P-type semiconductor tends to receive (accept) electrons, allowing 
current to flow when they are joined together.
(LED = light-emitting diode)
P-type
N-type
+
-
Electrons
Current


## Slide 25

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
25
Bipolar Junction Transistor (BJT)
Bipolar junction transistors (BJT)  are the first mass-produced transistors and 
are widely used in many circuits with different functions. There are two major 
types of BJT, NPN type and PNP type.
NPN BJT has 3 semiconductor pieces, 2 n-type semiconductors separated 
by 1 p-type semiconductor. The three terminals are called collector (c), 
base (b) and emitter (e). 
A small current in base (b) can control a large current flowing between 
collector (c) and emitter (e).


## Slide 26

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
26
Bipolar Junction Transistor (BJT)
Example in Lab – LED Control
If the switch is closed, there is a small current flowing into base (b), which 
allows a larger current flowing from collector (c) to emitter (e). So LED is on
c
b
e


## Slide 27

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
27
Bipolar Junction Transistor (BJT)
Example in Lab – LED Control
If the switch is open, there no current flowing into base (b), which stops 
current flowing from collector (c) to emitter (e). So LED is off.
c
b
e


## Slide 28

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
28
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
If the switch is closed, there is a small current flowing into base (b), which 
allows a larger current flowing from collector (c) to emitter (e). So LED is on.
Meanwhile, the capacitor is charged. 
c
b
e


## Slide 29

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
29
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
If the switch is opened, the capacitor begins to discharge and provide a small 
current flowing into base (b), which allows a larger current flowing from 
collector (c) to emitter (e). So LED is still on.
c
b
e


## Slide 30

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
30
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
Once the capacitor is fully discharged, it can no longer provide a small 
current flowing into base (b), which stops current flowing from collector (c) to 
emitter (e). So LED is off.
c
b
e


## Slide 31

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
31
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
When the switch is just opened and the LED is still on, 
1)
Who provides current to LED?
2)
Who provides current to the base of BJT?
c
b
e


## Slide 32

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
32
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
When the switch is just opened and the LED is still on, 
1)
Who provides current to LED? Capacitor C1.
2)
Who provides current to the base of BJT? Power supply.
c
b
e


## Slide 33

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
33
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
Why don’t we just use the capacitor to power the LED?
c
b
e


## Slide 34

University of Washington
Haonan Peng (penghn@uw.edu)
Techin 512 2025A
RC Circuits and BJTs
34
Bipolar Junction Transistor (BJT)
Example in Lab – LED Timer
Why don’t we just use the capacitor to power the LED?
Answer: Capacitor can only store a small amount of charge. If we use 
capacitor to power LED, it will dim very soon. 
But using BJT, we can use capacitor to provide small current to BJT base (b), 
while the power supply will provide large current for LED. This can last much 
longer.
