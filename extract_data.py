"""Extract simulation data and save to CSV."""

import os
import numpy as np
import pandas as pd
import argparse
import re


def ensure_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def read_force_coefficients(case_dir):
    """Read force coefficients from OpenFOAM forces output.
    
    Args:
        case_dir: Path to OpenFOAM case directory
    Returns:
        times: List of time values
        Cd: List of drag coefficients
        Cl: List of lift coefficients
    """
    times = []
    Cd = []
    Cl = []
    
    # Get all time directories
    time_dirs = []
    for item in os.listdir(case_dir):
        try:
            if item.replace('.', '').isdigit():
                time_dirs.append(item)
        except ValueError:
            continue
    time_dirs.sort(key=float)
    
    for time_dir in time_dirs:
        force_file = os.path.join(case_dir, time_dir, "uniform/functionObjects/functionObjectProperties")
        if not os.path.exists(force_file):
            continue
            
        try:
            with open(force_file, 'r') as f:
                content = f.read()
                
                # Find the forceCoeffs dictionary
                if "forceCoeffs" in content and "scalar" in content:
                    # Extract Cd and Cl values using string operations
                    cd_match = re.search(r'Cd\s+([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?);', content)
                    cl_match = re.search(r'Cl\s+([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?);', content)
                    
                    if cd_match and cl_match:
                        times.append(float(time_dir))
                        Cd.append(float(cd_match.group(1)))
                        Cl.append(float(cl_match.group(1)))
        except Exception as e:
            print(f"Error reading force coefficients from {force_file}: {str(e)}")
            continue
    
    # Sort by time
    sorted_data = sorted(zip(times, Cd, Cl))
    if sorted_data:
        times, Cd, Cl = zip(*sorted_data)
    
    return list(times), list(Cd), list(Cl)


def read_openfoam_vector_file(filepath):
    """Read OpenFOAM vector file and return list of values."""
    print(f"Reading vector file: {filepath}")
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
        # Find the data section
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '(':
                start_idx = i + 1
            elif line.strip() == ')':
                end_idx = i
                break
        
        if start_idx == -1 or end_idx == -1:
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
        
        return data


def read_openfoam_scalar_file(filepath):
    """Read OpenFOAM scalar file and return list of values."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
        # Find the data section
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '(':
                start_idx = i + 1
            elif line.strip() == ')':
                end_idx = i
                break
        
        if start_idx == -1 or end_idx == -1:
            return []
        
        # Process scalar data
        data = []
        for line in lines[start_idx:end_idx]:
            try:
                value = float(line.strip())
                data.append(value)
            except ValueError:
                continue
        
        return data


def extract_simulation_data(case_dir, output_dir):
    """Extract velocity, pressure and force coefficient data.
    
    Args:
        case_dir: Path to OpenFOAM case directory
        output_dir: Directory to save extracted data
    """
    print(f"\nExtracting data from: {case_dir}")
    
    # Get time directories
    time_dirs = []
    for item in os.listdir(case_dir):
        try:
            if item == '0' or (item.replace('.', '').isdigit() and float(item) > 0):
                time_dirs.append(item)
        except ValueError:
            continue
    time_dirs.sort(key=lambda x: float(x) if x.replace('.', '').isdigit() else 0)
    
    # Create output directories
    ensure_directory(os.path.join(output_dir, "velocity"))
    ensure_directory(os.path.join(output_dir, "pressure"))
    ensure_directory(os.path.join(output_dir, "forces"))
    
    # Initialize data structures
    times = []
    velocity_data = {}
    pressure_data = {}
    
    # Process each time directory
    for t_dir in time_dirs:
        t = float(t_dir) if t_dir.replace('.', '').isdigit() else 0.0
        print(f"\nProcessing time step {t} (directory: {t_dir})")
        time_dir = os.path.join(case_dir, t_dir)
        
        # Read velocity file
        U_file = os.path.join(time_dir, 'U')
        if os.path.exists(U_file):
            velocities = read_openfoam_vector_file(U_file)
            if velocities:
                times.append(t)
                for node_idx, vel in enumerate(velocities):
                    if node_idx not in velocity_data:
                        velocity_data[node_idx] = []
                    velocity_data[node_idx].append(vel)
        
        # Read pressure file
        p_file = os.path.join(time_dir, 'p')
        if os.path.exists(p_file):
            pressures = read_openfoam_scalar_file(p_file)
            for node_idx, p in enumerate(pressures):
                if node_idx not in pressure_data:
                    pressure_data[node_idx] = []
                pressure_data[node_idx].append(p)
    
    # Read force coefficients
    force_times, Cd, Cl = read_force_coefficients(case_dir)
    
    # Save velocity data
    if velocity_data:
        vel_columns = ['Time'] + [f'Node_{i}' for i in sorted(velocity_data.keys())]
        vel_df = pd.DataFrame(columns=vel_columns)
        vel_df['Time'] = times
        for node_idx in sorted(velocity_data.keys()):
            vel_df[f'Node_{node_idx}'] = velocity_data[node_idx]
        vel_path = os.path.join(output_dir, "velocity", "data.csv")
        vel_df.to_csv(vel_path, index=False)
        print(f"\nSaved velocity data: {vel_path}")
    
    # Save pressure data
    if pressure_data:
        press_columns = ['Time'] + [f'Node_{i}' for i in sorted(pressure_data.keys())]
        press_df = pd.DataFrame(columns=press_columns)
        press_df['Time'] = times
        for node_idx in sorted(pressure_data.keys()):
            press_df[f'Node_{node_idx}'] = pressure_data[node_idx]
        press_path = os.path.join(output_dir, "pressure", "data.csv")
        press_df.to_csv(press_path, index=False)
        print(f"Saved pressure data: {press_path}")
    
    # Save force coefficient data
    if Cd and Cl:
        force_df = pd.DataFrame({
            'Time': force_times,
            'Drag_Coefficient': Cd,
            'Lift_Coefficient': Cl
        })
        force_path = os.path.join(output_dir, "forces", "coefficients.csv")
        force_df.to_csv(force_path, index=False)
        print(f"Saved force coefficient data: {force_path}")


def main():
    parser = argparse.ArgumentParser(description='Extract OpenFOAM simulation data')
    parser.add_argument('case_dir', help='Path to OpenFOAM case directory')
    parser.add_argument('output_dir', help='Directory to save extracted data')
    args = parser.parse_args()
    
    extract_simulation_data(args.case_dir, args.output_dir)


if __name__ == '__main__':
    main()