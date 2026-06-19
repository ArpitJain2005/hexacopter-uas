

import argparse
import os
import sys
from datetime import datetime

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
except ImportError:
    print("Install required packages: pip install matplotlib pandas")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Flight Log Parser & Visualizer")
    parser.add_argument("--file",   required=True, help="Path to log file (.csv or .tlog)")
    parser.add_argument("--tlog",   action="store_true", help="Input is a MAVLink .tlog file")
    parser.add_argument("--output", default="flight_analysis.png",
                        help="Output plot filename")
    return parser.parse_args()


# ─────────────────────────────────────────
# CSV Parser (from telemetry_monitor.py logs)
# ─────────────────────────────────────────

def load_csv_log(filepath: str) -> pd.DataFrame:
    """Load and validate a CSV telemetry log."""
    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("elapsed_s").reset_index(drop=True)
    print(f"[CSV] Loaded {len(df)} rows. Duration: {df['elapsed_s'].max()}s")
    return df


# ─────────────────────────────────────────
# TLOG Parser (ArduCopter .tlog)
# ─────────────────────────────────────────

def load_tlog(filepath: str) -> pd.DataFrame:
    """Parse a MAVLink .tlog binary log into a DataFrame."""
    try:
        from pymavlink import mavutil
    except ImportError:
        print("Install pymavlink: pip install pymavlink")
        sys.exit(1)

    mlog = mavutil.mavlink_connection(filepath)
    rows = []
    t0   = None

    while True:
        msg = mlog.recv_match(type=["ATTITUDE", "GPS_RAW_INT",
                                     "SYS_STATUS", "VFR_HUD"],
                              blocking=False)
        if msg is None:
            break

        t = msg._timestamp
        if t0 is None:
            t0 = t
        elapsed = t - t0

        mtype = msg.get_type()
        row   = {"elapsed_s": round(elapsed, 2)}

        if mtype == "ATTITUDE":
            row.update({
                "roll_deg":  round(msg.roll  * 57.2958, 3),
                "pitch_deg": round(msg.pitch * 57.2958, 3),
                "yaw_deg":   round(msg.yaw   * 57.2958, 3),
            })
        elif mtype == "GPS_RAW_INT":
            row.update({
                "lat":        msg.lat / 1e7,
                "lon":        msg.lon / 1e7,
                "alt_agl_m": msg.alt / 1000.0,
                "satellites": msg.satellites_visible,
                "hdop":       msg.eph / 100.0,
            })
        elif mtype == "SYS_STATUS":
            row["bat_voltage"] = msg.voltage_battery / 1000.0
        elif mtype == "VFR_HUD":
            row["alt_agl_m"]   = msg.alt
            row["airspeed_ms"] = msg.airspeed
            row["groundspeed"] = msg.groundspeed

        rows.append(row)

    df = pd.DataFrame(rows).sort_values("elapsed_s").reset_index(drop=True)
    # Forward-fill across message types to align columns
    df = df.groupby("elapsed_s").first().reset_index().ffill()
    print(f"[TLOG] Parsed {len(df)} rows. Duration: {df['elapsed_s'].max():.1f}s")
    return df


# ─────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────

