# Motor Configuration — Hexacopter

## Motor Layout (ArduCopter X-Frame)

ArduCopter numbers hexacopter motors as follows (viewed from above):

```
              FRONT
         _____|_____
        /     |     \
    M1(CCW)   |   M2(CW)
      /        |        \
     /         |         \
M6(CW)----[FC CENTER]----M3(CCW)
     \         |         /
      \        |        /
    M5(CCW)   |   M4(CW)
        \_____| _____/
              |
             REAR
```

## Motor Number → ESC Output Mapping (Pixhawk / APM)

| Motor # | Position     | Direction | FC Output Pin |
|---------|--------------|-----------|---------------|
| M1      | Front-Left   | CCW       | MAIN OUT 1    |
| M2      | Front-Right  | CW        | MAIN OUT 2    |
| M3      | Right        | CCW       | MAIN OUT 3    |
| M4      | Rear-Right   | CW        | MAIN OUT 4    |
| M5      | Rear-Left    | CCW       | MAIN OUT 5    |
| M6      | Left         | CW        | MAIN OUT 6    |

## Propeller Direction Convention

- **CW motor** → **CCW propeller** (pushes air down with CW shaft rotation)
- **CCW motor** → **CW propeller**

Verify by hand-spinning each prop before powering — the flat face must face down.

## ESC Wiring

Each ESC connects:
- **3 phase wires** → BLDC motor (swap any 2 to reverse direction)
- **Signal wire** → Flight controller PWM output pin
- **Power wires (XT60)** → Power distribution board

## Direction Verification Procedure

1. Remove all propellers.
2. Connect battery and arm in Mission Planner Motor Test.
3. Test each motor individually at ~10% throttle.
4. Confirm rotation direction matches the table above.
5. If a motor spins wrong direction, swap any two of its three phase wires.

## BLDC Motor Specs (typical for this class)

| Parameter         | Value              |
|-------------------|--------------------|
| KV Rating         | 920–1000 KV        |
| Max Current       | ~22–30 A           |
| Recommended ESC   | 30A with BEC       |
| Propeller Size    | 10"–12" (matched pair) |
