import numpy as np
from mayavi import mlab
import pandas as pd
import math
from tvtk.api import tvtk
from Debris import Debris
import DataFuncs

# Set constants for size of earth
EARTH_D=12742
EARTH_R=EARTH_D/2
EARTH_TILT=23.5
DATA_FILE_PATH="./data/debris.csv"
EARTH_IMAGE_PATH="./images/earth.jpg"
NUM_ORBITS_PLOTTED=100


# Load in data from CSV file, and get rid of all items no longer in orbit or with bad data
print("Loading in Data...")
debrisDF=pd.read_csv(DATA_FILE_PATH)
debrisDF=debrisDF.loc[(debrisDF['DECAY'].isnull()) & (np.isfinite(debrisDF['INCLINATION'])) & (np.isfinite(debrisDF['APOGEE'])) & (np.isfinite(debrisDF['PERIGEE']))]
# Fix size column where there is no data
debrisDF.fillna({'RCS_SIZE': ""})

# From that dataframe above create a list of Debris objects
print("Creating Debris Objects...")
debrisList=[]
for index, row in debrisDF.iterrows():
    newDeb=Debris(row['SATNAME'], row['OBJECT_TYPE'], row['PERIOD'], row['INCLINATION'], row['APOGEE'], row['PERIGEE'], row['RCS_SIZE'])
    debrisList.append(newDeb)

# Get the texture for earth
textureReader = tvtk.JPEGReader()
textureReader.file_name=EARTH_IMAGE_PATH
texture = tvtk.Texture(input_connection=textureReader.output_port, interpolate=1)
# create the sphere source with a given radius and angular resolution
sphere = tvtk.TexturedSphereSource(radius=EARTH_R, theta_resolution=180,phi_resolution=180)
# assemble rest of the pipeline, assign texture    
sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
mlab.gcf().scene.add_actor(sphere_actor)
sphere_actor.rotate_y(23.5)

print("Plotting Orbits...")
# Plot the orbits of the objects in the debris list
for i in range(0, NUM_ORBITS_PLOTTED):
    print('\r\tPlotting orbit %d of %d' % (i,NUM_ORBITS_PLOTTED), end='\r' )
    debrisList[i].PlotOrbit(mlab, EARTH_D, 10, EARTH_TILT)
print('\r\tPlotted %d orbits out of %d total orbits.' % (NUM_ORBITS_PLOTTED, len(debrisList)))

averageDeb=DataFuncs.GetAverageOrbit(debrisList)
averageDeb.PlotOrbit(mlab, EARTH_D, 100, EARTH_TILT)

deb=Debris("Test Debris", "DEBRIS", 90, 10, 1000, 1000, "")
#print(deb.GetYearlyTimeSpentAtLatitudes(EARTH_R, EARTH_TILT))
deb.PlotOrbit(mlab, EARTH_D, 200, EARTH_TILT)

print("Done!")
# Set camera to focus on origin point and show the plot
mlab.view(focalpoint=(0,0,0))
mlab.show()




