# OpenFOAM Flow Simulation Visualizer

A Python script to simulate and visualize fluid flow around a cylinder using OpenFOAM and ParaView. The simulation demonstrates the von Kármán vortex street phenomenon.

## Features

- Automated OpenFOAM simulation setup and execution
- Real-time ParaView visualization
- Customizable simulation parameters
- High-quality video output of flow visualization
- Streamline visualization of flow patterns

## Prerequisites

### Required Software

- Ubuntu/Linux operating system
- OpenFOAM v2406
- ParaView 5.10.0+
- Python 3.8+
- ffmpeg

### Python Dependencies

- numpy >= 1.20.0
- matplotlib >= 3.4.0
- paraview >= 5.10.0

## Installation

1. **OpenFOAM Installation**

   ```bash
   sudo apt-get update
   sudo apt-get install openfoam2406
   ```

2. **ParaView Installation**

   ```bash
   sudo apt-get install paraview
   ```

3. **ffmpeg Installation**

   ```bash
   sudo apt-get install ffmpeg
   ```

4. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
fluid_simulation/
├── run.py                     # Main simulation script
├── requirements.txt           # Python package requirements
├── README.md                  # This file
└── flow_cylinder/            # OpenFOAM case directory
    ├── system/
    │   ├── controlDict       # Simulation control parameters
    │   ├── fvSchemes        # Numerical schemes
    │   └── fvSolution       # Solution parameters
    ├── constant/
    │   ├── transportProperties  # Fluid properties
    │   └── polyMesh/        # Mesh files
    └── 0/                   # Initial conditions
        ├── p               # Pressure field
        └── U               # Velocity field
```

## Usage

1. **Source OpenFOAM Environment**

   ```bash
   source /usr/lib/openfoam/openfoam2406/etc/bashrc
   ```

2. **Run the Simulation**

   ```bash
   python run.py --end-time <time> --delta-t <timestep> --nu <viscosity>
   ```

   Parameters:

   - `--end-time`: Duration of simulation in seconds
   - `--delta-t`: Time step size
   - `--nu`: Kinematic viscosity

### Example Usage

1. **Standard Flow Simulation (40 seconds)**

   ```bash
   python run.py --end-time 40.0 --delta-t 0.001 --nu 0.01
   ```

   This will:

   - Run simulation for 40 seconds
   - Use time steps of 0.001 seconds
   - Set kinematic viscosity to 0.01

2. **Fast Flow (Lower Viscosity)**

   ```bash
   python run.py --end-time 40.0 --delta-t 0.001 --nu 0.005
   ```

   - Creates faster flow with more turbulence
   - Good for observing vortex shedding

3. **Slow Flow (Higher Viscosity)**
   ```bash
   python run.py --end-time 40.0 --delta-t 0.001 --nu 0.02
   ```
   - Creates slower, more laminar flow
   - Better for observing steady-state behavior

### Output

The script generates:

1. OpenFOAM simulation results in `flow_cylinder/`
2. Visualization frames in `frames/`
3. Final video file: `flow_visualization.mp4`

The visualization shows:

- Velocity magnitude (color-coded)
- Streamlines showing flow patterns
- Color bar for velocity scale
- Full view of cylinder and surrounding flow
