# Lessons Learned & Debugging Notes

## Compass Interference (Toilet-Bowl Effect in LOITER)
**Symptom:** Drone slowly circled in LOITER mode instead of holding position.
**Root Cause:** Compass calibrated while placed on a metal workbench, causing bad offsets.
**Fix:** Re-calibrated compass outdoors, away from metal and electronics.
**Prevention:** Always calibrate compass in the same environment where you fly.

## ESC Not Responding After Calibration
**Symptom:** One ESC did not spin during motor test after calibration.
**Root Cause:** ESC signal wire on wrong MAIN OUT channel (wired to CH7 instead of CH3).
**Fix:** Re-wired to correct channel, verified in Mission Planner motor test.

## EKF Health Errors on Boot
**Symptom:** Mission Planner showed EKF errors, could not arm.
**Root Cause:** GPS mast was too short — GPS was sitting above the PDB, picking up EM noise.
**Fix:** Extended GPS mast to 15cm, compass interference dropped significantly.

## Vibration Levels Too High
**Symptom:** DataFlash logs showed vibration > 25 m/s^2.
**Root Cause:** Motor mount bolts were loose after first outdoor test.
**Fix:** Applied Loctite to all motor mount bolts, tightened properly. Vibration dropped to < 10 m/s^2.

## DroneKit Connection Timeout
**Symptom:** `connect()` timed out when using USB.
**Root Cause:** Wrong baud rate (used 115200 instead of 57600 for telemetry radio).
**Fix:** Use 57600 for SiK telemetry, 115200 for USB direct connection.

## IMU Calibration Not Saving
**Symptom:** Accel calibration kept failing after reboot.
**Root Cause:** Did not wait for the "Please reboot" prompt before unplugging.
**Fix:** Always wait for Mission Planner to show "Calibration Successful" and then reboot FC before disconnecting.
