# 🚁 Hexacopter UAS — CDAC Noida Internship Project

**Internship:** UAS Developer Intern @ CDAC Noida | June 2025 – August 2025

A fully functional **hexacopter drone** designed, assembled, calibrated, and flown from scratch. This repository documents the complete build process — hardware integration, sensor calibration, flight controller configuration, autonomous flight scripting using DroneKit, and Ground Control Station (GCS) operations via Mission Planner.

> ✅ Successfully achieved **manual flight** and **stable hover**, validating complete system integration, control logic, and real-time performance.

---

## 📸 Project Highlights

| Phase | Description | Status |
|-------|-------------|--------|
| Hardware Assembly | Frame, motors, ESCs, FC, GPS, power module | ✅ Complete |
| Sensor Calibration | IMU, Compass, GPS, ESC, RC | ✅ Complete |
| Flight Controller Config | ArduCopter parameters via Mission Planner | ✅ Complete |
| Manual Flight | Stable hover and directional control | ✅ Achieved |
| GCS Integration | Real-time telemetry via Mission Planner | ✅ Complete |
| Autonomous Flight | DroneKit waypoint navigation scripts | ✅ Scripted |

---

## 🛠️ Hardware Configuration

### Frame & Propulsion
| Component | Specification |
|-----------|--------------|
| Frame | Hexacopter (X-configuration, 550mm) |
| BLDC Motors | 920 KV brushless motors (x6) |
| ESCs | 30A electronic speed controllers (x6) |
| Propellers | 10x4.5 inch — 3x CW, 3x CCW |
| Motor Layout | Standard ArduCopter Hexa-X (CW/ACW alternating) |

### Electronics & Avionics
| Component | Specification |
|-----------|--------------|
| Flight Controller | Pixhawk (ArduCopter firmware) |
| GPS Module | u-blox M8N with compass |
| Power Module | 3DR-compatible 5V/12V BEC |
| Battery | 4S 5000mAh LiPo |
| Telemetry | 433 MHz SiK radio modules |
| RC Receiver | FlySky FS-iA6B (6-channel) |

### Motor Layout (ArduCopter Hexa-X)
```
        FRONT
    CW(1)   CCW(2)
  CCW(6)       CW(3)
    CW(5)   CCW(4)
        REAR
```

---

## 📁 Repository Structure

```
hexacopter-uas/
├── README.md
├── hardware/
│   ├── components.md          # Full BOM (Bill of Materials)
│   └── wiring_diagram.md      # Wiring and connection guide
├── calibration/
│   ├── calibrate_imu.py       # IMU/accelerometer calibration helper
│   ├── calibrate_compass.py   # Compass calibration helper
│   ├── calibrate_esc.py       # ESC calibration via DroneKit
│   └── preflight_check.py     # Pre-flight checklist automation
├── flight/
│   ├── manual_flight_params.md    # Key Mission Planner parameters
│   ├── hover_test.py              # Autonomous hover test script
│   ├── waypoint_mission.py        # Waypoint navigation mission
│   └── rtl_test.py                # Return-to-launch test
├── telemetry/
│   ├── telemetry_logger.py        # Log MAVLink telemetry to CSV
│   └── plot_telemetry.py          # Plot flight data (altitude, speed, etc.)
├── gcs/
│   └── mission_planner_params.md  # GCS setup and parameter reference
└── docs/
    ├── build_log.md               # Step-by-step assembly log
    └── lessons_learned.md         # Debugging and key insights
```

---

## Software & Tools

- **Firmware:** ArduCopter (via Pixhawk)
- **GCS:** Mission Planner
- **Scripting:** Python 3, DroneKit
- **Communication:** MAVLink protocol
- **Simulation:** Mission Planner SITL

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install dronekit dronekit-sitl pymavlink pyserial matplotlib
```

### Connect to Drone (USB/Telemetry)
```python
from dronekit import connect
vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)
# For SITL simulation:
# vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
```

### Run Pre-flight Check
```bash
python calibration/preflight_check.py --connect /dev/ttyUSB0
```

### Run Hover Test (SITL)
```bash
python flight/hover_test.py --connect tcp:127.0.0.1:5760
```

---

## Results

- Stable hover achieved at ~1.5m altitude
- GPS lock acquired within 2 minutes (open field)
- IMU vibration levels within acceptable range (< 15 m/s^2)
- All 6 ESCs calibrated and responding symmetrically
- RTL (Return to Launch) mode validated

---

## Author

**Arpit**
B.Tech Automation & Robotics | USAR, GGSIPU (2023–2027)
Internship: CDAC Noida — UAS Developer Intern

---

## License

MIT License — free to use for educational and research purposes.
