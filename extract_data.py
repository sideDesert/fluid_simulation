"""Extract simulation data and save to CSV."""

import os
import numpy as np
import pandas as pd


def ensure_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def calculate_drag_coefficient(force, velocity, density, area):
    """Calculate drag coefficient."""
    return 2 * force / (density * velocity * velocity * area)


def read_openfoam_vector_file(filepath):
    """Read OpenFOAM vector file and return list of values."""
    print(f"Reading vector file: {filepath}")
    with open(filepath, 'r') as f:
        lines = f.readlines()
        print(f"Total lines in file: {len(lines)}")
        
        # Debug: Print first few lines
        print("First 10 lines:")
        for line in lines[:10]:
            print(line.strip())
        
        # Find the data section
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '(':
                start_idx = i + 1
                print(f"Found data start at line {i+1}")
            elif line.strip() == ')':
                end_idx = i
                print(f"Found data end at line {i}")
                break
        
        if start_idx == -1 or end_idx == -1:
            print("Could not find data section markers")
            return []
        
        # Process vector data
        data = []
        for line in lines[start_idx:end_idx]:
            if '(' in line and ')' in line:
                values = line.strip('()\n').split()
                if len(values) == 3:
                    try:
                        vector = [float(v) for v in values]
                        magnitude = np.sqrt(sum(v*v for v in vector))
                        data.append(magnitude)
                    except ValueError:
                        continue
        
        print(f"Extracted {len(data)} vector values")
        return data


def read_openfoam_scalar_file(filepath):
    """Read OpenFOAM scalar file and return list of values."""
    print(f"Reading scalar file: {filepath}")
    with open(filepath, 'r') as f:
        lines = f.readlines()
        print(f"Total lines in file: {len(lines)}")
        
        # Debug: Print first few lines
        print("First 10 lines:")
        for line in lines[:10]:
            print(line.strip())
        
        # Find the data section
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '(':
                start_idx = i + 1
                print(f"Found data start at line {i+1}")
            elif line.strip() == ')':
                end_idx = i
                print(f"Found data end at line {i}")
                break
        
        if start_idx == -1 or end_idx == -1:
            print("Could not find data section markers")
            return []
        
        # Process scalar data
        data = []
        for line in lines[start_idx:end_idx]:
            try:
                value = float(line.strip())
                data.append(value)
            except ValueError:
                continue
        
        print(f"Extracted {len(data)} scalar values")
        return data


def extract_simulation_data(case_dir):
    """Extract velocity, pressure and drag coefficient data."""
    print(f"\nExtracting data from: {case_dir}")
    
    # Get time directories (including simulation results)
    time_dirs = []
    for item in os.listdir(case_dir):
        try:
            # Handle both integer and float time directories
            if item == '0' or (item.replace('.', '').isdigit() and float(item) > 0):
                time_dirs.append(item)
        except ValueError:
            continue
    time_dirs.sort(key=lambda x: float(x) if x.replace('.', '').isdigit() else 0)
    
    print(f"Found time directories: {time_dirs}")
    if not time_dirs:
        print("No time directories found. Make sure the simulation has been run.")
        return

    # Create data directories
    data_dir = "data"
    ensure_directory(data_dir)
    ensure_directory(os.path.join(data_dir, "velocity"))
    ensure_directory(os.path.join(data_dir, "pressure"))
    ensure_directory(os.path.join(data_dir, "drag"))

    # Initialize data structures
    times = []
    velocity_data = {}
    pressure_data = {}
    drag_coeffs = []

    # Constants for drag coefficient calculation
    density = 1.0
    diameter = 1.0
    area = diameter
    inlet_velocity = 1.0

    # Process each time directory
    for t_dir in time_dirs:
        t = float(t_dir) if t_dir.replace('.', '').isdigit() else 0.0
        print(f"\nProcessing time step {t} (directory: {t_dir})")
        time_dir = os.path.join(case_dir, t_dir)
        
        # Read velocity file
        U_file = os.path.join(time_dir, 'U')
        if os.path.exists(U_file):
            print(f"Found U file: {U_file}")
            velocities = read_openfoam_vector_file(U_file)
            if velocities:
                times.append(t)
                for node_idx, vel in enumerate(velocities):
                    if node_idx not in velocity_data:
                        velocity_data[node_idx] = []
                    velocity_data[node_idx].append(vel)
        else:
            print(f"No U file found in {time_dir}")

        # Read pressure file
        p_file = os.path.join(time_dir, 'p')
        if os.path.exists(p_file):
            print(f"Found p file: {p_file}")
            pressures = read_openfoam_scalar_file(p_file)
            for node_idx, p in enumerate(pressures):
                if node_idx not in pressure_data:
                    pressure_data[node_idx] = []
                pressure_data[node_idx].append(p)
            
            # Calculate drag coefficient
            if pressures:
                p_upstream = np.max(pressures)
                p_downstream = np.min(pressures)
                force = (p_upstream - p_downstream) * area
                cd = calculate_drag_coefficient(force, inlet_velocity, density, area)
                drag_coeffs.append(cd)
        else:
            print(f"No p file found in {time_dir}")

    print("\nSummary:")
    print(f"Time steps processed: {len(times)}")
    print(f"Velocity nodes: {len(velocity_data)}")
    print(f"Pressure nodes: {len(pressure_data)}")
    print(f"Drag coefficients calculated: {len(drag_coeffs)}")

    # Save velocity data
    if velocity_data:
        vel_columns = ['Time'] + [f'Node_{i}' for i in sorted(velocity_data.keys())]
        vel_df = pd.DataFrame(columns=vel_columns)
        vel_df['Time'] = times
        for node_idx in sorted(velocity_data.keys()):
            vel_df[f'Node_{node_idx}'] = velocity_data[node_idx]
        vel_path = os.path.join(data_dir, "velocity", "data.csv")
        vel_df.to_csv(vel_path, index=False)
        print(f"\nSaved velocity data: {vel_path}")

    # Save pressure data
    if pressure_data:
        press_columns = ['Time'] + [f'Node_{i}' for i in sorted(pressure_data.keys())]
        press_df = pd.DataFrame(columns=press_columns)
        press_df['Time'] = times
        for node_idx in sorted(pressure_data.keys()):
            press_df[f'Node_{node_idx}'] = pressure_data[node_idx]
        press_path = os.path.join(data_dir, "pressure", "data.csv")
        press_df.to_csv(press_path, index=False)
        print(f"Saved pressure data: {press_path}")

    # Save drag coefficient data
    if drag_coeffs:
        drag_df = pd.DataFrame({
            'Time': times,
            'Drag_Coefficient': drag_coeffs
        })
        drag_path = os.path.join(data_dir, "drag", "data.csv")
        drag_df.to_csv(drag_path, index=False)
        print(f"Saved drag coefficient data: {drag_path}")


if __name__ == "__main__":
    case_dir = "flow_cylinder"
    extract_simulation_data(case_dir) 