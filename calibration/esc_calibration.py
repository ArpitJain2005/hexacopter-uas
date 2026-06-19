

import time
import argparse
from dronekit import connect, VehicleMode
from pymavlink import mavutil


def parse_args():
    parser = argparse.ArgumentParser(description="ESC Calibration Script")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760",
                        help="Connection string (e.g. /dev/ttyUSB0 or tcp:127.0.0.1:5760)")
    parser.add_argument("--baud", type=int, default=57600,
                        help="Baud rate for serial connection")
    return parser.parse_args()


def set_rc_channel_pwm(vehicle, channel_id: int, pwm: int):
    """
    Send a PWM value override to a specific RC channel.
    channel_id: 1–8
    pwm: 1000 (min) to 2000 (max)
    """
    if channel_id < 1 or channel_id > 8:
        raise ValueError("Channel ID must be between 1 and 8")

    rc_channel_values = [65535] * 8  # 65535 = no override
    rc_channel_values[channel_id - 1] = pwm

    vehicle.channels.overrides = {str(channel_id): pwm}


def send_throttle(vehicle, pwm: int):
    """Override throttle channel (channel 3) with given PWM."""
    vehicle.channels.overrides['3'] = pwm
    print(f"  Throttle PWM set to: {pwm}")


def release_overrides(vehicle):
    """Release all RC overrides."""
    vehicle.channels.overrides = {}
    print("  RC overrides released.")


def esc_calibration(vehicle):
    """
    ESC calibration sequence:
    1. Set throttle to maximum (2000 µs)
    2. Wait for ESCs to register high signal (beep sequence)
    3. Set throttle to minimum (1000 µs)
    4. Wait for ESCs to complete calibration (beep confirmation)
    5. Release overrides
    """
    print("\n[ESC CALIBRATION] Starting procedure...")
    print("  Ensure props are REMOVED and vehicle is on bench.\n")

    input("  Press ENTER to begin (or Ctrl+C to abort): ")

    # Step 1: Set mode to STABILIZE (disarmed)
    print("\n[1/5] Setting mode to STABILIZE...")
    vehicle.mode = VehicleMode("STABILIZE")
    time.sleep(1)

    # Step 2: Max throttle
    print("[2/5] Sending MAXIMUM throttle (2000 µs)...")
    print("      Listen for ESC startup beeps...")
    send_throttle(vehicle, 2000)
    time.sleep(4)  # ESCs signal they've registered high point

    # Step 3: Min throttle
    print("[3/5] Sending MINIMUM throttle (1000 µs)...")
    print("      Listen for ESC calibration-complete beeps...")
    send_throttle(vehicle, 1000)
    time.sleep(4)

    # Step 4: Release
    print("[4/5] Releasing overrides...")
    release_overrides(vehicle)
    time.sleep(1)

    print("[5/5] ESC calibration complete.")
    print("      Motors should now respond uniformly to throttle input.")


def verify_motor_outputs(vehicle):
    """
    Print current RC channel values and servo outputs for verification.
    """
    print("\n[VERIFICATION] Current RC channel inputs:")
    for ch, val in vehicle.channels.items():
        print(f"  Channel {ch}: {val} µs")

    print("\n[VERIFICATION] Current servo/motor outputs:")
    for i in range(1, 7):
        key = f"servofunction{i}"
        print(f"  Output {i}: Check Mission Planner → Servo Output tab for live values")


def main():
    args = parse_args()

    print("=" * 55)
    print("  Hexacopter ESC Calibration — CDAC Noida UAS Project")
    print("=" * 55)
    print(f"\nConnecting to vehicle at: {args.connect}")

    vehicle = connect(args.connect, baud=args.baud, wait_ready=True)

    print(f"  Vehicle connected. Firmware: {vehicle.version}")
    print(f"  Mode: {vehicle.mode.name} | Armed: {vehicle.armed}")

    if vehicle.armed:
        print("\n[ERROR] Vehicle is ARMED. Disarm before calibration.")
        vehicle.close()
        return

    try:
        esc_calibration(vehicle)
        verify_motor_outputs(vehicle)
    except KeyboardInterrupt:
        print("\n[ABORTED] Calibration interrupted by user.")
        release_overrides(vehicle)
    finally:
        vehicle.close()
        print("\nConnection closed. ESC calibration session ended.")


if __name__ == "__main__":
    main()
