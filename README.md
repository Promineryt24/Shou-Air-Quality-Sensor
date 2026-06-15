# ☁️ Shou-Air-Quality-Monitoring

An Internet of Things (IoT) environmental monitoring system built to track indoor air quality. This project utilizes a Raspberry Pi Zero 2 W and an MQ-135 gas sensor to detect airborne pollutants, logging data locally to a CSV file and pushing real-time alerts to a ThingSpeak cloud dashboard.

Developed as a project for **IEA123: Internet of Things for Environmental Monitoring Towards Artificial Intelligence**.

---

## 🎯 Project Objectives

* **Systematic Data Acquisition:** Continuously monitor ambient air quality using a digital threshold system.
* **Fault-Tolerant Logging:** Simultaneously save data locally (`air_quality_log.csv`) to prevent data loss during network outages.
* **Cloud Integration:** Push live environmental status (Safe vs. Danger) to a ThingSpeak dashboard for remote monitoring and data visualization.
* **Safe Hardware Integration:** Implement a custom voltage divider circuit to safely bridge 5V sensor logic with 3.3V microcontroller inputs.

---

## 🛠️ Hardware Requirements

* **Microcontroller:** Raspberry Pi Zero 2 W (Myduino IoT Maker Kit)
* **Sensor:** MQ-135 Air Quality Sensor
* **Components:** Breadboard, Jumper Wires
* **Logic Level Protection:** 2x **2kΩ** Resistors (Used to build a 50/50 voltage divider)

---

## ⚠️ Critical Hardware Wiring & Voltage Divider

The MQ-135 sensor requires **5V** to power its internal heater, meaning its Digital Out (DO) pin outputs a **5V** signal. The Raspberry Pi Zero 2 W GPIO pins are strictly **3.3V** tolerant. Connecting them directly will permanently damage the Pi. 

To safely step down the voltage to **2.5V** (which the Pi safely registers as a "HIGH" signal), this project uses a voltage divider built with two **2kΩ** resistors.

### 🔌 Wiring Guide

| MQ-135 Sensor Pin | Connection / Component | Raspberry Pi Zero 2 W Pin |
| :--- | :--- | :--- |
| **VCC** | Direct Wire | **Pin 2 (5V)** |
| **GND** | Direct Wire | **Pin 6 (GND)** |
| **DO (Digital Out)** | To Breadboard Row A | - |
| - | **2kΩ** Resistor 1: Row A to Row B | - |
| - | **2kΩ** Resistor 2: Row B to GND Rail | - |
| - | GND Rail to Pi GND | **Pin 9 (GND)** |
| - | Data Wire: Row B to Pi GPIO | **Pin 7 (GPIO 4)** |
| **AO (Analog Out)** | *Leave Disconnected* | - |

---

## ⚙️ Software Setup & Cloud Integration

### Prerequisites

Ensure your Raspberry Pi is running an updated OS (Debian Trixie compatible) and has the required `requests` library installed for cloud communication.

```bash
sudo apt update
pip3 install requests --break-system-packages
