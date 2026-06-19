

import time
import argparse
from dronekit import connect


# ArduCopter GPS thresholds for flight readiness
MIN_SATELLITES   = 6
MAX_HDOP         = 2.0          # Horizontal Dilution of Precision
MIN_FIX_TYPE     = 3            # 3 = 3D fix, 4 = DGPS, 5 = RTK float, 6 = RTK fixed

GPS_FIX_LABELS = {
    0: "No GPS",
    1: "No Fix",
    2: "2D Fix",
    3: "3D Fix ✓",
    4: "DGPS",
    5: "RTK Float",
    6: "RTK Fixed",
}


def parse_args():
    parser = argparse.ArgumentParser(description="GPS Health Check")
    parser.add_argument("--connect", default="tcp:127.0.0.1:5760",
                        help="MAVLink connection string")
    parser.add_argument("--baud", type=int, default=57600,
                        help="Serial baud rate")
    parser.add_argument("--wait", action="store_true",
                        help="Keep monitoring until GPS lock is achieved")
    parser.add_argument("--timeout", type=int, default=120,
                        help="Max wait time in seconds (default: 120)")
    return parser.parse_args()


def print_gps_status(vehicle):
    """Print current GPS status and return True if ready for flight."""
    gps = vehicle.gps_0
    loc = vehicle.location.global_frame

    fix_type   = gps.fix_type
    satellites = gps.satellites_visible
    hdop       = gps.eph / 100.0 if gps.eph else None  # eph in cm, convert to m

    fix_label = GPS_FIX_LABELS.get(fix_type, f"Unknown ({fix_type})")

    print(f"\n[GPS STATUS]")
    print(f"  Fix Type      : {fix_label} (type {fix_type})")
    print(f"  Satellites    : {satellites}  {'✓' if satellites >= MIN_SATELLITES else '✗ (need ≥ 6)'}")

    if hdop is not None:
        hdop_str = f"{hdop:.2f}"
        hdop_ok  = hdop <= MAX_HDOP
        print(f"  HDOP          : {hdop_str}  {'✓' if hdop_ok else '✗ (need ≤ 2.0)'}")
    else:
        hdop_ok = False
        print(f"  HDOP          : N/A")

    if loc.lat and loc.lon:
        print(f"  Latitude      : {loc.lat:.6f} °")
        print(f"  Longitude     : {loc.lon:.6f} °")
        print(f"  Altitude      : {loc.alt:.1f} m (MSL)")
    else:
        print(f"  Position      : Not available yet")

    fix_ok = fix_type >= MIN_FIX_TYPE
    sats_ok = satellites >= MIN_SATELLITES

    flight_ready = fix_ok and sats_ok and hdop_ok
    print(f"\n  GPS Flight Ready: {'✅ YES' if flight_ready else '❌ NO — waiting for lock...'}")

    return flight_ready


def wait_for_gps_lock(vehicle, timeout: int):
    """Poll GPS status until lock is achieved or timeout expires."""
    print(f"\n[WAITING] Polling for GPS lock (timeout: {timeout}s)...")
    start = time.time()

    while time.time() - start < timeout:
        elapsed = int(time.time() - start)
        ready = print_gps_status(vehicle)
        if ready:
            print(f"\n✅ GPS lock achieved in {elapsed}s!")
            return True
        print(f"  [{elapsed}s elapsed] Retrying in 5s...")
        time.sleep(5)

    print(f"\n❌ GPS lock NOT achieved within {timeout}s.")
    print("   Check antenna placement and sky visibility.")
    return False


def check_ekf_status(vehicle):
    """Check EKF (Extended Kalman Filter) health flags."""
    ekf = vehicle.ekf_ok
    print(f"\n[EKF STATUS]")
    print(f"  EKF OK: {'✓ Healthy' if ekf else '✗ EKF not ready — do not fly'}")
    return ekf


def main():
    args = parse_args()

    print("=" * 55)
    print("  GPS Health Check — CDAC Noida UAS Project")
    print("=" * 55)
    print(f"\nConnecting to: {args.connect} ...")

    vehicle = connect(args.connect, baud=args.baud, wait_ready=True)
    print(f"  Connected. Firmware: {vehicle.version}")

    try:
        if args.wait:
            gps_ready = wait_for_gps_lock(vehicle, args.timeout)
        else:
            gps_ready = print_gps_status(vehicle)

        ekf_ready = check_ekf_status(vehicle)

        print("\n" + "=" * 50)
        print("  GPS PREFLIGHT SUMMARY")
        print("=" * 50)
        print(f"  GPS Lock : {'✓ PASS' if gps_ready else '✗ FAIL'}")
        print(f"  EKF OK   : {'✓ PASS' if ekf_ready else '✗ FAIL'}")
        print("=" * 50)

        if gps_ready and ekf_ready:
            print("  ✅ GPS ready. Safe to arm and fly.")
        else:
            print("  ❌ Not ready. Resolve issues before flight.")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n[ABORTED] GPS check interrupted.")
    finally:
        vehicle.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    main()
