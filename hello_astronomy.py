import numpy as np
import matplotlib.pyplot as plt

# Simulated observations of a variable star
time = np.linspace(0, 10, 200)
brightness = 10 + 0.5 * np.sin(2 * np.pi * time / 3)

plt.plot(time, brightness)
plt.xlabel("Time (days)")
plt.ylabel("Relative brightness")
plt.title("Simulated Variable Star Light Curve")
plt.grid(True)
plt.show()