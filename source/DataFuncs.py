from Debris import Debris
import Constants

# METHOD GetAverageOrbit: Gets the average orbit from a list of debris with respect ot the period, inclindation, apogee, and perigee
# PARAMETER listODebris: List of debris objects
def GetAverageOrbit(listODebris):
    features=[0,0,0,0]
    # Loop through all the debris objects and add up the important values
    for deb in listODebris:
        features[0]=features[0]+deb.period
        features[1]=features[1]+deb.inclination
        features[2]=features[2]+deb.apogee
        features[3]=features[3]+deb.perigee
    # Divide each important values by the number of items in the list to get the average
    features = [x / len(listODebris) for x in features]
    # Return a debris object with the average orbit
    return( Debris("Average Orbit", "Average", features[0], features[1], features[2], features[3], "AVG") )

# METHOD GetTotalSurfaceAreaAtEachLatitude: Gets the total surface area present throughout a year at each latitude
# PARAMETER listOfDebris: List of debris objects 
def GetTotalSurfaceAreaAtEachLatitude(listOfDebris):
    latitudeSurfArea=[0]*180
    for deb in listOfDebris:
        surfArea=deb.GetSurfaceArea()
        latPercents=deb.GetPercentageAtLatitudes()
        # Get the amount of the debris surface area that is in each latitude throughout the year
        latPercents=[x * surfArea for x in latPercents]
        # Add to total
        latitudeSurfArea=[x + y  for x, y in zip(latitudeSurfArea, latPercents)]
    return latitudeSurfArea

# METHOD GetTotalBlockedEnergyAtEachLatitude: Get the amount of energy reflected or absorbed by orbital debris at each latitude
# PARAMETER latitudeSurfArea: Amount of debris surface area at each latitidue
# RETURNS: Reflected or abosrbed energy by latitude in Kw
def GetTotalBlockedEnergyAtEachLatitude(latitudeSurfArea):
    return [x * Constants.SOLAR_CONSTANT/1000 * Constants.YEARLY_KW_SCALE for x in latitudeSurfArea]