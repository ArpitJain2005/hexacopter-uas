# Mission Planner — GCS Setup & Operations Guide

## Initial Setup Checklist (Mission Planner)

### 1. Connect to Flight Controller
- Port: COM port (USB) or UDP/TCP for telemetry
- Baud: 57600 (telemetry radio) or 115200 (USB direct)
- Click **Connect** (top right)

### 2. Mandatory Hardware Setup (Initial Setup tab)

| Step | Location | Notes |
|------|----------|-------|
| Frame Class | Mandatory Hardware > Frame Type | Set to Hexa X |
| Accel Calibration | Mandatory Hardware > Accel Calibration | 6-position, level first |
| Compass Calibration | Mandatory Hardware > Compass | OnBoard + external; rotate all axes |
| Radio Calibration | Mandatory Hardware > Radio Calibration | Move all sticks to extremes |
| ESC Calibration | Optional Hardware > ESC Calibration | Or use calibrate_esc.py |
| Flight Modes | Mandatory Hardware > Flight Modes | Set CH5 switch positions |

### 3. Recommended Flight Modes (CH5 switch)
| Switch Position | Mode | Use Case |
|----------------|------|----------|
| 1 | STABILIZE | Manual flight, learning |
| 2 | ALT_HOLD | Altitude-assisted manual |
| 3 | LOITER | GPS-assisted hover |
| 4 | AUTO | Waypoint mission |
| 5 | RTL | Return to launch |
| 6 | LAND | Controlled descent |

### 4. SITL Simulation Setup
```
# Start SITL from ArduCopter source
cd ArduCopter
sim_vehicle.py -v ArduCopter --console --map

# Connect Mission Planner to SITL
# Port: TCP  |  Address: 127.0.0.1  |  Port: 5760
```

## GCS Dashboard — Key Instruments to Monitor

| Instrument | Normal Range | Warning |
|------------|-------------|---------|
| Battery voltage | > 14.8V (4S full) | < 14.0V (failsafe) |
| GPS HDOP | < 1.5 | > 2.0 |
| Satellites | > 8 | < 6 |
| EKF variance | Green | Any Red = land |
| Vibration (X/Y/Z) | < 15 m/s^2 | > 30 m/s^2 |

## Pre-flight GCS Checklist

- [ ] GCS connected and receiving telemetry
- [ ] Battery voltage displayed and > 15V
- [ ] GPS 3D fix, HDOP < 2.0, satellites > 6
- [ ] EKF health indicators all green
- [ ] Home position set (map shows H marker)
- [ ] Flight mode correct (STABILIZE for first flight)
- [ ] RC input moving as expected (HUD shows response)
- [ ] Failsafe parameters verified

## Recording & Downloading Logs

- **Onboard logs:** Pixhawk logs to micro SD (DataFlash .bin files)
- **Download:** Mission Planner > DataFlash Logs > Download Logs
- **Analyze:** Mission Planner > DataFlash Logs > Review a Log
  - Check: vibration, attitude, motor outputs, battery
