import numpy as np
import math

minInYear=525600

class Debris():

    def __init__(self, name, objectType, period, inclination, apogee, perigee, size):
        self.name=name
        self.objectType=objectType
        self.period=period
        self.inclination=inclination
        self.apogee=apogee
        self.perigee=perigee
        self.size=size

    def ToString(self):
        return(str(self.apogee)+" - "+str(self.perigee))

    # METHOD GetPercentageAtLatitudes: Gets what percentage of the time the piece of debris spends at each latitude
    # PARAMETER planetR: Radius of planet
    # PARAMETER planetTilt: Tilt of planet on its axis of rotation
    def GetPercentageAtLatitudes(self, planetR, planetTilt):
        points=self.GetPointsOfOrbit(planetR*2, planetTilt)
        latitudePercent=[0]*180

        # Loop through all the z values of the orbit
        for x,z in zip(points[0],points[2]):
            # Calculate the latitude the object is at when it is at this z value
            theta=self.DegreesToRadians(self.inclination)
            r=(x/abs(x))*math.sqrt(math.pow(x,2)+math.pow(z,2))
            realZ=r*math.sin(theta)
            if(abs(realZ)<planetR):
                latVal=round(self.RadiansToDegrees(math.asin(realZ/planetR)))
                # If it is within the right range add one to that latitude
                if(latVal>-90 and latVal<90):
                    latitudePercent[90+latVal]=latitudePercent[90+latVal]+1

        # Convert all the latitudes into percentages based on the number of points in the orbit
        latitudePercent=[x / len(points[2]) for x in latitudePercent]
        return(latitudePercent)

    def GetYearlyTimeSpentAtLatitudes(self, planetR, planetTilt):
        latitudePercents=self.GetPercentageAtLatitudes(planetR, planetTilt)
        return([x * minInYear for x in latitudePercents])

    def DegreesToRadians(self, degrees):
        return degrees*math.pi/180
    
    def RadiansToDegrees(self, radians):
        return radians*180/math.pi

    # METHOD GetPointsOfOrbit: Gets the points in 3d space that can be used to plot the orbit
    # PARAMETER planetD: Diameter of planet the orbit will be plotted around
    # PARAMETER planetTilt: Tilt of planet on its axis 
    def GetPointsOfOrbit(self, planetD, planetTilt):
        planetR=planetD/2
        # Adjust the apogee and perigee to be from the earths center not the surface
        adjApogee=self.apogee+planetR
        adjPerigee=self.perigee+planetR
        # Calculate the eccentricity and the semi major axis of the orbit
        e=(adjApogee-adjPerigee)/(adjApogee+adjPerigee)
        a=(adjApogee+adjPerigee)/2
        # Take the inclination, adjust it for the earths tilt so it plots correctly and then convert to radians
        inc=(self.inclination-planetTilt)*math.pi/180

        xmat=[]
        ymat=[]
        zmat=[]

        # Loop through alittle more than 1 revolution and calculate points for the orbit
        for i in np.arange(0, 2.05*math.pi, 2*math.pi/360):
            x=a*(math.cos(i)-e)
            y=a*math.sqrt(1-math.pow(e,2))*math.sin(i)   
            # Rotate the orbit around the Y axis based on the inclination by adjusting the x and y coordinates    
            z=x*math.sin(inc)
            x=x*math.cos(inc)
            xmat.append(x)
            ymat.append(y)
            zmat.append(z)
        
        return(xmat,ymat,zmat)

    # METHOD GetColor: Gets the color of the orbit plot based on the size of the object
    def GetColor(self):
        if(self.size=="SMALL"):
            return (0,1,0)
        if(self.size=="MEDIUM"):
            return (0,1,1)
        if(self.size=="LARGE"):
            return (0,0,1)
        if(self.size=="AVG"):
            return(0.1, 0.1, 0.1)
        return (1,1,0)


    # METHOD PlotOrbit: Plots the orbit of the piece of debris on a mlab figure
    # PARAMETER plot: mlab plot that the orbit will be added to
    # PARAMETER planetD: Diameter of the planet the orbit will be plotted around
    # PARAMETER lineRadius: Thickness of orbit line that will be plotted
    # PARAMETER planetTilt: Tilt of planet on its axis or rotation
    def PlotOrbit(self, plot, planetD, lineRadius, planetTilt):
        points=self.GetPointsOfOrbit(planetD, planetTilt)
        plot.plot3d(points[0], points[1], points[2], color=self.GetColor(), tube_radius=lineRadius, tube_sides=3)
    

