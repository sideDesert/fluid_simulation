"""Script to run OpenFOAM simulation and create ParaView visualization."""

import os
import subprocess
from extract_data import extract_simulation_data


def modify_transport_properties(transport_properties_path, nu):
    """Modify transportProperties file with new kinematic viscosity value.
    
    Args:
        transport_properties_path: Path to the transportProperties file
        nu: New kinematic viscosity value
    """
    with open(transport_properties_path, 'r') as file:
        lines = file.readlines()
    
    modified_lines = []
    for line in lines:
        if 'nu' in line and '[' in line and ']' in line:
            modified_lines.append(f'nu              {nu} [0 2 -1 0 0 0 0];\n')
        else:
            modified_lines.append(line)
    
    with open(transport_properties_path, 'w') as file:
        file.writelines(modified_lines)


def modify_control_dict(control_dict_path, end_time, delta_t):
    """Modify controlDict file with new endTime and deltaT values.
    
    Args:
        control_dict_path: Path to the controlDict file
        end_time: New end time value
        delta_t: New time step size
    """
    with open(control_dict_path, 'r') as file:
        lines = file.readlines()
    
    modified_lines = []
    for line in lines:
        if 'endTime' in line and 'stopAt' not in line:
            modified_lines.append(f'endTime         {end_time};\n')
        elif 'deltaT' in line:
            modified_lines.append(f'deltaT          {delta_t};\n')
        elif 'writeControl' in line:
            modified_lines.append('writeControl    runTime;\n')
        elif 'writeInterval' in line:
            modified_lines.append('writeInterval   0.1;\n')
        else:
            modified_lines.append(line)
    
    with open(control_dict_path, 'w') as file:
        file.writelines(modified_lines)


