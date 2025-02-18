import numpy as np
import matplotlib.pyplot as plt
import re
import os

def read_velocity_data(case_dir):
    """Read velocity data from all time directories.
    
    Args:
        case_dir: Path to OpenFOAM case directory
    Returns:
        times: List of time values
        velocities: List of velocity magnitudes
    """
    times = []
    velocities = []
    
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
        try:
            U_file = os.path.join(case_dir, time_dir, 'U')
            if not os.path.exists(U_file):
                continue
                
            with open(U_file, 'r') as f:
                content = f.read()
                # Find the vector data section
                match = re.search(r'\(\s*\(([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s+([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s+([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\)', content)
                
                if match:
                    vx, vy, vz = map(float, match.groups())
                    vel_mag = np.sqrt(vx*vx + vy*vy + vz*vz)
                    times.append(float(time_dir))
                    velocities.append(vel_mag)
        except Exception as e:
            print(f"Error reading velocity from {U_file}: {str(e)}")
            continue
    
    # Sort by time
    sorted_data = sorted(zip(times, velocities))
    if sorted_data:
        times, velocities = zip(*sorted_data)
    
    return np.array(times), np.array(velocities)

# Read the velocity data
case_dir = "flow_cylinder"
times, velocities = read_velocity_data(case_dir)

if len(times) == 0:
    print("No velocity data found!")
    exit(1)

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(times, velocities, 'b-', linewidth=1.5)
plt.xlabel('Time (s)')
plt.ylabel('Velocity Magnitude (m/s)')
plt.title('Velocity Magnitude vs Time')
plt.grid(True)

# Set reasonable margins on the x-axis
if len(times) > 0:
    max_time = times[-1]
    plt.xlim(0, max_time + max_time * 0.05)  # Add 5% margin

# Save the plot
plt.savefig('velocity_plot.png', dpi=300, bbox_inches='tight')
plt.close() 