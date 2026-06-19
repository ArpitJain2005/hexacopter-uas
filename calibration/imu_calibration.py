"""
IMU Preflight Check & Calibration Monitor — Hexacopter UAS
===========================================================
CDAC Noida Internship | Arpit Jain

Purpose:
    Reads live IMU data (accelerometer, gyroscope, attitude) from
    the flight controller over MAVLink and verifies sensor health
    before flight. Also guides through the accelerometer calibration
    positions required by ArduCopter.

Usage:
    python imu_calibration.py --connect /dev/ttyUSB0 --baud 57600
    python imu_calibration.py --connect tcp:127.0.0.1:5760  # SITL

Dependencies:
    pip install dronekit pymavlink
"""

import time
import argparse
from dronekit import connect


# Thresholds for healthy IMU readings at rest
GYRO_THRESHOLD_DEG_S = 2.0      # max drift at rest (deg/s)
ACCEL_EARTH_G = 9.81
ACCEL_TOLERANCE_MS2 = 1.5       # tolerance around 1g on vertical axis


def parse_args():
    parser = argparse.ArgumentParser(description="IMU Preflight Check")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760",
                        help="Connection string")
    parser.add_argument("--baud", type=int, default=57600,
                        help="Serial baud rate")
    parser.add_argument("--duration", type=int, default=5,
                        help="Sampling duration in seconds")
    return parser.parse_args()


def check_attitude(vehicle):
    """Read and evaluate current attitude (roll, pitch, yaw)."""
    attitude = vehicle.attitude
    roll_deg  = round(attitude.roll  * 57.2958, 2)
    pitch_deg = round(attitude.pitch * 57.2958, 2)
    yaw_deg   = round(attitude.yaw   * 57.2958, 2)

    print(f"\n[ATTITUDE]")
    print(f"  Roll  : {roll_deg:+7.2f} °")
    print(f"  Pitch : {pitch_deg:+7.2f} °")
    print(f"  Yaw   : {yaw_deg:+7.2f} °")

    roll_ok  = abs(roll_deg)  < 5.0
    pitch_ok = abs(pitch_deg) < 5.0

    print(f"  Roll  {'✓ LEVEL' if roll_ok  else '✗ NOT LEVEL — place on flat surface'}")
    print(f"  Pitch {'✓ LEVEL' if pitch_ok else '✗ NOT LEVEL — place on flat surface'}")

    return roll_ok and pitch_ok


def check_gyro(vehicle, duration: int):
    """Sample gyro data and check for excessive drift at rest."""
    print(f"\n[GYROSCOPE] Sampling for {duration}s — keep vehicle STATIONARY...")

    max_roll_rate  = 0.0
    max_pitch_rate = 0.0
    max_yaw_rate   = 0.0

    start = time.time()
    while time.time() - start < duration:
        v = vehicle.attitude
        roll_rate  = abs(v.rollspeed  * 57.2958)
        pitch_rate = abs(v.pitchspeed * 57.2958)
        yaw_rate   = abs(v.yawspeed   * 57.2958)

        max_roll_rate  = max(max_roll_rate,  roll_rate)
        max_pitch_rate = max(max_pitch_rate, pitch_rate)
        max_yaw_rate   = max(max_yaw_rate,   yaw_rate)
        time.sleep(0.1)

    print(f"  Max roll rate  : {max_roll_rate:.3f} °/s  "
          f"{'✓' if max_roll_rate  < GYRO_THRESHOLD_DEG_S else '✗ HIGH — recalibrate gyro'}")
    print(f"  Max pitch rate : {max_pitch_rate:.3f} °/s  "
          f"{'✓' if max_pitch_rate < GYRO_THRESHOLD_DEG_S else '✗ HIGH — recalibrate gyro'}")
    print(f"  Max yaw rate   : {max_yaw_rate:.3f} °/s  "
          f"{'✓' if max_yaw_rate   < GYRO_THRESHOLD_DEG_S else '✗ HIGH — recalibrate gyro'}")

    return all(r < GYRO_THRESHOLD_DEG_S for r in
               [max_roll_rate, max_pitch_rate, max_yaw_rate])


def check_vibration(vehicle):
    """Read vibration levels reported by ArduCopter EKF."""
    vibe = vehicle.vibration
    if vibe is None:
        print("\n[VIBRATION] Data not available (bench test / SITL)")
        return True

    print(f"\n[VIBRATION]")
    print(f"  X: {vibe.vibration_x:.3f}  {'✓' if vibe.vibration_x < 30 else '✗ HIGH'}")
    print(f"  Y: {vibe.vibration_y:.3f}  {'✓' if vibe.vibration_y < 30 else '✗ HIGH'}")
    print(f"  Z: {vibe.vibration_z:.3f}  {'✓' if vibe.vibration_z < 30 else '✗ HIGH'}")
    print("  (Values < 30 m/s² considered acceptable for flight)")

    return all(v < 30 for v in
               [vibe.vibration_x, vibe.vibration_y, vibe.vibration_z])


def print_calibration_guide():
    """Print ArduCopter accel calibration position instructions."""
    positions = [
        ("Level",         "Place drone flat on ground, props up"),
        ("On Left Side",  "Roll 90° — left side down"),
        ("On Right Side", "Roll 90° — right side down"),
        ("Nose Down",     "Pitch 90° — nose pointing down"),
        ("Nose Up",       "Pitch 90° — nose pointing up"),
        ("Upside Down",   "Flip completely — props facing ground"),
    ]

    print("\n[ACCEL CALIBRATION GUIDE]")
    print("  In Mission Planner → Initial Setup → Mandatory Hardware → Accel Calibration")
    print("  Place the drone in each position when prompted:\n")
    for i, (pos, desc) in enumerate(positions, 1):
        print(f"  Step {i}: {pos:15s} — {desc}")
    print("\n  Click 'Calibrate Accel' in Mission Planner and follow on-screen prompts.")


def summarize(checks: dict):
    print("\n" + "=" * 50)
    print("  IMU PREFLIGHT CHECK SUMMARY")
    print("=" * 50)
    all_pass = True
    for name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {name:20s}: {status}")
        if not result:
            all_pass = False

    print("=" * 50)
    if all_pass:
        print("  ✅ All IMU checks PASSED — safe to proceed to arming.")
    else:
        print("  ❌ Some checks FAILED — resolve issues before flight.")
    print("=" * 50)


def main():
    args = parse_args()

    print("=" * 55)
    print("  IMU Preflight Check — CDAC Noida UAS Project")
    print("=" * 55)
    print(f"\nConnecting to: {args.connect} ...")

    vehicle = connect(args.connect, baud=args.baud, wait_ready=True)
    print(f"  Connected. Firmware: {vehicle.version}\n")

    try:
        checks = {}
        checks["Attitude (Level)"]  = check_attitude(vehicle)
        checks["Gyro Drift"]        = check_gyro(vehicle, args.duration)
        checks["Vibration"]         = check_vibration(vehicle)
        print_calibration_guide()
        summarize(checks)
    except KeyboardInterrupt:
        print("\n[ABORTED] IMU check interrupted.")
    finally:
        vehicle.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    main()
