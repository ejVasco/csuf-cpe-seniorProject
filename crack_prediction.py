# landslide_predictor.py
import csv
import math

def compute_landslide_risk(depth, slope, rainfall, saturation):
    # Replace with your actual model/formula
    risk = (depth * math.tan(math.radians(slope))) + (rainfall * 0.1) + (saturation * 50)
    return min(risk, 100)  # Cap at 100% likelihood

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

    print(f"📊 Depth: {depth} m | Slope: {slope}°")
    print(f"🌧️ Estimated Landslide Risk: {risk:.2f}%")
