## Diode I-V Characteristic Analyser

A command-line Python program that calculates and plots diode current-voltage characteristics using the Shockley diode equation.

### Features

- Analyse a silicon or germanium diode.
- Adjust saturation current, ideality factor, and temperature.
- Calculate current at a chosen voltage, the 1 mA knee voltage, and static and dynamic resistance.
- Plot forward and reverse characteristics, compare silicon with germanium, and compare several temperatures.

### Requirements

- Python 3
- NumPy
- Matplotlib

Install the libraries with:

```bash
python -m pip install numpy matplotlib
```

### Run

```bash
python diode_iv_analyser.py
```

Follow the prompts to enter diode parameters and voltage ranges. The program prints calculated values and opens the plots in Matplotlib windows.
