# Mission Planner — Setup & Parameter Tuning Guide

## Overview

Mission Planner (MP) is the Ground Control Station (GCS) software used throughout this
project for firmware flashing, sensor calibration, parameter tuning, simulation, and
live telemetry monitoring.

---

## 1. Initial Setup

### 1.1 Firmware Installation
1. Connect FC via USB.
2. Open Mission Planner → **Setup → Install Firmware**.
3. Select **ArduCopter** → **Hexa** frame type.
4. Click **Upload Firmware** and wait for completion.

### 1.2 Frame Type Configuration
- Navigate to **Config → Full Parameter List** or **Initial Setup → Mandatory Hardware → Frame Type**.
- Set `FRAME_CLASS = 2` (Hexacopter)
- Set `FRAME_TYPE = 1` (X configuration)

---

## 2. Mandatory Hardware Calibration

### 2.1 Accelerometer Calibration
1. Go to **Initial Setup → Mandatory Hardware → Accel Calibration**.
2. Click **Calibrate Accel**.
3. Place drone in 6 positions when prompted:
   - Level (flat on ground)
   - On left side
   - On right side
   - Nose down
   - Nose up
   - Upside down
4. Click **Done** when complete.

### 2.2 Compass Calibration
1. Go to **Initial Setup → Mandatory Hardware → Compass**.
2. Click **Start** under **Onboard Mag Calibration**.
3. Rotate drone in all orientations until progress bars complete.
4. Click **Reboot** to apply.

### 2.3 Radio Calibration
1. Go to **Initial Setup → Mandatory Hardware → Radio Calibration**.
2. Turn on RC transmitter.
3. Click **Calibrate Radio** and move all sticks to extremes.
4. Set flight mode channel (CH5 typically) to 3-position switch.

### 2.4 ESC Calibration
> See `calibration/esc_calibration.py` for automated method.  
> Manual method: MP → Initial Setup → Optional Hardware → ESC Calibration.

### 2.5 Flight Modes
Recommended mode configuration for CH5:

| Position | Mode        | Purpose                          |
|----------|-------------|----------------------------------|
| Low      | STABILIZE   | Manual attitude control          |
| Mid      | ALT_HOLD    | Barometer altitude hold          |
| High     | LOITER      | GPS position + altitude hold     |

---

## 3. Key Parameters (Full Parameter List)

| Parameter       | Recommended Value | Description                              |
|-----------------|-------------------|------------------------------------------|
| `ARMING_CHECK`  | 1 (all)           | Enable all arming pre-checks             |
| `FS_THR_ENABLE` | 1                 | Throttle failsafe → RTL                  |
| `FS_GCS_ENABLE` | 1                 | GCS heartbeat failsafe                   |
| `BATT_LOW_VOLT` | 14.0              | Low battery warning voltage (4S)         |
| `BATT_CRT_VOLT` | 13.2              | Critical battery → RTL trigger           |
| `RTL_ALT`       | 3000              | RTL climb altitude in cm (= 30m)         |
| `LAND_SPEED`    | 50                | Descent speed during landing (cm/s)      |
| `WPNAV_SPEED`   | 500               | Waypoint nav speed (cm/s)                |
| `INS_GYRO_FILT` | 20                | Gyro low-pass filter (Hz)                |
| `ATC_RAT_RLL_P` | 0.135             | Roll rate P gain (tune per aircraft)     |
| `ATC_RAT_PIT_P` | 0.135             | Pitch rate P gain                        |

---

## 4. PID Tuning (Basic)

ArduCopter default PIDs work for most builds but should be adjusted if:
- Oscillations occur in hover
- Drone feels sluggish
- Toilet-bowling (slow GPS drift circles)

### Basic Approach
1. Start with default PIDs in STABILIZE mode.
2. Fly short hover. If oscillations → reduce Rate P gains.
3. If sluggish → increase Rate P slightly.
4. Enable AutoTune: Set CH7 option to `AutoTune` (param `CH7_OPT = 17`).
5. Fly in calm wind in ALT_HOLD mode, flip CH7 to trigger AutoTune.
6. Let drone self-tune, land, and save params when complete.

---

## 5. Simulation (SITL)

Mission Planner includes a built-in SITL simulator:
1. Go to **Simulation** tab in Mission Planner.
2. Select **Multi-Rotor → Hexa**.
3. Click **Start Simulation**.
4. Connect using `tcp:127.0.0.1:5760` in scripts.

This was used extensively during the CDAC internship to validate
all Python scripts before real flight testing.

---

## 6. Pre-Flight Checklist (Mission Planner)

- [ ] HUD shows correct attitude (level with drone flat)
- [ ] GPS fix: 3D, ≥6 satellites, HDOP ≤ 2.0
- [ ] EKF status: green in HUD
- [ ] Battery voltage: above 15.8V (4S full)
- [ ] All RC channels respond in correct direction
- [ ] Flight modes correctly assigned to switch positions
- [ ] Failsafe actions configured (throttle, GCS, battery)
- [ ] Arm via RC (throttle down-right hold 3s) or MP safety slider
