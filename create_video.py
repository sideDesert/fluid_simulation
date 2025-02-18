#!/usr/bin/env python3
from paraview.simple import *
import os

# Disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Get the case directory path
case_dir = os.path.abspath("flow_cylinder")
foam_file = os.path.join(case_dir, "flow_cylinder.foam")

# Read the OpenFOAM case
foam = OpenFOAMReader(FileName=foam_file)
foam.MeshRegions = ['internalMesh']
foam.CellArrays = ['U']

# Create a new 'Render View'
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.Background = [0.32, 0.34, 0.43]  # Match your screenshot background
renderView.OrientationAxesVisibility = False

# Show the data
foam_display = Show(foam, renderView)
foam_display.Representation = 'Surface'

# Color by velocity magnitude
ColorBy(foam_display, ('POINTS', 'U', 'Magnitude'))

# Modify the color transfer function
velocity_LUT = GetColorTransferFunction('U')
velocity_LUT.RescaleTransferFunction(0.0, 0.4)
velocity_LUT.ApplyPreset('Rainbow Desaturated', True)

# Show color bar
foam_display.SetScalarBarVisibility(renderView, True)

# Set up basic camera
renderView.InteractionMode = '2D'
renderView.ResetCamera()

# Add timestamp
annotateTime = AnnotateTimeFilter(Input=foam)
timeDisplay = Show(annotateTime, renderView)
timeDisplay.WindowLocation = 'Upper Left Corner'

# Set up animation scene
animation = GetAnimationScene()
animation.UpdateAnimationUsingDataTimeSteps()

# Save animation
SaveAnimation(
    'flow_visualization.avi',
    renderView,
    ImageResolution=[1920, 1080],
    FrameRate=24,
    Type='mp4'
) 
