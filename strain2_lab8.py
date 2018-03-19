'''
AD623

Gain Calculation Equation
Rg = 100000/(G - 1)

Rg = 120

Gain G = 834.33

Input Offset Error (Interpolate Table 8)
201.84 uV

Total Error Referred to Input (RTI)
= Input Error + (Output Error/G)
Total Error Referred to Output (RTO)
= (Input Error × G) + Output Error 


Multimeter
Resolution 1mV @ 0.5% reading +/- 2 digits

Resistor Tolerance
350 ohm +/- 5%

Gauge Factor S = 2.13
Tolerance +/- 1.00%

E_a =  V_o (R_2 + R_3)^2 
      ---------------------
      V_e * S * R_2 * R_3i


NI 9234 DAQ System
24 bits
+/- 7.1 mV


'''