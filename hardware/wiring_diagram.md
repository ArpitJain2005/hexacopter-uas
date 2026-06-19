# Wiring & Connection Guide

## Power Distribution

```
LiPo Battery (4S)
       |
  [Power Module]  ──────────────────> Pixhawk POWER port (5V regulated)
       |
  [PDB - Power Distribution Board]
   |    |    |    |    |    |
 ESC1 ESC2 ESC3 ESC4 ESC5 ESC6
  |    |    |    |    |    |
 M1   M2   M3   M4   M5   M6
```

## ESC to Flight Controller (PWM Signal)

| ESC | Motor | FC Output Channel | Rotation |
|-----|-------|-------------------|----------|
| ESC1 | Front-Right | CH1 (MAIN OUT 1) | CW  |
| ESC2 | Rear-Right  | CH2 (MAIN OUT 2) | CCW |
| ESC3 | Right       | CH3 (MAIN OUT 3) | CW  |
| ESC4 | Rear-Left   | CH4 (MAIN OUT 4) | CCW |
| ESC5 | Left        | CH5 (MAIN OUT 5) | CW  |
| ESC6 | Front-Left  | CH6 (MAIN OUT 6) | CCW |

> ESC signal wire (white/yellow) → FC MAIN OUT pin
> ESC ground (black) → FC MAIN OUT GND rail
> Do NOT connect ESC +5V to FC rail (BEC conflict)

## GPS/Compass Connection
```
GPS Module
├── TX  → FC GPS port RX
├── RX  → FC GPS port TX
├── GND → FC GND
├── VCC → FC 5V
├── SDA → FC I2C SDA  (compass)
└── SCL → FC I2C SCL  (compass)
```

## RC Receiver (PPM mode)
```
FS-iA6B Receiver
├── PPM pin → FC RC IN
├── GND     → FC GND
└── VCC     → FC 5V
```
> Bind receiver to transmitter BEFORE connecting to FC.
> Set iA6B to PPM output mode (jumper on pins 4-5 in bind mode).

## Telemetry Radio
```
433 MHz SiK (Air Unit)
├── TX  → FC TELEM1 RX
├── RX  → FC TELEM1 TX
├── GND → FC GND
└── VCC → FC 5V
```

## Safety Notes
- Always connect LiPo LAST, disconnect FIRST
- Remove propellers before any bench testing
- Verify motor rotation direction before first prop-on test
- Use a LiPo charge bag during charging
