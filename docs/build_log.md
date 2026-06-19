# Hexacopter Build Log
CDAC Noida UAS Internship | June 2025

## Week 1 — Component Sourcing & Frame Assembly
- Received all components: frame kit, 6x BLDC motors, 6x ESCs, Pixhawk FC, GPS, battery, PDB
- Assembled hexacopter frame (550mm X-config), attached arms and motor mounts
- Mounted BLDC motors — verified CW/CCW orientation per ArduCopter Hexa-X layout:
  - Front-Right: CW (M1), Rear-Right: CCW (M2), Right: CW (M3)
  - Rear-Left: CCW (M4), Left: CW (M5), Front-Left: CCW (M6)
- Installed landing gear (tall skid-type for camera clearance)
- **Issue:** Motor 3 mount holes misaligned — re-drilled with 3mm bit

## Week 2 — Electronics Integration & Wiring
- Soldered ESCs to Power Distribution Board (PDB)
- Ran ESC signal wires to Pixhawk MAIN OUT channels 1–6
- Mounted Pixhawk on vibration dampening foam platform (M3 nylon standoffs)
- Connected GPS module to Pixhawk GPS port and I2C (compass)
- Raised GPS on 15cm mast to reduce magnetic interference from PDB
- Installed telemetry radio (433 MHz) on TELEM1 port
- Connected RC receiver (FlySky iA6B) in PPM mode to RC IN
- First power-on test (no props): Pixhawk booted, Mission Planner connected

## Week 3 — Calibration & Configuration
- Completed 6-position IMU (accelerometer) calibration via Mission Planner
- Completed compass calibration (onboard + external) — fitness < 0.35
- Completed RC radio calibration (all 6 channels)
- ESC calibration performed — all 6 ESCs confirmed calibrated (beep sequence OK)
- Set flight modes: STABILIZE / ALT_HOLD / LOITER / AUTO / RTL / LAND
- Configured battery failsafe at 14.0V, GCS heartbeat failsafe enabled
- Motor test via Mission Planner (no props) — all 6 motors spun in correct direction

## Week 4 — Ground Testing & First Flight
- Vibration test: mounted, spun motors at 50% throttle — vibration < 10 m/s^2 (excellent)
- SITL simulation: ran hover_test.py and waypoint_mission.py — all passed
- First outdoor test: flew in STABILIZE mode
  - Motors armed cleanly, throttle response smooth
  - Achieved stable hover at ~1.5m altitude for 30+ seconds
  - Yaw, pitch, roll response as expected
  - RTL mode tested — drone returned to home and landed within 1m of launch point
- **Issue:** Slight toilet-bowl effect in LOITER mode — resolved by re-calibrating compass away from metal table

## Key Lessons Learned
1. Always mount compass as far as possible from PDB and power cables
2. ESC calibration must be done with battery directly (not through USB power)
3. Level the drone precisely before IMU calibration — any tilt affects the accel offsets
4. SITL simulation saves time — test all scripts in simulation before real hardware
5. Use motor test in Mission Planner before installing props to verify rotation direction
