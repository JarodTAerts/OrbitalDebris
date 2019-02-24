# Orbital Debris
This is a repo which contains my work with orbital space debris and its effect on earth's atmosphere and enviroment. All source code for this project is in python. This code is completely open sourced and can be used by anyone for any purpose.

## Required Python Packages

- Numpy
  - Used for various calculations.
  - Installation: ```pip install numpy```
- MayAvi MLab
  - Used for ploting and displaying the orbits in 3d space.
  - Installation: ```pip install mayavi```
- Pandas
  - Used for reading in the data from a csv file and organizing it with pandas dataframes.
  -  Installation: ```pip install pandas```

## Running the Simulation

1. Install all required python packages noted above.
2. Navigate to the __./OrbitalDebris__ directory.
3. Run the __orbitPlotter.py__ python script with python. Something like: ```python ./source/orbitPlotter.py```.

## Notes
- If you decide to run the script from a different location, such as inside the source folder, you may have to change the constants __DATA_FILE_PATH__ and __EARTH_IMAGE_PATH__ in __orbitPlotter.py__ so the can be properly loaded.
- If you choose to plot a different number of orbits by changing __NUM_ORBITS_PLOTTED__ in __orbitPlotter.py__ it may take a very long time to load due to the slow render times with MayAvi.
- The thick black orbit shown in the plot is the average orbit of all orbits in the dataset.

## Sources
- Datafile containing all the orbits of the orbital debris can be found here <https://www.space-track.org/auth/login>. A valid account will be needed to access data.
- Earth Image is NASA's Blue Marble texture image and can be found here <https://visibleearth.nasa.gov/view.php?id=73909>.