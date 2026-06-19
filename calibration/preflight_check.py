#!/usr/bin/env python3
"""
preflight_check.py
------------------
Automated pre-flight checklist for the CDAC Hexacopter UAS.
Connects via DroneKit/MAVLink and validates all critical systems
before any flight operation.

Usage:
    python preflight_check.py --connect /dev/ttyUSB0          # real hardware
    python preflight_check.py --connect tcp:127.0.0.1:5760    # SITL simulation

Author: Arpit | CDAC Noida UAS Internship 2025
"""

import argparse
import time
import sys
from dronekit import connect, VehicleMode
from pymavlink import mavutil


# ── Thresholds ────────────────────────────────────────────────────────────────
MIN_BATTERY_VOLTAGE   = 14.0   # Volts  (3.5V/cell × 4S)
MIN_GPS_SATELLITES    = 6      # satellites for reliable lock
MAX_HDOP              = 2.0    # horizontal dilution of precision
MAX_VIBE_THRESHOLD    = 15.0   # m/s² — ArduCopter recommended limit
ARMED_TIMEOUT         = 10     # seconds to wait for arm confirmation


def parse_args():
    parser = argparse.ArgumentParser(description="Hexacopter Pre-flight Checklist")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760",
                        help="MAVLink connection string")
    parser.add_argument("--baud", type=int, default=57600,
                        help="Serial baud rate (default: 57600)")
    return parser.parse_args()


def print_header():
    print("\n" + "="*55)
    print("   HEXACOPTER UAS — PRE-FLIGHT CHECKLIST")
    print("   CDAC Noida | ArduCopter / Pixhawk")
    print("="*55)


def check(label, passed, detail=""):
    """Print a single checklist item result."""
    status = "  PASS" if passed else "  FAIL"
    detail_str = f"  ({detail})" if detail else ""
    print(f"  [{status}] {label}{detail_str}")
    return passed


def run_preflight(vehicle):
    results = []
    print("\n--- BATTERY ---")
    v = vehicle.battery.voltage
    results.append(check("Battery voltage", v is not None and v >= MIN_BATTERY_VOLTAGE,
                          f"{v:.2f}V" if v else "N/A"))

    level = vehicle.battery.level
    results.append(check("Battery level", level is not None and level >= 20,
                          f"{level}%" if level else "N/A"))

    print("\n--- GPS ---")
    gps = vehicle.gps_0
    results.append(check("GPS fix type", gps.fix_type >= 3,
                          f"fix_type={gps.fix_type}"))
    results.append(check("Satellites visible", gps.satellites_visible >= MIN_GPS_SATELLITES,
                          f"{gps.satellites_visible} sats"))
    results.append(check("HDOP acceptable", gps.eph is not None and gps.eph <= MAX_HDOP * 100,
                          f"HDOP={gps.eph/100:.2f}" if gps.eph else "N/A"))

    print("\n--- IMU / AHRS ---")
    ekf = vehicle.ekf_ok
    results.append(check("EKF health", ekf, "EKF converged" if ekf else "EKF not ready"))

    attitude = vehicle.attitude
    roll_ok  = abs(attitude.roll)  < 0.1   # ~5.7°
    pitch_ok = abs(attitude.pitch) < 0.1
    results.append(check("Level on ground (roll)",  roll_ok,
                          f"{attitude.roll:.3f} rad"))
    results.append(check("Level on ground (pitch)", pitch_ok,
                          f"{attitude.pitch:.3f} rad"))

    print("\n--- FLIGHT CONTROLLER ---")
    results.append(check("Autopilot connected", vehicle.is_armable is not None))
    results.append(check("No pre-arm errors", vehicle.is_armable,
                          "Ready to arm" if vehicle.is_armable else "Pre-arm checks failing"))

    mode_ok = vehicle.mode.name in ("STABILIZE", "LOITER", "ALT_HOLD", "GUIDED")
    results.append(check("Flight mode set", mode_ok, vehicle.mode.name))

    print("\n--- SUMMARY ---")
    passed = sum(results)
    total  = len(results)
    print(f"  {passed}/{total} checks passed")

    if passed == total:
        print("\n  ✅ ALL CHECKS PASSED — Safe to proceed with flight.\n")
    else:
        failed = total - passed
        print(f"\n  ⚠️  {failed} CHECK(S) FAILED — Do NOT fly until resolved.\n")

    return passed == total


def main():
    args = parse_args()
    print_header()

    print(f"\n[*] Connecting to vehicle at {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        sys.exit(1)

    print(f"[*] Connected. Firmware: {vehicle.version}")
    print(f"[*] Vehicle type: {vehicle._vehicle_type}")

    try:
        run_preflight(vehicle)
    finally:
        vehicle.close()
        print("[*] Connection closed.")


if __name__ == "__main__":
    main()
