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

2. **Single Simulation**

   ```bash
   python3 run.py --end-time <time> --delta-t <timestep> --Re <reynolds> --velocity <velocity>
   ```

   Parameters:

   - `--end-time`: Duration of simulation in seconds
   - `--delta-t`: Time step size
   - `--Re`: Reynolds number (dimensionless)
   - `--velocity`: Free stream velocity (m/s)

3. **Batch Simulations**

   Create a JSON configuration file (e.g., `sample.json`):

   ```json
   {
     "velocity": [1.0, 1.0],
     "Re": [50, 100]
   }
   ```

   Run multiple simulations:

   ```bash
   python3 batch_run.py sample.json --end-time 5.0 --delta-t 0.01
   ```

   This will:

   - Run simulations for each Re-velocity pair
   - Save videos in `media/` directory as `flow_Re{Re}_U{velocity}.mp4`
   - Save data in `data/run_Re{Re}_U{velocity}/` directories
   - Each run directory contains:
     - `velocity/data.csv`: Velocity magnitude data
     - `pressure/data.csv`: Pressure field data
     - `drag/data.csv`: Drag coefficient data

### Example Usage

1. **Single Laminar Flow (Re = 100)**

   ```bash
   python3 run.py --end-time 40.0 --delta-t 0.001 --Re 100 --velocity 1.0
   ```

2. **Multiple Flow Regimes**

   Create `simulations.json`:

   ```json
   {
     "velocity": [1.0, 1.0, 1.0],
     "Re": [50, 100, 200]
   }
   ```

   Run batch simulations:

   ```bash
   python3 batch_run.py simulations.json --end-time 40.0 --delta-t 0.001
   ```

   This will simulate:

   - Steady flow (Re = 50)
   - Laminar vortex shedding (Re = 100)
   - Transitional flow (Re = 200)

### Output Structure

```
project/
├── media/                      # Visualization videos
│   ├── flow_Re50_U1.0.mp4
│   └── flow_Re100_U1.0.mp4
└── data/                      # Simulation data
    ├── run_Re50_U1.0/
    │   ├── velocity/
    │   ├── pressure/
    │   └── drag/
    └── run_Re100_U1.0/
        ├── velocity/
        ├── pressure/
        └── drag/
```

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
