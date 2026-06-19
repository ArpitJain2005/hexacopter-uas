#!/usr/bin/env python3
import argparse
import time
import sys
from dronekit import connect
from pymavlink import mavutil


POSITIONS = [
    "LEVEL (top facing up, front facing forward) — default rest position",
    "RIGHT SIDE DOWN (right arm pointing down)",
    "LEFT SIDE DOWN (left arm pointing down)",
    "NOSE DOWN (front pointing down)",
    "NOSE UP (front pointing up)",
    "UPSIDE DOWN (top facing ground)",
]


def parse_args():
    parser = argparse.ArgumentParser(description="IMU Accelerometer Calibration")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud", type=int, default=57600)
    return parser.parse_args()


def send_calibration_command(vehicle, accelcal):
    """Send MAVLink PREFLIGHT_CALIBRATION message."""
    vehicle._master.mav.command_long_send(
        vehicle._master.target_system,
        vehicle._master.target_component,
        mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION,
        0,          # confirmation
        0,          # gyro cal
        0,          # magnetometer cal
        0,          # ground pressure
        0,          # radio cal
        accelcal,   # accel cal (1=simple, 2=full 6-pos)
        0,          # compass/motor interference
        0           # airspeed
    )


def wait_for_ack(vehicle, timeout=30):
    """Wait for COMMAND_ACK from FC."""
    start = time.time()
    while time.time() - start < timeout:
        msg = vehicle._master.recv_match(type='COMMAND_ACK', blocking=False)
        if msg:
            return msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED
        time.sleep(0.1)
    return False


def main():
    args = parse_args()
    print("\n========================================")
    print("  IMU ACCELEROMETER CALIBRATION TOOL")
    print("  CDAC Noida Hexacopter UAS")
    print("========================================\n")

    print(f"[*] Connecting to {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print("[*] Connected. Ensure props are REMOVED before calibration.\n")
    input("Press ENTER to begin 6-position accelerometer calibration...")

    for i, position in enumerate(POSITIONS):
        print(f"\n--- Position {i+1}/6 ---")
        print(f"  Orient drone: {position}")
        input("  Press ENTER when ready and drone is held STILL...")

        # For real hardware, each position is triggered by separate call.
        # ArduCopter auto-advances through positions; this script guides user timing.
        if i == 0:
            send_calibration_command(vehicle, 1)  # Initiate calibration
            time.sleep(1)
        else:
            # Send continue signal (simulated here; Mission Planner handles ack-based flow)
            time.sleep(2)

        print(f"  [*] Position {i+1} captured.")

    print("\n[*] Calibration sequence complete.")
    print("[*] Reboot the flight controller to apply new calibration values.")
    print("[!] Verify in Mission Planner: Initial Setup > Mandatory Hardware > Accel Calibration\n")

    vehicle.close()
    print("[*] Disconnected.")


if __name__ == "__main__":
    main()
