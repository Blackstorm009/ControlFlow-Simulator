# MCUS — Microprogrammed Control Unit Simulator

A microprogrammed control unit simulator built in 8086 assembly with a Python/Tkinter GUI to visualize the fetch-decode-execute cycle and control signal generation.

## Overview

This project demonstrates how a control unit generates control signals to drive CPU operations. The assembly program simulates four microinstructions, while the Python GUI visualizes register states, active control signals, and step-by-step execution in real time.

## Features

- Fetch-decode-execute cycle simulation
- Four control signals: `MEM_READ`, `ALU_ADD`, `ALU_SUB`, `HALT`
- Live register tracking (AX, BX, CX, SI)
- Step-by-step execution with Next / Prev / Reset controls
- Visual highlighting of active control signals
- Execution log for tracing each step

## Tech Stack

- **Assembly (8086, COM format)** — core simulation logic
- **Python (Tkinter)** — GUI visualization layer

## Project Structure
├── mcus.asm          # 8086 assembly source (COM format)

├── mcus_gui.py       # Python GUI simulator

└── README.md

## How It Works

1. **Setup** — Initializes registers (`AX`, `BX`, `CX`, `SI`) and instruction counter
2. **Fetch** — Checks if instructions remain (`CX`)
3. **Decode** — Determines which microinstruction to execute based on `SI`
4. **Execute** — Runs the corresponding control signal:
   - `DO_MEM_READ` — simulates a memory read
   - `DO_ALU_ADD` — simulates an ALU addition
   - `DO_ALU_SUB` — simulates an ALU subtraction
   - `DO_HALT` — terminates the program
5. **Next** — Advances to the next instruction and repeats

## Running the Assembly Code

Assemble and run using an 8086 emulator such as **DOSBox** with **NASM** or **MASM**:

```bash
nasm -f bin mcus.asm -o mcus.com
mcus.com
```

## Running the GUI Simulator

Requires Python 3 with Tkinter (included by default):

```bash
python mcus_gui.py
```

## Controls

| Button | Action |
|--------|--------|
| Next Step | Executes the next microinstruction |
| Prev Step | Reverts to the previous state |
| Reset | Restarts the simulation from the beginning |
