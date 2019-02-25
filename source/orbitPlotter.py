import numpy as np
from mayavi import mlab
import pandas as pd
import math
from tvtk.api import tvtk
from Debris import Debris
import DataFuncs
import Constants

# Load in data from CSV file, and get rid of all items no longer in orbit or with bad data
print("Loading in Data...")
debrisDF=pd.read_csv(Constants.DATA_FILE_PATH)
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
textureReader.file_name=Constants.EARTH_IMAGE_PATH
texture = tvtk.Texture(input_connection=textureReader.output_port, interpolate=1)
# create the sphere source with a given radius and angular resolution
sphere = tvtk.TexturedSphereSource(radius=Constants.EARTH_R, theta_resolution=180,phi_resolution=180)
# assemble rest of the pipeline, assign texture    
sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
mlab.gcf().scene.add_actor(sphere_actor)
sphere_actor.rotate_y(23.5)

print("Plotting Orbits...")
# Plot the orbits of the objects in the debris list
for i in range(0, Constants.NUM_ORBITS_PLOTTED):
    print('\r\tPlotting orbit %d of %d' % (i,Constants.NUM_ORBITS_PLOTTED), end='\r' )
    debrisList[i].PlotOrbit(mlab, 10)
print('\r\tPlotted %d orbits out of %d total orbits.' % (Constants.NUM_ORBITS_PLOTTED, len(debrisList)))

averageDeb=DataFuncs.GetAverageOrbit(debrisList)
averageDeb.PlotOrbit(mlab, 100)

deb=Debris("Test Debris", "DEBRIS", 90, 10, 1000, 1000, "")
#print(deb.GetPercentageAtLatitudes(EARTH_R, EARTH_TILT))
deb.PlotOrbit(mlab, 200)


latSurfArea=DataFuncs.GetTotalSurfaceAreaAtEachLatitude(debrisList)

count=-90
for area in latSurfArea:
    print("Latitude %d: %f M^2" % (count, area))
    count+=1

print("Done!")
# Set camera to focus on origin point and show the plot
mlab.view(focalpoint=(0,0,0))
mlab.show()




