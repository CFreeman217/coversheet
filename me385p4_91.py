import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
num = [3]
den = [10, 0, 180, 0, 540]

sys = signal.TransferFunction(num, den)
t = np.linspace(0, 30, 250)
time, imp = signal.impulse(sys, T=t)

plt.plot(time, imp)
plt.title('Problem 4.91c Unit Impulse Response Plot')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.savefig('me385p4_91plot.png', bbox_inches='tight')
plt.show()

