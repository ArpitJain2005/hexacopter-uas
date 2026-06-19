#!/usr/bin/env python3
"""
calibrate_compass.py
--------------------
Initiates compass (magnetometer) calibration on ArduCopter via MAVLink.
The user rotates the drone through all axes during calibration.

Usage:
    python calibrate_compass.py --connect /dev/ttyUSB0

Author: Arpit | CDAC Noida UAS Internship 2025
"""

import argparse
import time
import sys
from dronekit import connect
from pymavlink import mavutil


def parse_args():
    parser = argparse.ArgumentParser(description="Compass Calibration")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud", type=int, default=57600)
    return parser.parse_args()


def start_compass_cal(vehicle):
    vehicle._master.mav.command_long_send(
        vehicle._master.target_system,
        vehicle._master.target_component,
        mavutil.mavlink.MAV_CMD_DO_START_MAG_CAL,
        0,
        0,    # mag_mask  (0 = calibrate all)
        1,    # retry
        1,    # autosave
        0,    # delay
        0, 0, 0
    )


def monitor_calibration(vehicle, duration=60):
    """Listen for MAG_CAL_PROGRESS messages during calibration."""
    print("[*] Rotate the drone slowly through all axes (pitch, roll, yaw).")
    print(f"[*] You have {duration} seconds...\n")
    start = time.time()
    while time.time() - start < duration:
        msg = vehicle._master.recv_match(
            type=['MAG_CAL_PROGRESS', 'MAG_CAL_REPORT'], blocking=False)
        if msg:
            mtype = msg.get_type()
            if mtype == 'MAG_CAL_PROGRESS':
                print(f"  Compass {msg.compass_id} — {msg.completion_pct}% complete  "
                      f"| Attempt {msg.attempt}", end="\r")
            elif mtype == 'MAG_CAL_REPORT':
                result_str = {0: "PENDING", 1: "RUNNING", 2: "SUCCESS",
                              3: "FAILED", 4: "BAD_ORIENTATION"}.get(msg.cal_status, "UNKNOWN")
                print(f"\n  Compass {msg.compass_id}: {result_str} "
                      f"| Fitness: {msg.fitness:.4f}")
        time.sleep(0.1)


def main():
    args = parse_args()
    print("\n==============================")
    print("  COMPASS CALIBRATION TOOL")
    print("==============================\n")

    print(f"[*] Connecting to {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print("[*] Connected.")
    print("[!] Move drone AWAY from metal objects, computers, and magnetic sources.\n")
    input("Press ENTER to start compass calibration...")

    start_compass_cal(vehicle)
    monitor_calibration(vehicle, duration=60)

    print("\n[*] Calibration window complete.")
    print("[*] Check Mission Planner for final offsets and fitness values.")
    print("[*] Fitness < 0.4 is ideal. > 0.8 may indicate interference.\n")

    vehicle.close()


if __name__ == "__main__":
    main()
