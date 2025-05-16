import csv
import math
import tkinter as tk
from tkinter import ttk

def compute_landslide_risk(slope, CD, CW, CO, TC,
                          beta_0= -3.5, beta_s=0.18, beta_CD=0.28,
                          beta_CW= 0.28, beta_CO=.25, beta_TC=0.5):
    linear_sum = (beta_0 +
                  (beta_s * slope) +
                  (beta_CD * CD) +
                  (beta_CW * CW) +
                  (beta_CO * (CO/180)) +
                  (beta_TC * TC))
    probalility = (logistic(linear_sum))
    return round(probalility * 100, 2)  # as percentage

def logistic(x):
    return 1 / (1 + math.exp(-x))

# Read the latest data
filename = "landslide_data.csv"
with open(filename, mode='r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    if not rows:
        raise ValueError("No data found in CSV.")

    latest = rows[-1]
    depth = float(latest["Depth (m)"])
    slope = float(latest["Slope (deg)"])
    CD = float(latest.get("Crack Density", 0))
    CW = float(latest.get("Crack Width", 0))
    CO = float(latest.get("Crack Orientation", 0))
    TC = float(latest.get("Terrain Curvature"))

    risk = compute_landslide_risk(slope, CD, CW, CO, TC,)






# Create GUI window
window = tk.Tk()
window.title("🌋 Landslide Risk Assessment")
window.geometry("600x600")

# Create labels to display the results
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), padding=10)

ttk.Label(window, text=f"Depth: {depth:.2f} m").pack()
ttk.Label(window, text=f"Slope: {slope:.2f}°").pack()
ttk.Label(window, text=f"Crack Density {CD:.1f}").pack()
ttk.Label(window, text=f"Crack Width: {CW:.2f}").pack()
ttk.Label(window, text=f"Crack Orientation: {CO:.2f}").pack()
ttk.Label(window, text=f"Terrain Curvature: {TC:.2f}").pack()

# Risk Label - Larger and Bold
ttk.Label(window, text=f"🌧️ Estimated Landslide Risk:", font=("Helvetica", 13, "bold")).pack(pady=10)
ttk.Label(window, text=f"{risk:.2f}%", font=("Helvetica", 16, "bold"), foreground="red").pack()

# Run the GUI loop
window.mainloop()
