# Project Report — Hexacopter UAS Development
### CDAC Noida Internship | June – August 2025
**Intern:** Arpit Jain | B.Tech Automation & Robotics, USAR GGSIPU (2023–2027)

---

## 1. Introduction

This report documents the design, assembly, calibration, and flight validation of a
custom hexacopter Unmanned Aerial System (UAS) developed during a summer internship at
CDAC Noida. The project objective was to build a fully integrated, flight-ready hexacopter
and achieve stable hover — validating system integration from hardware to firmware.

---

## 2. Objectives

- Design and assemble a hexacopter from individual components
- Configure CW/CCW motor layout for torque balance
- Calibrate all sensors (IMU, GPS, ESCs) for flight readiness
- Utilize Mission Planner for GCS operations and parameter tuning
- Achieve stable manual flight and hover

---

## 3. System Design

### 3.1 Frame Selection
A hexacopter X-frame was chosen over a quadcopter for:
- **Redundancy**: Loss of one motor can still allow controlled descent
- **Higher payload capacity**: 6 motors provide greater total thrust
- **Stability**: More even thrust distribution

### 3.2 Motor Configuration
Alternating CW/CCW motor pairs cancel yaw reaction torques without requiring tail rotors.
ArduCopter motor numbering (Motor 1–6) was followed exactly to match firmware expectations.

### 3.3 Power System
A 4S LiPo battery was selected to balance energy density and motor compatibility.
The power module provides dual output: main battery power to the PDB and a regulated
5V BEC to the flight controller and peripherals. Voltage and current are monitored via
MAVLink for real-time GCS display and battery failsafe.

### 3.4 Flight Controller
The Pixhawk / APM running ArduCopter firmware was selected for its:
- Open-source, well-documented firmware stack
- Integrated IMU (3-axis accel + gyro + mag)
- MAVLink protocol for GCS integration
- Mission Planner compatibility

---

## 4. Assembly Process

Assembly followed a structured 6-phase approach (see `hardware/component_checklist.md`):

1. Frame construction and landing gear attachment
2. Motor and ESC mounting, PDB soldering
3. Flight controller installation on vibration dampers
4. GPS mast mounting and peripheral wiring
5. RC receiver and telemetry radio connection
6. Pre-power safety inspection

Key challenge: Routing all signal and power cables away from motor wires and propeller
arcs while keeping the center of gravity balanced.

---

## 5. Calibration Procedure

### 5.1 ESC Calibration
All 6 ESCs were calibrated simultaneously by sending max-then-min PWM signals from the
flight controller. This ensures all ESCs share the same throttle range, so all 6 motors
spin up uniformly for a given throttle command.

### 5.2 Accelerometer Calibration
The drone was placed in 6 orientations (level, left side, right side, nose down, nose up,
inverted) as prompted by Mission Planner, allowing the IMU to determine its true orientation
relative to gravity in all axes.

### 5.3 Compass Calibration
Performed onboard compass calibration (rotating the drone in all directions) to cancel
hard and soft iron distortions from nearby motors and battery.

### 5.4 RC Calibration
All RC channels were mapped and their min/mid/max PWM endpoints recorded to ensure
accurate stick-to-attitude translation.

---

## 6. Mission Planner & GCS Operations

Mission Planner was used for:
- **Firmware flashing** and frame type selection
- **Mandatory hardware calibration** workflows
- **Parameter tuning** (PID gains, failsafe voltages, RTL altitude)
- **SITL simulation** — all Python scripts validated in simulation first
- **Live telemetry monitoring** — attitude, GPS, battery, EKF status
- **Motor test** — individual motor verification before first flight

---

## 7. Flight Testing & Results

### 7.1 First Hover
Manual flight in STABILIZE mode was performed in a controlled outdoor area.
The drone was armed via RC, spun up motors, and lifted off to approximately 2–3m AGL.

**Observations:**
- All 6 motors spun simultaneously at arm
- Drone lifted off without yaw rotation (correct CW/CCW balance)
- Manual attitude corrections were required (STABILIZE mode — no auto-leveling beyond gyro stabilization)
- Hover maintained for ~30 seconds

### 7.2 GPS-Assisted Hover (LOITER Mode)
After achieving manual flight confidence, GPS LOITER mode was tested:
- GPS fix acquired (3D, 10+ satellites, HDOP ~1.2)
- EKF health confirmed green in Mission Planner
- Drone held position within ~1.5m horizontal radius during hover

**Result: Stable hover validated ✅**

---

## 8. Key Learnings

- Proper CW/CCW propeller orientation is critical — reversed props cause immediate flip on takeoff
- Vibration isolation of the FC significantly impacts IMU data quality and EKF health
- GPS antenna placement must be as far from electronics as possible to reduce noise
- SITL simulation is invaluable — all scripts were SITL-validated before real flight
- Battery voltage monitoring and failsafe configuration are non-negotiable safety requirements

---

## 9. Tools & Technologies

| Category         | Tools Used                                              |
|------------------|---------------------------------------------------------|
| Firmware         | ArduCopter (ArduPilot stack)                            |
| GCS              | Mission Planner                                         |
| Programming      | Python 3, DroneKit, PyMAVLink                           |
| Simulation       | Mission Planner SITL                                    |
| Hardware         | Pixhawk FC, u-blox M8N GPS, BLDC motors, ESCs          |
| Communication    | MAVLink protocol, 433MHz telemetry                      |

---

## 10. Conclusion

The project successfully achieved its primary objective: a fully assembled, calibrated,
and flight-validated hexacopter UAS. The drone demonstrated stable hover in both manual
STABILIZE mode and GPS-assisted LOITER mode, confirming correct integration of all hardware,
firmware, and control systems.

The internship provided practical exposure to the complete UAS development lifecycle —
from soldering and mechanical assembly to flight controller tuning and autonomous flight
scripting — reinforcing core skills in embedded systems, robotics, and real-time systems.

---

*Report prepared by Arpit Jain | CDAC Noida Internship 2025*
