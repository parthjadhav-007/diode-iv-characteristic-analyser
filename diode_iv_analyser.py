import numpy as np
import matplotlib.pyplot as plt

k = 1.380649e-23      
q = 1.602176634e-19   

print("=" * 55)
print("       DIODE I-V CHARACTERISTIC ANALYSER")
print("=" * 55)


choice = int(input("Enter 1 for Silicon diode or 2 for Germanium diode: "))

if choice == 1:
    name = "Silicon"
    Is300 = 1e-12      
    Eg = 1.12          
elif choice == 2:
    name = "Germanium"
    Is300 = 1e-6
    Eg = 0.66
else:
    print("Error: please enter only 1 or 2.")
    raise SystemExit

text = input("Saturation current at 300 K in A (press Enter to use %.0e): " % Is300)
if text != "":
    Is300 = float(text)

n = float(input("Ideality factor, between 1 and 2 (e.g. 1): "))
T = float(input("Temperature in degree C (e.g. 27): "))
Vf_max = float(input("Maximum forward voltage to plot in V (e.g. 0.8): "))
Vr_max = float(input("Maximum reverse voltage to plot in V (e.g. 10): "))
Vtest = float(input("Voltage at which to calculate the current in V (e.g. 0.65): "))

if Is300 <= 0 or n <= 0 or Vf_max <= 0 or Vr_max <= 0:
    print("Error: saturation current, ideality factor and voltage limits must be positive.")
    raise SystemExit

if Vtest > 5 or Vf_max > 5:
    print("Error: forward voltages must be 5 V or less (the exponential becomes too large).")
    raise SystemExit


TK = T + 273.15
Vt = k * TK / q


Is = Is300 * (TK / 300) ** 3 * np.exp((Eg * q / (n * k)) * (1 / 300 - 1 / TK))


Vf = np.linspace(0.001, Vf_max, 500)
If = Is * (np.exp(Vf / (n * Vt)) - 1)


Vr = np.linspace(0, Vr_max, 500)
Ir = Is * (np.exp(-Vr / (n * Vt)) - 1)


I_test = Is * (np.exp(Vtest / (n * Vt)) - 1)


V_knee = n * Vt * np.log(1e-3 / Is + 1)

print()
print("=" * 55)
print("RESULTS for", name, "diode at", T, "C")
print("=" * 55)
print("Thermal voltage (Vt)            : %.5f V" % Vt)
print("Saturation current at %.1f C    : %.3e A" % (T, Is))
print("Voltage for 1 mA (knee voltage) : %.3f V" % V_knee)
print()
print("At V = %.3f V:" % Vtest)
print("   Current                      : %.4e A" % I_test)

if I_test != 0:
    R_static = Vtest / I_test
    
    slope = Is / (n * Vt) * np.exp(Vtest / (n * Vt))
    r_dynamic = 1 / slope
    print("   Static resistance (V/I)      : %.4g ohm" % R_static)
    print("   Dynamic resistance (dV/dI)   : %.4g ohm" % r_dynamic)


plt.figure("Graph 1 - Diode characteristics", figsize=(14, 4.5))

plt.subplot(1, 3, 1)
plt.plot(Vf, If * 1000, color="blue")
ymax = 50
if Vtest > 0 and Vtest <= Vf_max:
    plt.plot(Vtest, I_test * 1000, "ro", label="V = %.2f V" % Vtest)
    plt.legend()
    if I_test * 1000 > 50:
        ymax = I_test * 1000 * 1.2    
plt.ylim(0, ymax)
plt.xlabel("Forward voltage (V)")
plt.ylabel("Current (mA)")
plt.title("Forward bias (linear)")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.semilogy(Vf, If, color="purple")
plt.xlabel("Forward voltage (V)")
plt.ylabel("Current (A, log scale)")
plt.title("Forward bias (log scale)")
plt.grid(True, which="both")

plt.subplot(1, 3, 3)
plt.plot(-Vr, Ir, color="red")
plt.xlabel("Reverse voltage (V)")
plt.ylabel("Current (A)")
plt.title("Reverse bias (leakage current)")
plt.grid(True)

plt.tight_layout()


names = ["Silicon", "Germanium"]
Is_list = [1e-12, 1e-6]
Eg_list = [1.12, 0.66]
colors = ["blue", "orange"]

print()
print("-" * 55)
print("SILICON vs GERMANIUM (n = %.2f, T = %.1f C)" % (n, T))
print("-" * 55)

plt.figure("Graph 2 - Silicon vs Germanium", figsize=(8, 5))

for i in range(2):
    Is_x = Is_list[i] * (TK / 300) ** 3 * np.exp((Eg_list[i] * q / (n * k)) * (1 / 300 - 1 / TK))
    Vx = np.linspace(0.001, 1.0, 500)
    Ix = Is_x * (np.exp(Vx / (n * Vt)) - 1)
    knee_x = n * Vt * np.log(1e-3 / Is_x + 1)
    print("%-10s knee voltage (1 mA): %.3f V" % (names[i], knee_x))
    plt.plot(Vx, Ix * 1000, color=colors[i], label="%s (knee = %.2f V)" % (names[i], knee_x))

plt.ylim(0, 50)
plt.xlim(0, 1.0)
plt.xlabel("Forward voltage (V)")
plt.ylabel("Current (mA)")
plt.title("Silicon vs Germanium diode")
plt.grid(True)
plt.legend()
plt.tight_layout()


print()
print("-" * 55)
print("EFFECT OF TEMPERATURE on the %s diode" % name)
print("-" * 55)
print("Temp (C)    Is (A)         Voltage for 1 mA (V)")

plt.figure("Graph 3 - Effect of temperature", figsize=(8, 5))

for Tx in [0, 25, 50, 75, 100]:
    TKx = Tx + 273.15
    Vt_x = k * TKx / q
    Is_x = Is300 * (TKx / 300) ** 3 * np.exp((Eg * q / (n * k)) * (1 / 300 - 1 / TKx))
    Vx = np.linspace(0.001, Vf_max, 500)
    Ix = Is_x * (np.exp(Vx / (n * Vt_x)) - 1)
    knee_x = n * Vt_x * np.log(1e-3 / Is_x + 1)
    print("%5d      %.3e      %.3f" % (Tx, Is_x, knee_x))
    plt.plot(Vx, Ix * 1000, label="%d C" % Tx)

plt.ylim(0, 50)
plt.xlabel("Forward voltage (V)")
plt.ylabel("Current (mA)")
plt.title("%s diode at different temperatures" % name)
plt.grid(True)
plt.legend()
plt.tight_layout()

print()
print("Close the graph windows to end the program.")
plt.show()
