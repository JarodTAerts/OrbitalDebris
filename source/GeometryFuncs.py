import math
import Constants

# METHOD ZValToLatitude: Converts position of a orbit to a latitude value on the earth
# PARAMETER xVal: xVal of position in orbit. This is always x since all orbits are inclined the same way
# PARAMETER zVal: Z value in absolute graphing space of the position in the orbit
# PARAMETER inclination: Inclination of orbit
def ZValToLatitude(xVal, zVal, inclination):
    theta=DegreesToRadians(inclination)
    r=(xVal/abs(xVal))*math.sqrt(math.pow(xVal,2)+math.pow(zVal,2))
    realZ=r*math.sin(theta)

    if(abs(realZ) < Constants.EARTH_R):
        latVal=round(RadiansToDegrees(math.asin(realZ/Constants.EARTH_R)))

        if(latVal>-90 and latVal<90):
            return latVal
    return -999

# METHOD DegreesToRadians: Converts degrees to radians
# PARAMETER degrees: Value of degrees to be converted 
def DegreesToRadians(degrees):
    return degrees*math.pi/180

# METHOD RadiansToDegrees: Converts radians to degrees
# PARAMETER radians: Value in radians to be converted
def RadiansToDegrees(radians):
    return radians*180/math.pi