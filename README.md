# OpenFOAM Flow Simulation Visualizer

A Python script to simulate and visualize fluid flow around a cylinder using OpenFOAM and ParaView. The simulation demonstrates the von Kármán vortex street phenomenon.

## Features

- Automated OpenFOAM simulation setup and execution
- Real-time ParaView visualization
- Customizable simulation parameters
- High-quality video output of flow visualization
- Streamline visualization of flow patterns
- Data extraction and analysis (velocity, pressure, drag coefficient)

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
- pandas >= 1.3.0

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
├── extract_data.py           # Data extraction script
├── data/                     # Generated data directory
│   ├── velocity/            # Velocity magnitude data
│   ├── pressure/           # Pressure field data
│   └── drag/              # Drag coefficient data
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

3. **Extract Simulation Data**

   ```bash
   python extract_data.py
   ```

   This will create CSV files containing:

   - Velocity magnitude at each node over time
   - Pressure values at each node over time
   - Drag coefficient over time

### Example Usage

1. **Standard Flow Simulation (40 seconds)**

   ```bash
   python run.py --end-time 40.0 --delta-t 0.001 --nu 0.01
   python extract_data.py
   ```

   This will:

   - Run simulation for 40 seconds
   - Use time steps of 0.001 seconds
   - Set kinematic viscosity to 0.01
   - Generate data files for analysis

2. **Fast Flow (Lower Viscosity)**

   ```bash
   python run.py --end-time 40.0 --delta-t 0.001 --nu 0.005
   python extract_data.py
   ```

   - Creates faster flow with more turbulence
   - Good for observing vortex shedding

3. **Slow Flow (Higher Viscosity)**
   ```bash
   python run.py --end-time 40.0 --delta-t 0.001 --nu 0.02
   python extract_data.py
   ```
   - Creates slower, more laminar flow
   - Better for observing steady-state behavior

### Output

The scripts generate:

1. OpenFOAM simulation results in `flow_cylinder/`
2. Visualization frames in `frames/`
3. Final video file: `flow_visualization.mp4`
4. Data files in `data/`:
   - `velocity/data.csv`: Velocity magnitude at each node
   - `pressure/data.csv`: Pressure values at each node
   - `drag/data.csv`: Drag coefficient over time

The visualization shows:

- Velocity magnitude (color-coded)
- Streamlines showing flow patterns
- Color bar for velocity scale
- Full view of cylinder and surrounding flow

## Data Analysis

The generated CSV files can be used for:

- Flow pattern analysis
- Drag coefficient studies
- Pressure distribution analysis
- Velocity field visualization
- Time-dependent behavior studies

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
