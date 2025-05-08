import subprocess

def run_main_program():
    # Run the main script that generates the text file
    print("Running depth and slope analysis...")
    subprocess.run(["python", "stereo_depth.py"], check=True)
    print("Analysis complete.\n")

def extract_depth_and_slope(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        depth_line = lines[0]
        slope_line = lines[1]

        # Parse values
        depth = float(depth_line.strip().split(":")[1].split()[0])
        slope = float(slope_line.strip().split(":")[1].split()[0])

        return depth, slope

def main():
    report_file = "depth_slope_report.txt"

    # Step 1: Run the analysis script
    run_main_program()

    # Step 2: Extract the values
    depth, slope = extract_depth_and_slope(report_file)
    print(f"Extracted depth: {depth:.2f} meters")
    print(f"Extracted slope: {slope:.2f} degrees")

    # Step 3: Example logic using the values
    if slope > 30:
        print("⚠️  Warning: Steep slope detected!")
    else:
        print("✅ Slope is within normal range.")

if __name__ == "__main__":
    main()
