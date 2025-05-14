# external_sensor.py
import csv
from datetime import datetime

# Latest data from external sensor
rainfall_mm = 0.0
soil_saturation = 0.8  # from 0 to 1

# Open CSV and append new columns if not present (or log to a new file with matching timestamps)
filename = "landslide_data.csv"
rows = []

with open(filename, mode='r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Add new data to latest row
latest_row = rows[-1]
latest_row["Rainfall (mm)"] = f"{rainfall_mm}"
latest_row["Soil Saturation"] = f"{soil_saturation}"

# Write back updated rows (with new fieldnames)
fieldnames = list(latest_row.keys())
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("✅ External sensor data updated in CSV.")
