# Bill of Materials & Assembly Checklist

## Bill of Materials (BOM)

| # | Component              | Qty | Notes                                      |
|---|------------------------|-----|--------------------------------------------|
| 1 | Hexacopter Frame       | 1   | Carbon fibre / glass fibre, ~550–680mm     |
| 2 | BLDC Motors            | 6   | ~920KV, matched set                        |
| 3 | ESCs                   | 6   | 30A, SimonK / BLHeli firmware              |
| 4 | Flight Controller      | 1   | APM 2.8 or Pixhawk 2.4.8                   |
| 5 | GPS + Compass Module   | 1   | u-blox M8N, mounted on mast               |
| 6 | Power Module           | 1   | 90A, 5.3V BEC, voltage+current sensor     |
| 7 | LiPo Battery           | 1   | 4S 10000mAh (or per endurance need)        |
| 8 | Propellers (CW)        | 3   | Matched to motor KV and frame size         |
| 9 | Propellers (CCW)       | 3   | Matched to motor KV and frame size         |
|10 | Telemetry Module       | 2   | 433MHz pair (air + ground)                 |
|11 | RC Receiver            | 1   | Compatible with transmitter (PPM/SBUS)     |
|12 | RC Transmitter         | 1   | Min. 6-channel                             |
|13 | Power Distribution Board| 1  | Solder pads for 6 ESCs                    |
|14 | Landing Gear           | 1   | Fixed type, sufficient ground clearance    |
|15 | XT60 Connectors        | 4   | Male/female pairs                          |
|16 | Heat Shrink Tubing     | —   | For ESC and power wire insulation          |
|17 | Zip Ties + Velcro      | —   | Cable management                           |
|18 | Vibration Dampers      | 4   | For flight controller mounting             |

---

## Assembly Checklist

### Phase 1 — Frame Assembly
- [ ] Mount central plates and arm tubes per frame manual
- [ ] Secure landing gear legs to bottom plate
- [ ] Mount power distribution board (PDB) to center plate

### Phase 2 — Motor & ESC Mounting
- [ ] Bolt BLDC motors onto arm ends
- [ ] Solder ESC power wires to PDB
- [ ] Connect ESC phase wires to motor (3 wires each)
- [ ] Route signal wires cleanly toward FC

### Phase 3 — Flight Controller Installation
- [ ] Mount FC on vibration dampers at center
- [ ] Connect ESC signal wires to FC MAIN OUT 1–6
- [ ] Connect power module to FC power rail and PM port
- [ ] Mount GPS on elevated mast (away from mag interference)
- [ ] Connect GPS/Compass to FC UART and I2C ports

### Phase 4 — RC & Telemetry
- [ ] Bind RC receiver to transmitter
- [ ] Connect RC RX to FC (PPM or SBUS input)
- [ ] Mount telemetry radio on frame
- [ ] Connect telemetry to FC TELEM port

### Phase 5 — Pre-Power Checks
- [ ] All solder joints inspected (no cold joints)
- [ ] No exposed wires
- [ ] Props OFF during all bench testing
- [ ] FC orientation confirmed (arrow pointing forward)
- [ ] Battery connector polarity verified

### Phase 6 — Initial Power-On
- [ ] Connect battery (no props)
- [ ] FC boots without errors (solid LED)
- [ ] Mission Planner connects via USB
- [ ] Firmware version confirmed (ArduCopter Hexa)
- [ ] Frame type set to Hexa X in MP
