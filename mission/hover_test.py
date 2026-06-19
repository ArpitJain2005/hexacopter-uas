

import time
import argparse
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


# --- Configuration ---
DEFAULT_ALTITUDE_M  = 3.0    # Target hover altitude (metres AGL)
DEFAULT_HOVER_SEC   = 15     # Duration to hold hover (seconds)
ARM_TIMEOUT_SEC     = 30     # Max time to wait for arming
TAKEOFF_TIMEOUT_SEC = 30     # Max time to wait to reach target alt
ALT_REACH_THRESH    = 0.95   # Fraction of target alt to consider "reached"


def parse_args():
    parser = argparse.ArgumentParser(description="Hexacopter Hover Test")
    parser.add_argument("--connect",  default="tcp:127.0.0.1:5760",
                        help="MAVLink connection string")
    parser.add_argument("--baud",     type=int, default=57600)
    parser.add_argument("--altitude", type=float, default=DEFAULT_ALTITUDE_M,
                        help=f"Target hover altitude in metres (default: {DEFAULT_ALTITUDE_M})")
    parser.add_argument("--hover",    type=int, default=DEFAULT_HOVER_SEC,
                        help=f"Hover duration in seconds (default: {DEFAULT_HOVER_SEC})")
    return parser.parse_args()


# ─────────────────────────────────────────
# Pre-flight Checks
# ─────────────────────────────────────────

def preflight_checks(vehicle) -> bool:
    """Run preflight checks. Returns True if all pass."""
    print("\n[PREFLIGHT CHECKS]")
    checks = {}

    # GPS
    gps = vehicle.gps_0
    gps_ok = (gps.fix_type >= 3 and gps.satellites_visible >= 6)
    checks["GPS Lock"]   = gps_ok
    print(f"  GPS        : fix={gps.fix_type}  sats={gps.satellites_visible}  "
          f"{'✓' if gps_ok else '✗'}")

    # EKF
    ekf_ok = vehicle.ekf_ok
    checks["EKF Health"] = ekf_ok
    print(f"  EKF        : {'✓ OK' if ekf_ok else '✗ NOT READY'}")

    # Battery
    bat = vehicle.battery
    bat_ok = bat.voltage is None or bat.voltage > 14.0   # skip if no sensor in SITL
    checks["Battery"]    = bat_ok
    print(f"  Battery    : {bat.voltage}V  {'✓' if bat_ok else '✗ LOW'}")

    # Attitude (level)
    att = vehicle.attitude
    level_ok = abs(att.roll * 57.3) < 5 and abs(att.pitch * 57.3) < 5
    checks["Level"]      = level_ok
    print(f"  Level      : roll={att.roll*57.3:+.1f}°  pitch={att.pitch*57.3:+.1f}°  "
          f"{'✓' if level_ok else '✗ NOT LEVEL'}")

    all_ok = all(checks.values())
    print(f"\n  Overall    : {'✅ ALL PASS' if all_ok else '❌ FAILED — aborting'}")
    return all_ok


# ─────────────────────────────────────────
# Arming
# ─────────────────────────────────────────

def arm_vehicle(vehicle) -> bool:
    """Switch to GUIDED mode and arm. Returns True on success."""
    print("\n[ARMING]")
    print("  Setting mode to GUIDED...")
    vehicle.mode = VehicleMode("GUIDED")

    timeout = time.time() + 10
    while vehicle.mode.name != "GUIDED" and time.time() < timeout:
        time.sleep(0.5)

    if vehicle.mode.name != "GUIDED":
        print("  ✗ Failed to set GUIDED mode.")
        return False

    print("  Arming motors...")
    vehicle.armed = True

    timeout = time.time() + ARM_TIMEOUT_SEC
    while not vehicle.armed and time.time() < timeout:
        print("    Waiting for arm...")
        time.sleep(1)

    if vehicle.armed:
        print("  ✓ Vehicle ARMED.")
        return True
    else:
        print("  ✗ Arming timed out.")
        return False


