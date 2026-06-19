

import time
import argparse
import csv
import os
from datetime import datetime
from dronekit import connect, VehicleMode


HEADER = """
╔══════════════════════════════════════════════════════════╗
║      HEXACOPTER UAS — GROUND CONTROL TELEMETRY          ║
║             CDAC Noida | Arpit Jain                     ║
╚══════════════════════════════════════════════════════════╝
"""


def parse_args():
    parser = argparse.ArgumentParser(description="Real-Time Telemetry Monitor")
    parser.add_argument("--connect",  default="tcp:127.0.0.1:5760",
                        help="MAVLink connection string")
    parser.add_argument("--baud",     type=int, default=57600)
    parser.add_argument("--interval", type=float, default=1.0,
                        help="Refresh interval in seconds")
    parser.add_argument("--log",      action="store_true",
                        help="Log telemetry to CSV file")
    return parser.parse_args()


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def get_fix_label(fix_type: int) -> str:
    return {0: "No GPS", 1: "No Fix", 2: "2D", 3: "3D ✓",
            4: "DGPS ✓", 5: "RTK~✓", 6: "RTK ✓"}.get(fix_type, "?")


def get_mode_color(mode: str) -> str:
    """Return a status indicator for the flight mode."""
    safe_modes   = {"STABILIZE", "LOITER", "GUIDED", "AUTO", "POSHOLD"}
    caution_modes = {"ALT_HOLD", "DRIFT"}
    if mode in safe_modes:
        return "●"   # Active / normal
    elif mode in caution_modes:
        return "◐"
    else:
        return "○"


def format_dashboard(vehicle, elapsed_sec: int) -> str:
    """Build the telemetry dashboard string."""
    att  = vehicle.attitude
    loc  = vehicle.location.global_relative_frame
    gps  = vehicle.gps_0
    bat  = vehicle.battery
    airspeed = vehicle.airspeed
    groundspeed = vehicle.groundspeed
    mode = vehicle.mode.name
    armed = "ARMED 🔴" if vehicle.armed else "DISARMED 🟢"
    ekf  = "✓ OK" if vehicle.ekf_ok else "✗ FAIL"

    roll  = att.roll  * 57.2958
    pitch = att.pitch * 57.2958
    yaw   = att.yaw   * 57.2958

    bat_v = f"{bat.voltage:.2f}V" if bat.voltage else "N/A"
    bat_a = f"{bat.current:.1f}A" if bat.current else "N/A"
    bat_p = f"{bat.level}%" if bat.level else "N/A"

    hdop = gps.eph / 100.0 if gps.eph else 0.0

    lines = [
        HEADER,
        f"  Time Elapsed  : {elapsed_sec:>6}s          {datetime.now().strftime('%H:%M:%S')}",
        f"  Mode          : {get_mode_color(mode)} {mode:<12}    Status: {armed}",
        "",
        "  ┌─── ATTITUDE ──────────────────────────────┐",
        f"  │  Roll   : {roll:>+8.2f} °                      │",
        f"  │  Pitch  : {pitch:>+8.2f} °                      │",
        f"  │  Yaw    : {yaw:>+8.2f} °                      │",
        "  └───────────────────────────────────────────┘",
        "",
        "  ┌─── GPS ───────────────────────────────────┐",
        f"  │  Fix     : {get_fix_label(gps.fix_type):<8}  Sats: {gps.satellites_visible:<4}       │",
        f"  │  HDOP    : {hdop:<8.2f}                        │",
        f"  │  Lat     : {loc.lat:.6f} °                 │" if loc.lat else
        "  │  Lat     : N/A                            │",
        f"  │  Lon     : {loc.lon:.6f} °                 │" if loc.lon else
        "  │  Lon     : N/A                            │",
        f"  │  Alt AGL : {loc.alt:>8.2f} m                    │",
        "  └───────────────────────────────────────────┘",
        "",
        "  ┌─── VELOCITY & POWER ──────────────────────┐",
        f"  │  Airspeed  : {airspeed:>6.2f} m/s                    │",
        f"  │  Groundspd : {groundspeed:>6.2f} m/s                    │",
        f"  │  Battery V : {bat_v:>8}                      │",
        f"  │  Battery A : {bat_a:>8}                      │",
        f"  │  Battery % : {bat_p:>8}                      │",
        "  └───────────────────────────────────────────┘",
        "",
        f"  EKF Health  : {ekf}",
        "",
        "  Press Ctrl+C to exit",
    ]

    return "\n".join(lines)


def get_telemetry_row(vehicle, elapsed: int) -> dict:
    """Return a dict of current telemetry for CSV logging."""
    att = vehicle.attitude
    loc = vehicle.location.global_relative_frame
    gps = vehicle.gps_0
    bat = vehicle.battery
    return {
        "timestamp":    datetime.now().isoformat(),
        "elapsed_s":    elapsed,
        "mode":         vehicle.mode.name,
        "armed":        vehicle.armed,
        "roll_deg":     round(att.roll  * 57.2958, 3),
        "pitch_deg":    round(att.pitch * 57.2958, 3),
        "yaw_deg":      round(att.yaw   * 57.2958, 3),
        "alt_agl_m":    round(loc.alt,  2) if loc.alt else None,
        "lat":          loc.lat,
        "lon":          loc.lon,
        "gps_fix":      gps.fix_type,
        "satellites":   gps.satellites_visible,
        "hdop":         round(gps.eph / 100.0, 2) if gps.eph else None,
        "airspeed_ms":  round(vehicle.airspeed, 2),
        "groundspeed":  round(vehicle.groundspeed, 2),
        "bat_voltage":  bat.voltage,
        "bat_current":  bat.current,
        "bat_level":    bat.level,
        "ekf_ok":       vehicle.ekf_ok,
    }


def main():
    args = parse_args()

    print(HEADER)
    print(f"Connecting to {args.connect} ...")
    vehicle = connect(args.connect, baud=args.baud, wait_ready=True)
    print(f"Connected. Firmware: {vehicle.version}\n")

    log_file = None
    writer   = None

    if args.log:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"telemetry_{ts}.csv"
        log_file = open(log_path, "w", newline="")
        sample = get_telemetry_row(vehicle, 0)
        writer = csv.DictWriter(log_file, fieldnames=sample.keys())
        writer.writeheader()
        print(f"Logging to: {log_path}")

    start = time.time()
    try:
        while True:
            elapsed = int(time.time() - start)
            clear()
            print(format_dashboard(vehicle, elapsed))

            if writer:
                row = get_telemetry_row(vehicle, elapsed)
                writer.writerow(row)
                if log_file:
                    log_file.flush()

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n\nTelemetry monitor stopped.")
    finally:
        if log_file:
            log_file.close()
            print(f"Log saved.")
        vehicle.close()


if __name__ == "__main__":
    main()