def plot_flight_analysis(df: pd.DataFrame, output_path: str):
    """Generate a 4-panel flight analysis figure."""
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("Hexacopter UAS — Flight Analysis\nCDAC Noida Internship | Arpit Jain",
                 fontsize=14, fontweight="bold")

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

    t = df["elapsed_s"]

    # Panel 1 — Altitude Profile
    ax1 = fig.add_subplot(gs[0, 0])
    if "alt_agl_m" in df.columns:
        ax1.plot(t, df["alt_agl_m"], color="#2196F3", linewidth=2)
        ax1.fill_between(t, df["alt_agl_m"], alpha=0.15, color="#2196F3")
        ax1.axhline(y=df["alt_agl_m"].max(), color="red", linestyle="--",
                    alpha=0.5, label=f"Max: {df['alt_agl_m'].max():.1f}m")
        ax1.set_ylabel("Altitude AGL (m)")
        ax1.legend(fontsize=8)
    ax1.set_title("Altitude Profile")
    ax1.set_xlabel("Time (s)")
    ax1.grid(True, alpha=0.3)

    # Panel 2 — Attitude
    ax2 = fig.add_subplot(gs[0, 1])
    for col, color, label in [("roll_deg",  "#E91E63", "Roll"),
                                ("pitch_deg", "#4CAF50", "Pitch"),
                                ("yaw_deg",   "#FF9800", "Yaw")]:
        if col in df.columns:
            ax2.plot(t, df[col], color=color, linewidth=1.5, label=label)
    ax2.axhline(y=0, color="gray", linestyle="--", alpha=0.4)
    ax2.set_title("Attitude (Roll / Pitch / Yaw)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Degrees (°)")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    # Panel 3 — GPS Ground Track
    ax3 = fig.add_subplot(gs[1, 0])
    if "lat" in df.columns and "lon" in df.columns:
        lat = df["lat"].dropna()
        lon = df["lon"].dropna()
        if len(lat) > 1:
            sc = ax3.scatter(lon, lat, c=range(len(lat)),
                             cmap="plasma", s=10, zorder=3)
            ax3.plot(lon, lat, color="gray", linewidth=0.8, alpha=0.5)
            ax3.plot(lon.iloc[0],  lat.iloc[0],  "go", ms=10, label="Start", zorder=5)
            ax3.plot(lon.iloc[-1], lat.iloc[-1], "rs", ms=10, label="End",   zorder=5)
            plt.colorbar(sc, ax=ax3, label="Time →")
            ax3.legend(fontsize=8)
        ax3.set_xlabel("Longitude (°)")
        ax3.set_ylabel("Latitude (°)")
    else:
        ax3.text(0.5, 0.5, "GPS data not available", ha="center", va="center",
                 transform=ax3.transAxes, fontsize=11, color="gray")
    ax3.set_title("GPS Ground Track")
    ax3.grid(True, alpha=0.3)

    # Panel 4 — Battery Voltage
    ax4 = fig.add_subplot(gs[1, 1])
    if "bat_voltage" in df.columns:
        bv = df["bat_voltage"].dropna()
        ax4.plot(t[:len(bv)], bv, color="#9C27B0", linewidth=2)
        ax4.axhline(y=14.0, color="orange", linestyle="--",
                    alpha=0.7, label="Warning (14.0V)")
        ax4.axhline(y=13.2, color="red",    linestyle="--",
                    alpha=0.7, label="Critical (13.2V)")
        ax4.set_ylabel("Voltage (V)")
        ax4.legend(fontsize=8)
    else:
        ax4.text(0.5, 0.5, "Battery data not available", ha="center", va="center",
                 transform=ax4.transAxes, fontsize=11, color="gray")
    ax4.set_title("Battery Voltage")
    ax4.set_xlabel("Time (s)")
    ax4.grid(True, alpha=0.3)

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"\n[PLOT] Saved to: {output_path}")
    plt.show()


# ─────────────────────────────────────────
# Summary Stats
# ─────────────────────────────────────────

def print_summary(df: pd.DataFrame):
    print("\n" + "=" * 50)
    print("  FLIGHT SUMMARY")
    print("=" * 50)
    print(f"  Duration        : {df['elapsed_s'].max():.0f}s")

    if "alt_agl_m" in df.columns:
        print(f"  Max Altitude    : {df['alt_agl_m'].max():.2f}m")
        print(f"  Avg Altitude    : {df['alt_agl_m'].mean():.2f}m")

    if "roll_deg" in df.columns:
        print(f"  Max Roll        : {df['roll_deg'].abs().max():.2f}°")
        print(f"  Max Pitch       : {df['pitch_deg'].abs().max():.2f}°")

    if "bat_voltage" in df.columns:
        v = df["bat_voltage"].dropna()
        if len(v):
            print(f"  Start Voltage   : {v.iloc[0]:.2f}V")
            print(f"  End Voltage     : {v.iloc[-1]:.2f}V")
            print(f"  Voltage Drop    : {v.iloc[0] - v.iloc[-1]:.2f}V")

    if "satellites" in df.columns:
        print(f"  Avg Satellites  : {df['satellites'].mean():.1f}")
    print("=" * 50)


def main():
    args = parse_args()

    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}")
        sys.exit(1)

    print(f"Loading log: {args.file}")
    df = load_tlog(args.file) if args.tlog else load_csv_log(args.file)

    print_summary(df)
    plot_flight_analysis(df, args.output)


if __name__ == "__main__":
    main()