# ─────────────────────────────────────────
# Takeoff
# ─────────────────────────────────────────

def takeoff(vehicle, target_alt: float) -> bool:
    """Command takeoff to target_alt metres AGL."""
    print(f"\n[TAKEOFF] Climbing to {target_alt}m AGL...")
    vehicle.simple_takeoff(target_alt)

    timeout = time.time() + TAKEOFF_TIMEOUT_SEC
    while time.time() < timeout:
        alt = vehicle.location.global_relative_frame.alt
        print(f"  Current altitude: {alt:.2f}m")
        if alt >= target_alt * ALT_REACH_THRESH:
            print(f"  ✓ Target altitude reached: {alt:.2f}m")
            return True
        time.sleep(1)

    print(f"  ✗ Takeoff timed out. Last alt: "
          f"{vehicle.location.global_relative_frame.alt:.2f}m")
    return False


# ─────────────────────────────────────────
# Hover
# ─────────────────────────────────────────

def hover(vehicle, duration: int):
    """Hold hover position for given duration, logging telemetry."""
    print(f"\n[HOVER] Holding position for {duration}s...")
    print(f"  {'Time':>5}  {'Alt(m)':>8}  {'Roll°':>7}  {'Pitch°':>7}  {'Yaw°':>7}  {'Sats':>5}")
    print("  " + "-" * 50)

    for elapsed in range(duration):
        alt   = vehicle.location.global_relative_frame.alt
        att   = vehicle.attitude
        gps   = vehicle.gps_0
        roll  = att.roll  * 57.2958
        pitch = att.pitch * 57.2958
        yaw   = att.yaw   * 57.2958

        print(f"  {elapsed:>5}s  {alt:>8.2f}  {roll:>+7.1f}  {pitch:>+7.1f}  {yaw:>+7.1f}  "
              f"{gps.satellites_visible:>5}")
        time.sleep(1)

    print("  ✓ Hover complete.")


# ─────────────────────────────────────────
# Land / RTL
# ─────────────────────────────────────────

def return_to_launch(vehicle):
    """Command RTL mode."""
    print("\n[RTL] Returning to launch point...")
    vehicle.mode = VehicleMode("RTL")

    while vehicle.armed:
        alt = vehicle.location.global_relative_frame.alt
        print(f"  Descending... altitude: {alt:.2f}m")
        if alt < 0.3:
            break
        time.sleep(2)

    print("  ✓ Landed and disarmed.")


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────

def main():
    args = parse_args()

    print("=" * 60)
    print("  Hexacopter Hover Test — CDAC Noida UAS Project")
    print("=" * 60)
    print(f"  Target altitude : {args.altitude}m")
    print(f"  Hover duration  : {args.hover}s")
    print(f"  Connection      : {args.connect}")

    print(f"\nConnecting...")
    vehicle = connect(args.connect, baud=args.baud, wait_ready=True)
    print(f"  Connected. Firmware: {vehicle.version}")

    try:
        # 1. Pre-flight checks
        if not preflight_checks(vehicle):
            print("\n[ABORT] Pre-flight checks failed.")
            return

        input("\n  Pre-flight checks PASSED. Press ENTER to arm and takeoff (Ctrl+C to abort): ")

        # 2. Arm
        if not arm_vehicle(vehicle):
            print("\n[ABORT] Failed to arm.")
            return

        # 3. Takeoff
        if not takeoff(vehicle, args.altitude):
            print("\n[ABORT] Takeoff failed. Initiating RTL...")
            return_to_launch(vehicle)
            return

        # 4. Hover
        hover(vehicle, args.hover)

        # 5. RTL
        return_to_launch(vehicle)

    except KeyboardInterrupt:
        print("\n[EMERGENCY] User interrupt — switching to RTL.")
        vehicle.mode = VehicleMode("RTL")

    finally:
        vehicle.close()
        print("\nConnection closed. Mission complete.")


if __name__ == "__main__":
    main()
