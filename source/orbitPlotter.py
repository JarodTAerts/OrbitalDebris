import numpy as np
from mayavi import mlab
import pandas as pd
import math
from tvtk.api import tvtk
import matplotlib.pyplot as plt
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

if(Constants.NUM_ORBITS_PLOTTED == 0): 
    Constants.NUM_ORBITS_PLOTTED = len(debrisList)

if(Constants.PLOT_ENERGY):
    print("Getting Surface Area per Latitude...")
    latSurfArea=DataFuncs.GetTotalSurfaceAreaAtEachLatitude(debrisList)
    lats=range(-90,90)
    latReflectedEnergy=DataFuncs.GetTotalBlockedEnergyAtEachLatitude(latSurfArea)
    latReflectedEnergy=[x/1000 for x in latReflectedEnergy]

    csvDF = pd.DataFrame(data={"Latitude":lats, "Blocked":latReflectedEnergy})
    csvDF.to_csv('./data/blocked.csv', sep=',')

    print("Plotting Solar Energy...")
    plt.plot(lats, latReflectedEnergy)
    plt.suptitle("Solar Energy Blocked or Absorbed by Orbital Debris")
    plt.xlabel("Latitude")
    plt.ylabel("Reflected or Absorbed Energy (1000s of KiloWatts)")
    plt.xticks(range(-90,100,30))
    plt.grid(True)
    plt.show()


if(Constants.PLOT_ORBITS):
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

    # Set camera to focus on origin point and show the plot
    mlab.view(focalpoint=(0,0,0))
    mlab.show()


print("Done!")

