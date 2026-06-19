#!/usr/bin/env python3


import argparse
import csv
import sys
import os

try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
except ImportError:
    print("[ERROR] matplotlib not found. Install with: pip install matplotlib")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Plot Flight Telemetry")
    parser.add_argument("--log", required=True, help="Path to CSV log file")
    parser.add_argument("--save", default="", help="Save plot to file instead of showing")
    return parser.parse_args()


def load_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def extract(rows, key, cast=float):
    return [cast(r[key]) for r in rows if r[key] not in ("", "None", None)]


def plot(rows, save_path=""):
    t   = extract(rows, "elapsed_s")
    alt = extract(rows, "alt_rel_m")
    rol = extract(rows, "roll_deg")
    pit = extract(rows, "pitch_deg")
    yaw = extract(rows, "yaw_deg")
    bat = extract(rows, "battery_v")
    lat = extract(rows, "lat")
    lon = extract(rows, "lon")

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("Hexacopter Flight Telemetry", fontsize=14, fontweight="bold")
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.35)

    # Altitude
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t[:len(alt)], alt, color="royalblue", linewidth=1.5)
    ax1.set_title("Altitude (Relative)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Altitude (m)")
    ax1.grid(True, alpha=0.3)

    # Roll & Pitch
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t[:len(rol)], rol, label="Roll",  color="tomato",    linewidth=1.2)
    ax2.plot(t[:len(pit)], pit, label="Pitch", color="goldenrod", linewidth=1.2)
    ax2.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax2.set_title("Roll & Pitch")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Angle (deg)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Yaw
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(t[:len(yaw)], yaw, color="mediumorchid", linewidth=1.5)
    ax3.set_title("Yaw (Heading)")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Yaw (deg)")
    ax3.grid(True, alpha=0.3)

    # Battery
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(t[:len(bat)], bat, color="seagreen", linewidth=1.5)
    ax4.axhline(14.0, color="red", linewidth=0.8, linestyle="--", label="Failsafe 14V")
    ax4.set_title("Battery Voltage")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Voltage (V)")
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # GPS Track
    ax5 = fig.add_subplot(gs[2, :])
    if lat and lon:
        ax5.plot(lon, lat, color="steelblue", linewidth=1.5, marker=".", markersize=3)
        ax5.plot(lon[0],  lat[0],  "go", markersize=8, label="Start")
        ax5.plot(lon[-1], lat[-1], "rs", markersize=8, label="End")
        ax5.set_title("GPS Ground Track")
        ax5.set_xlabel("Longitude")
        ax5.set_ylabel("Latitude")
        ax5.legend()
        ax5.grid(True, alpha=0.3)
    else:
        ax5.text(0.5, 0.5, "No GPS data", ha="center", va="center",
                 transform=ax5.transAxes, fontsize=12)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"[*] Plot saved to {save_path}")
    else:
        plt.show()


def main():
    args = parse_args()
    if not os.path.exists(args.log):
        print(f"[ERROR] File not found: {args.log}")
        sys.exit(1)

    print(f"[*] Loading {args.log} ...")
    rows = load_csv(args.log)
    print(f"[*] {len(rows)} records loaded. Generating plots ...")
    plot(rows, save_path=args.save)


if __name__ == "__main__":
    main()
