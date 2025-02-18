"""Script to run multiple OpenFOAM simulations from JSON configuration."""

import os
import json
import subprocess
from pathlib import Path
import shutil


def validate_json(data):
    """Validate JSON structure and data.
    
    Args:
        data: Loaded JSON data
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(data, dict):
        print("Error: JSON must be a dictionary")
        return False
        
    if 'nu' not in data or 'Re' not in data:
        print("Error: JSON must contain 'nu' and 'Re' arrays")
        return False
        
    if not isinstance(data['nu'], list) or not isinstance(data['Re'], list):
        print("Error: 'nu' and 'Re' must be arrays")
        return False
        
    if len(data['nu']) != len(data['Re']):
        print("Error: 'nu' and 'Re' arrays must have equal length")
        return False
        
    if not data['nu'] or not data['Re']:
        print("Error: Arrays cannot be empty")
        return False
        
    return True


def run_simulation(end_time, delta_t, Re, nu, run_number):
    """Run single simulation with given parameters."""
    print(f"\nRunning simulation {run_number}")
    print(f"Parameters: Re={Re}, nu={nu}")
    
    try:
        # Create directories
        os.makedirs('media', exist_ok=True)
        run_dir = f'data/run_Re{Re}_nu{nu}'
        os.makedirs(run_dir, exist_ok=True)
        
        # Run the simulation
        subprocess.run([
            'python3',
            'run.py',
            '--end-time', str(end_time),
            '--delta-t', str(delta_t),
            '--Re', str(Re),
            '--nu', str(nu)
        ], check=True)
        
        # Move and rename the video file
        if os.path.exists('flow_visualization.mp4'):
            new_name = f'media/flow_Re{Re}_nu{nu}.mp4'
            shutil.move('flow_visualization.mp4', new_name)
            print(f"Video saved as: {new_name}")
        
        # Extract data directly to run directory
        print("Extracting simulation data...")
        subprocess.run([
            'python3',
            'extract_data.py',
            '--output-dir', run_dir
        ], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running simulation: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main(config_file, end_time, delta_t):
    """Run multiple simulations from config file.
    
    Args:
        config_file: Path to JSON configuration file
        end_time: Simulation end time
        delta_t: Time step size
    """
    # Load and validate JSON
    try:
        with open(config_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file: {e}")
        return
        
    if not validate_json(data):
        return
        
    # Run simulations
    successful = 0
    total = len(data['nu'])
    
    for i, (nu, Re) in enumerate(zip(data['nu'], data['Re']), 1):
        if run_simulation(end_time, delta_t, Re, nu, i):
            successful += 1
            
    print(f"\nCompleted {successful}/{total} simulations")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run multiple OpenFOAM simulations')
    parser.add_argument('input', type=str, help='JSON input file')
    parser.add_argument('--end-time', type=float, required=True, help='End time for simulation')
    parser.add_argument('--delta-t', type=float, required=True, help='Time step size')
    
    args = parser.parse_args()
    main(args.input, args.end_time, args.delta_t) 