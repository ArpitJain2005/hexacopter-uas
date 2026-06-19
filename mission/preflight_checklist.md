# Pre-Flight Safety Checklist — Hexacopter UAS

> **Always complete this checklist before every flight.**  
> Sign off each item. Do not skip steps.

---

## 🔧 A. Physical Inspection

- [ ] Frame arms and central plate — no cracks or loose fasteners
- [ ] All 6 motors spin freely by hand — no grinding or resistance
- [ ] Propellers secured (self-tightening nuts finger-tight)
- [ ] Correct CW / CCW propeller on each motor
- [ ] Landing gear attached securely
- [ ] All cables routed and zip-tied — nothing near props
- [ ] FC mounted on vibration dampers — not loose
- [ ] GPS mast upright and connector secure

---

## 🔋 B. Battery & Power

- [ ] LiPo battery voltage checked: ≥ **15.8V** (4S) / ≥ **11.8V** (3S)
- [ ] No swelling, damage, or hot spots on battery pack
- [ ] Battery secured firmly to frame (no movement in flight)
- [ ] XT60 connector clean and fully seated
- [ ] Power module connector secure

---

## 📡 C. RC Transmitter

- [ ] Transmitter ON and bound to receiver
- [ ] Throttle at zero before powering vehicle
- [ ] All control surfaces (sticks) respond correctly in Mission Planner
- [ ] Flight mode switch assigns: STABILIZE / ALT_HOLD / LOITER
- [ ] Failsafe tested: TX off → FC enters RTL

---

## 💻 D. Mission Planner / GCS

- [ ] Connected to vehicle via telemetry or USB
- [ ] **GPS**: Fix type = 3D, Satellites ≥ 6, HDOP ≤ 2.0
- [ ] **EKF**: Status indicator green (OK)
- [ ] **Attitude**: HUD horizon level matches physical drone
- [ ] Battery voltage displayed and correct
- [ ] No active error messages or pre-arm warnings

---

## 🌍 E. Environment

- [ ] Flying area clear of people, buildings, overhead wires
- [ ] Wind speed acceptable (< 7 m/s recommended)
- [ ] No rain or moisture on electronics
- [ ] Legal to fly at this location (DGCA/local regulations)
- [ ] Spotter / safety observer present

---

## ✅ F. Final Checks Before Arm

- [ ] Props clear of obstructions — call "ARMING" out loud
- [ ] All crew stand behind the pilot or at safe distance
- [ ] RC transmitter in hand — ready for manual override
- [ ] Throttle at minimum
- [ ] Arm via RC: throttle down-right hold 3 seconds (or MP slider)
- [ ] Motors spin briefly at idle — no abnormal sound
- [ ] Takeoff immediately after arming — do not leave armed on ground

---

## 🚨 Emergency Procedures

| Situation              | Action                                            |
|------------------------|---------------------------------------------------|
| Drone drifting badly   | Switch to STABILIZE → manual correction           |
| Lost GPS               | Mode auto-falls back → switch to STABILIZE        |
| Low battery warning    | Land immediately                                  |
| Loss of RC signal      | Failsafe → RTL (verify configured in MP)          |
| Fly-away               | Kill switch (if configured) or cut RC signal      |
| Motor failure          | No recovery — clear the area, accept crash        |