def run_openfoam_simulation(case_dir):
    """Run OpenFOAM simulation using icoFoam from the case directory.
    
    Args:
        case_dir: Path to the OpenFOAM case directory
        
    Returns:
        bool: True if simulation successful, False otherwise
    """
    try:
        # Change to the case directory
        original_dir = os.getcwd()
        os.chdir(case_dir)
        
        # Run the simulation
        subprocess.run(['icoFoam'], check=True)
        
        # Change back to original directory
        os.chdir(original_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running simulation: {e}")
        # Make sure to return to original directory even if there's an error
        os.chdir(original_dir)
        return False


def create_paraview_visualization(case_dir):
    """Create flow visualization using ParaView.
    
    Args:
        case_dir: Path to the OpenFOAM case directory
    """
    # Create frames directory
    os.makedirs('frames', exist_ok=True)
    
    # Generate ParaView state file
    paraview_state = f'''
# ParaView State File
from paraview.simple import *
import os
os.makedirs('frames', exist_ok=True)
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'OpenFOAM Reader'
foam = OpenFOAMReader(FileName='{os.path.join(case_dir, "flow_cylinder.foam")}')
foam.MeshRegions = ['internalMesh']
foam.CellArrays = ['U', 'p']

# Get animation scene
scene = GetAnimationScene()
scene.PlayMode = 'Snap To TimeSteps'

# Get active view
renderView = GetActiveViewOrCreate('RenderView')

# Show data
foamDisplay = Show(foam, renderView)

# Color by velocity magnitude
ColorBy(foamDisplay, ('POINTS', 'U', 'Magnitude'))

# Set up a better color scheme
velocityLUT = GetColorTransferFunction('U')
velocityLUT.RGBPoints = [0.0, 0.0, 0.0, 1.0,  # Blue for low velocity
                        0.5, 1.0, 1.0, 1.0,    # Cyan for medium
                        1.0, 1.0, 0.0, 0.0]    # Red for high velocity
velocityLUT.ColorSpace = 'HSV'

# Add streamlines
streamTracer = StreamTracer(Input=foam)
streamTracer.SeedType = 'Line'
streamTracer.Vectors = ['POINTS', 'U']
streamTracer.MaximumStreamlineLength = 20.0

# Configure seed line
seed = streamTracer.SeedType
seed.Point1 = [-1.0, -2.0, 0.0]
seed.Point2 = [-1.0, 2.0, 0.0]
seed.Resolution = 20

# Show streamlines
streamTracerDisplay = Show(streamTracer, renderView)
ColorBy(streamTracerDisplay, ('POINTS', 'U', 'Magnitude'))
streamTracerDisplay.LookupTable = velocityLUT

# Add color bar
foamDisplay.SetScalarBarVisibility(renderView, True)
scalarBar = GetScalarBar(velocityLUT, renderView)
scalarBar.Title = 'Velocity Magnitude'
scalarBar.ComponentTitle = ''
scalarBar.TitleFontSize = 8
scalarBar.LabelFontSize = 6
scalarBar.Position = [0.85, 0.05]
scalarBar.ScalarBarLength = 0.25

# Set up the view
renderView.CameraPosition = [10.0, 0.0, 40.0]
renderView.CameraFocalPoint = [10.0, 0.0, 0.0]
renderView.CameraViewUp = [0.0, 1.0, 0.0]
renderView.CameraParallelScale = 15

# Set background
renderView.Background = [1.0, 1.0, 1.0]  # White background

# Save animation
scene.GoToFirst()
print("Saving animation frames...")
timesteps = foam.TimestepValues
for i in range(len(timesteps)):
    scene.AnimationTime = timesteps[i]
    Render()
    SaveScreenshot('frames/frame_%04d.png' % i, renderView,
                  ImageResolution=[1920, 1080])
    print('Frame %d of %d' % (i+1, len(timesteps)))

print("Creating video from frames...")
'''

    # Write ParaView state file
    with open('visualization.py', 'w') as f:
        f.write(paraview_state)

    # Run ParaView in batch mode
    subprocess.run(['pvbatch', 'visualization.py'], check=True)

    # Create video from frames using ffmpeg
    try:
        subprocess.run([
            'ffmpeg', '-framerate', '10',
            '-pattern_type', 'glob',
            '-i', 'frames/frame_*.png',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-b:v', '5000k', 'flow_visualization.mp4'
        ], check=True)
        
        # Only cleanup if video creation was successful
        subprocess.run(['rm', '-rf', 'frames'], check=True)
        subprocess.run(['rm', 'visualization.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating video: {e}")
        print("Frames are preserved in the 'frames' directory")


def calculate_nu_from_reynolds(Re, velocity, characteristic_length=0.01):
    """Calculate kinematic viscosity from Reynolds number.
    
    Args:
        Re: Reynolds number
        velocity: Free stream velocity (m/s)
        characteristic_length: Cylinder diameter (m), default is 0.01m (1cm)
    Returns:
        nu: Kinematic viscosity (m²/s)
    """
    return (velocity * characteristic_length) / Re


def main(end_time, delta_t, Re, velocity):
    """Main function to run simulation and create visualization."""
    # Calculate nu from Reynolds number
    nu = calculate_nu_from_reynolds(Re, velocity)
    print(f"Calculated kinematic viscosity: {nu} m²/s")
    
    # Paths to configuration files
    case_dir = "flow_cylinder"
    control_dict_path = os.path.join(case_dir, "system", "controlDict")
    transport_properties_path = os.path.join(case_dir, "constant", "transportProperties")
    
    # Modify configuration files
    modify_control_dict(control_dict_path, end_time, delta_t)
    modify_transport_properties(transport_properties_path, nu)
    
    # Run simulation
    print(f"Running simulation with Re={Re}, U={velocity}, endTime={end_time}, deltaT={delta_t}")
    if run_openfoam_simulation(case_dir):
        print("Simulation completed successfully")
        
        # Create ParaView visualization
        print("Creating flow visualization...")
        create_paraview_visualization(case_dir)
        print("Visualization created: flow_visualization.mp4")
    else:
        print("Simulation failed")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run OpenFOAM simulation with custom parameters')
    parser.add_argument('--end-time', type=float, required=True, help='End time for simulation')
    parser.add_argument('--delta-t', type=float, required=True, help='Time step size')
    parser.add_argument('--Re', type=float, required=True, help='Reynolds number')
    parser.add_argument('--velocity', type=float, required=True, help='Inlet velocity (m/s)')
    
    args = parser.parse_args()
    main(args.end_time, args.delta_t, args.Re, args.velocity) 