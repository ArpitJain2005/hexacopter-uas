#!/usr/bin/env python3

import argparse
import time
import math
import sys
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from pymavlink import mavutil


def parse_args():
    parser = argparse.ArgumentParser(description="Waypoint Navigation Mission")
    parser.add_argument("--connect",  default="tcp:127.0.0.1:5760")
    parser.add_argument("--baud",     type=int,   default=57600)
    parser.add_argument("--altitude", type=float, default=5.0)
    parser.add_argument("--radius",   type=float, default=10.0,
                        help="Square size in metres (default: 10m)")
    return parser.parse_args()


def get_distance_metres(loc1, loc2):
    """Approximate distance between two LocationGlobalRelative objects."""
    dlat = loc2.lat - loc1.lat
    dlon = loc2.lon - loc1.lon
    return math.sqrt((dlat * 1.113195e5)**2 + (dlon * 1.113195e5 * math.cos(math.radians(loc1.lat)))**2)


def offset_location(home, dNorth, dEast, alt):
    """Offset from home position in metres North and East."""
    earth_radius = 6378137.0
    dLat = dNorth / earth_radius
    dLon = dEast  / (earth_radius * math.cos(math.radians(home.lat)))
    return LocationGlobalRelative(
        home.lat + math.degrees(dLat),
        home.lon + math.degrees(dLon),
        alt
    )


def upload_mission(vehicle, home, altitude, radius):
    """Build and upload a square waypoint mission."""
    cmds = vehicle.commands
    cmds.clear()

    # Takeoff command
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                     0, 0, 0, 0, 0, 0, 0, 0, altitude))

    # 4 waypoints — square pattern
    corners = [
        ( radius,  0),
        ( radius,  radius),
        ( 0,       radius),
        ( 0,       0),
    ]
    for dN, dE in corners:
        wp = offset_location(home, dN, dE, altitude)
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                         mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                         0, 0, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt))

    # RTL dummy waypoint
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                     mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                     0, 0, 0, 0, 0, 0, 0, 0, 0))

    cmds.upload()
    print(f"[*] Uploaded mission: takeoff + {len(corners)} waypoints + RTL")


def arm_and_takeoff(vehicle, altitude):
    while not vehicle.is_armable:
        print("  Waiting for armable state...")
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode.name != "GUIDED":
        time.sleep(0.5)
    vehicle.armed = True
    while not vehicle.armed:
        time.sleep(1)
    print("[OK] Armed. Taking off...")
    vehicle.simple_takeoff(altitude)
    while vehicle.location.global_relative_frame.alt < altitude * 0.95:
        print(f"  Alt: {vehicle.location.global_relative_frame.alt:.1f}m", end="\r")
        time.sleep(0.5)
    print(f"\n[OK] Altitude reached: {vehicle.location.global_relative_frame.alt:.1f}m")


def run_mission(vehicle):
    print("[*] Starting AUTO mission...")
    vehicle.mode = VehicleMode("AUTO")
    vehicle.commands.next = 0

    nextwaypoint = vehicle.commands.next
    while True:
        nextwaypoint = vehicle.commands.next
        print(f"  Waypoint: {nextwaypoint} | "
              f"Alt: {vehicle.location.global_relative_frame.alt:.1f}m | "
              f"Mode: {vehicle.mode.name}", end="\r")
        if vehicle.mode.name == "RTL":
            print("\n[*] RTL mode detected — mission complete.")
            break
        time.sleep(1)


def main():
    args = parse_args()
    print("\n====================================")
    print("  HEXACOPTER WAYPOINT MISSION")
    print("====================================")
    print(f"\n[*] Connecting to {args.connect} ...")
    try:
        vehicle = connect(args.connect, baud=args.baud, wait_ready=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print(f"[*] Connected | Home: {vehicle.home_location}")
    home = vehicle.location.global_relative_frame

    try:
        upload_mission(vehicle, home, args.altitude, args.radius)
        arm_and_takeoff(vehicle, args.altitude)
        run_mission(vehicle)
        print("[OK] Mission finished. Waiting for landing...")
        while vehicle.armed:
            time.sleep(1)
        print("[OK] Landed and disarmed.")
    except KeyboardInterrupt:
        print("\n[!] Interrupted -- RTL.")
        vehicle.mode = VehicleMode("RTL")
    finally:
        vehicle.close()
        print("[*] Done.\n")


if __name__ == "__main__":
    main()
