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
