#!/usr/bin/env python3
"""
calibrate_esc.py
----------------
ESC (Electronic Speed Controller) calibration helper.
Sends PWM min/max signals via DroneKit to calibrate all 6 ESCs simultaneously.

WARNING: Remove propellers before running this script.

Usage:
    python calibrate_esc.py --connect /dev/ttyUSB0

Author: Arpit | CDAC Noida UAS Internship 2025
"""

import argparse
import time
import sys
from dronekit import connect, VehicleMode
from pymavlink import mavutil


PWM_MAX = 2000   # microseconds — throttle high signal
PWM_MIN = 1000   # microseconds — throttle low signal
NUM_MOTORS = 6


def parse_args():
    parser = argparse.ArgumentParser(description="ESC Calibration Tool")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud", type=int, default=57600)
    return parser.parse_args()


def set_servo_pwm(vehicle, channel, pwm):
    """Override a servo/motor channel with a specific PWM value."""
    vehicle._master.mav.command_long_send(
        vehicle._master.target_system,
        vehicle._master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        channel,
        pwm,
        0, 0, 0, 0, 0
    )


def release_overrides(vehicle):
    """Release all channel overrides."""
    overrides = vehicle.channels.overrides
    for ch in range(1, 9):
        overrides[str(ch)] = 0
    vehicle.channels.overrides = overrides


def main():
    args = parse_args()
    print("\n============================")
    print("  ESC CALIBRATION TOOL")
    print("  Hexacopter — 6 Motors")
    print("============================\n")
    print("[!] CRITICAL: Remove ALL propellers before continuing!\n")
    input("Confirm props removed — press ENTER to continue...")

    print(f"\n[*] Connecting to {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print("[*] Connected.")

    # Step 1: Send max throttle
    print("\n[Step 1] Sending MAXIMUM throttle signal to all ESCs...")
    print("         Connect battery NOW when ESCs beep (ready signal).")
    for ch in range(1, NUM_MOTORS + 1):
        set_servo_pwm(vehicle, ch, PWM_MAX)
    time.sleep(3)

    # Step 2: Wait for ESC ready beeps
    input("\n[Step 2] Wait for ESC startup beeps, then press ENTER...")

    # Step 3: Send min throttle
    print("\n[Step 3] Sending MINIMUM throttle signal...")
    for ch in range(1, NUM_MOTORS + 1):
        set_servo_pwm(vehicle, ch, PWM_MIN)
    time.sleep(3)

    print("\n[*] ESC calibration complete. You should have heard the confirmation beeps.")
    print("[*] Releasing overrides...")
    release_overrides(vehicle)

    print("[*] Test motor spin-up with Mission Planner Motor Test before installing props.")
    vehicle.close()
    print("[*] Done.\n")


if __name__ == "__main__":
    main()
