# Key Mission Planner Parameters for Manual Flight

These parameters were tuned during the CDAC internship flight tests.
Set these in Mission Planner: Config > Full Parameter List

## Stabilize Mode (Manual Flight)
| Parameter | Value | Description |
|-----------|-------|-------------|
| STAB_PITCH_MAX | 4500 | Max pitch angle in stabilize (centidegrees) |
| STAB_ROLL_MAX | 4500 | Max roll angle in stabilize |
| ATC_RAT_RLL_P | 0.135 | Roll rate P gain |
| ATC_RAT_PIT_P | 0.135 | Pitch rate P gain |
| ATC_RAT_YAW_P | 0.180 | Yaw rate P gain |

## Throttle / Motor
| Parameter | Value | Description |
|-----------|-------|-------------|
| MOT_SPIN_ARM | 0.10 | Motor speed when armed (idle) |
| MOT_SPIN_MIN | 0.15 | Minimum motor speed in flight |
| MOT_THST_HOVER | 0.35 | Estimated hover throttle (auto-learned) |
| THR_MID | 500 | Mid-throttle stick position |

## Failsafe
| Parameter | Value | Description |
|-----------|-------|-------------|
| FS_THR_ENABLE | 1 | Throttle failsafe enabled |
| FS_THR_VALUE | 975 | Throttle failsafe PWM value |
| FS_GCS_ENABLE | 1 | GCS heartbeat failsafe |
| FS_BATT_ENABLE | 1 | Low battery failsafe |
| FS_BATT_VOLTAGE | 14.0 | Trigger voltage (4S = 3.5V/cell) |

## GPS / Navigation
| Parameter | Value | Description |
|-----------|-------|-------------|
| GPS_TYPE | 1 | Auto-detect GPS type |
| EK3_ENABLE | 1 | Use EKF3 estimator |
| COMPASS_USE | 1 | Enable primary compass |
| COMPASS_USE2 | 0 | Disable internal compass (FC) — use external only |

## Frame
| Parameter | Value | Description |
|-----------|-------|-------------|
| FRAME_CLASS | 2 | Hexacopter |
| FRAME_TYPE | 1 | X-configuration |

## RC Calibration (typical values)
| Channel | Min | Max | Trim |
|---------|-----|-----|------|
| CH1 (Roll)     | 1000 | 2000 | 1500 |
| CH2 (Pitch)    | 1000 | 2000 | 1500 |
| CH3 (Throttle) | 1000 | 2000 | 1000 |
| CH4 (Yaw)      | 1000 | 2000 | 1500 |

> Actual values depend on your RC transmitter — always calibrate via
> Mission Planner: Initial Setup > Mandatory Hardware > Radio Calibration
