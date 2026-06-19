#!/usr/bin/env python3
"""
hover_test.py
-------------
Autonomous hover test for the CDAC Hexacopter UAS.
Arms the drone, takes off to a target altitude, holds hover
for a set duration, then lands, validating stable flight.

Test in SITL before flying real hardware.

Usage:
    python hover_test.py --connect tcp:127.0.0.1:5760     # SITL
    python hover_test.py --connect /dev/ttyUSB0 --altitude 1.5  # Hardware

Author: Arpit | CDAC Noida UAS Internship 2025
"""

import argparse
import time
import sys
from dronekit import connect, VehicleMode


def parse_args():
    parser = argparse.ArgumentParser(description="Autonomous Hover Test")
    parser.add_argument("--connect",  default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud",     type=int,   default=57600)
    parser.add_argument("--altitude", type=float, default=1.5,
                        help="Target hover altitude in metres (default: 1.5)")
    parser.add_argument("--duration", type=int,   default=10,
                        help="Hover duration in seconds (default: 10)")
    return parser.parse_args()


def arm_and_takeoff(vehicle, target_altitude):
    print("\n[*] Running pre-arm checks...")
    while not vehicle.is_armable:
        print("  Waiting for vehicle to be armable (GPS fix + EKF)...")
        time.sleep(1)

    print("[*] Switching to GUIDED mode...")
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode.name != "GUIDED":
        time.sleep(0.5)

    print("[*] Arming motors...")
    vehicle.armed = True
    while not vehicle.armed:
        print("  Waiting for arm confirmation...")
        time.sleep(1)
    print("[OK] Motors armed.")

    print(f"[*] Taking off to {target_altitude}m ...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f"  Altitude: {alt:.2f}m / {target_altitude}m", end="\r")
        if alt >= target_altitude * 0.95:
            print(f"\n[OK] Target altitude reached: {alt:.2f}m")
            break
        time.sleep(0.5)


def hover(vehicle, duration):
    print(f"\n[*] Hovering for {duration} seconds ...")
    print(f"{'Time':>6} | {'Alt(m)':>7} | {'Roll(deg)':>9} | {'Pitch(deg)':>10} | {'Bat(V)':>7}")
    print("-" * 52)
    start = time.time()
    while time.time() - start < duration:
        elapsed = time.time() - start
        alt   = vehicle.location.global_relative_frame.alt
        roll  = vehicle.attitude.roll  * 57.296
        pitch = vehicle.attitude.pitch * 57.296
        bat   = vehicle.battery.voltage or 0.0
        print(f"{elapsed:>5.1f}s | {alt:>7.2f} | {roll:>+9.2f} | {pitch:>+10.2f} | {bat:>6.2f}V")
        time.sleep(1)


def land(vehicle):
    print("\n[*] Initiating LAND mode ...")
    vehicle.mode = VehicleMode("LAND")
    while vehicle.mode.name != "LAND":
        time.sleep(0.5)
    while vehicle.armed:
        alt = vehicle.location.global_relative_frame.alt
        print(f"  Landing ... {alt:.2f}m", end="\r")
        time.sleep(0.5)
    print("\n[OK] Landed and disarmed.")


def main():
    args = parse_args()
    print("\n================================")
    print("  HEXACOPTER HOVER TEST")
    print("================================")
    print(f"\n[*] Connecting to {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print(f"[*] Connected | Firmware: {vehicle.version}")
    try:
        arm_and_takeoff(vehicle, args.altitude)
        hover(vehicle, args.duration)
        land(vehicle)
        print("\n[OK] Hover test COMPLETE.")
    except KeyboardInterrupt:
        print("\n[!] Interrupted -- switching to LAND.")
        vehicle.mode = VehicleMode("LAND")
    finally:
        vehicle.close()
        print("[*] Connection closed.\n")


if __name__ == "__main__":
    main()
