from gpiozero import DigitalInputDevice
import time
import requests
import csv
import os
from datetime import datetime

# --- ThingSpeak Setup ---
# Replace 'YOUR_API_KEY' with your actual Write API Key
API_KEY = "YOUR_API_KEY"
URL = "https://api.thingspeak.com/update"

# --- Hardware Setup ---
sensor = DigitalInputDevice(4) # MQ-135 on GPIO 4

# --- CSV File Setup ---
csv_filename = "air_quality_log.csv"
file_exists = os.path.isfile(csv_filename)

with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Timestamp", "Air_Quality_Status", "Description"])

print("=========================================")
print("  Cloud Air Quality Monitoring Started   ")
print("=========================================")
print("Press Ctrl+C to stop.")

try:
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Read the Sensor
        if sensor.is_active:
            air_status = 1
            description = "Danger - Poor Air Quality"
            print(f"[{current_time}] ⚠️ ALERT: Poor Air Quality!")
        else:
            air_status = 0
            description = "Safe - Normal Air Quality"
            print(f"[{current_time}] ✅ Status: Normal.")

        # 2. Log to Local CSV File
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, air_status, description])

        # 3. Send Data to ThingSpeak
        payload = {"api_key": API_KEY, "field1": air_status}
        try:
            r = requests.post(URL, data=payload, timeout=10)
            print(f"   -> Cloud Update: HTTP {r.status_code}")
        except Exception as e:
            print(f"   -> Cloud Error: {e} - retrying later...")

        # Wait 15 seconds (ThingSpeak strict limit)
        time.sleep(15)

except KeyboardInterrupt:
    print("\nMonitoring cleanly stopped by user.")
