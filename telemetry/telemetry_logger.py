#!/usr/bin/env python3
"""
telemetry_logger.py
-------------------
Logs real-time MAVLink telemetry from the hexacopter to a CSV file.
Captures: timestamp, altitude, roll, pitch, yaw, airspeed, groundspeed,
          battery voltage/current, GPS lat/lon, satellites, mode.

Usage:
    python telemetry_logger.py --connect /dev/ttyUSB0 --output flight_log.csv
    python telemetry_logger.py --connect tcp:127.0.0.1:5760

Author: Arpit | CDAC Noida UAS Internship 2025
"""

import argparse
import csv
import time
import sys
import os
from datetime import datetime
from dronekit import connect


def parse_args():
    parser = argparse.ArgumentParser(description="Flight Telemetry Logger")
    parser.add_argument("--connect",   default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud",      type=int, default=57600)
    parser.add_argument("--output",    default="",
                        help="Output CSV filename (auto-named if not specified)")
    parser.add_argument("--interval",  type=float, default=0.5,
                        help="Logging interval in seconds (default: 0.5)")
    return parser.parse_args()


FIELDS = [
    "timestamp", "elapsed_s",
    "alt_rel_m", "alt_abs_m",
    "roll_deg", "pitch_deg", "yaw_deg",
    "groundspeed_ms", "airspeed_ms",
    "battery_v", "battery_a", "battery_pct",
    "lat", "lon",
    "gps_fix", "satellites",
    "mode", "armed"
]


def collect_row(vehicle, start_time):
    att  = vehicle.attitude
    loc  = vehicle.location
    gps  = vehicle.gps_0
    bat  = vehicle.battery
    now  = datetime.utcnow().isoformat()
    return {
        "timestamp":      now,
        "elapsed_s":      round(time.time() - start_time, 2),
        "alt_rel_m":      round(loc.global_relative_frame.alt or 0, 3),
        "alt_abs_m":      round(loc.global_frame.alt or 0, 3),
        "roll_deg":       round(att.roll  * 57.296, 3),
        "pitch_deg":      round(att.pitch * 57.296, 3),
        "yaw_deg":        round(att.yaw   * 57.296, 3),
        "groundspeed_ms": round(vehicle.groundspeed or 0, 3),
        "airspeed_ms":    round(vehicle.airspeed or 0, 3),
        "battery_v":      round(bat.voltage  or 0, 3),
        "battery_a":      round(bat.current  or 0, 3),
        "battery_pct":    bat.level,
        "lat":            loc.global_frame.lat,
        "lon":            loc.global_frame.lon,
        "gps_fix":        gps.fix_type,
        "satellites":     gps.satellites_visible,
        "mode":           vehicle.mode.name,
        "armed":          vehicle.armed,
    }


def main():
    args = parse_args()

    output_file = args.output or f"flight_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    print("\n================================")
    print("  TELEMETRY LOGGER")
    print("================================")
    print(f"[*] Connecting to {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print(f"[*] Connected. Logging to: {output_file}")
    print("[*] Press Ctrl+C to stop.\n")

    start_time = time.time()
    row_count  = 0

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        try:
            while True:
                row = collect_row(vehicle, start_time)
                writer.writerow(row)
                f.flush()
                row_count += 1
                print(f"  [{row['elapsed_s']:>7.1f}s] "
                      f"Alt={row['alt_rel_m']:.1f}m  "
                      f"Roll={row['roll_deg']:+.1f}  "
                      f"Pitch={row['pitch_deg']:+.1f}  "
                      f"Bat={row['battery_v']:.2f}V  "
                      f"Mode={row['mode']}", end="\r")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print(f"\n\n[*] Stopped. {row_count} rows saved to {output_file}")

    vehicle.close()


if __name__ == "__main__":
    main()
