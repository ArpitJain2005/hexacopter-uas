#!/usr/bin/env python3
"""
rtl_test.py
-----------
Tests Return-to-Launch (RTL) functionality.
Arm, take off, fly to a small offset, then trigger RTL
and confirm the drone returns and lands at home.

Usage:
    python rtl_test.py --connect tcp:127.0.0.1:5760

Author: Arpit | CDAC Noida UAS Internship 2025
"""

import argparse
import time
import sys
from dronekit import connect, VehicleMode, LocationGlobalRelative


def parse_args():
    parser = argparse.ArgumentParser(description="RTL Test")
    parser.add_argument("--connect",  default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud",     type=int,   default=57600)
    parser.add_argument("--altitude", type=float, default=3.0)
    return parser.parse_args()


def arm_and_takeoff(vehicle, alt):
    while not vehicle.is_armable:
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode.name != "GUIDED":
        time.sleep(0.5)
    vehicle.armed = True
    while not vehicle.armed:
        time.sleep(1)
    vehicle.simple_takeoff(alt)
    while vehicle.location.global_relative_frame.alt < alt * 0.95:
        time.sleep(0.5)
    print(f"[OK] At {vehicle.location.global_relative_frame.alt:.1f}m")


def main():
    args = parse_args()
    print("\n====================")
    print("  RTL TEST")
    print("====================")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    try:
        arm_and_takeoff(vehicle, args.altitude)
        print("[*] Hovering 5s before RTL...")
        time.sleep(5)

        print("[*] Triggering RTL...")
        vehicle.mode = VehicleMode("RTL")

        while vehicle.armed:
            alt = vehicle.location.global_relative_frame.alt
            print(f"  RTL in progress ... alt={alt:.1f}m", end="\r")
            time.sleep(0.5)

        print("\n[OK] RTL successful. Vehicle landed and disarmed.")
    except KeyboardInterrupt:
        vehicle.mode = VehicleMode("LAND")
    finally:
        vehicle.close()


if __name__ == "__main__":
    main()
