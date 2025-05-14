import csv
import math
import tkinter as tk
from tkinter import ttk

def compute_landslide_risk(depth, slope, rainfall, saturation):
    # Replace with your actual model/formula
    risk = (depth * math.tan(math.radians(slope))) + (rainfall * 0.1) + (saturation * 50)
    return min(risk, 100)  # Cap at 100% likelihood

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
    rainfall = float(latest.get("Rainfall (mm)", 0))
    saturation = float(latest.get("Soil Saturation", 0))

    risk = compute_landslide_risk(depth, slope, rainfall, saturation)






# Create GUI window
window = tk.Tk()
window.title("🌋 Landslide Risk Assessment")
window.geometry("400x300")

# Create labels to display the results
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), padding=10)

ttk.Label(window, text=f"Depth: {depth:.2f} m").pack()
ttk.Label(window, text=f"Slope: {slope:.2f}°").pack()
ttk.Label(window, text=f"Rainfall: {rainfall:.1f} mm").pack()
ttk.Label(window, text=f"Soil Saturation: {saturation:.2f}").pack()

# Risk Label - Larger and Bold
ttk.Label(window, text=f"🌧️ Estimated Landslide Risk:", font=("Helvetica", 13, "bold")).pack(pady=10)
ttk.Label(window, text=f"{risk:.2f}%", font=("Helvetica", 16, "bold"), foreground="red").pack()

# Run the GUI loop
window.mainloop()
