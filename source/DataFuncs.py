from Debris import Debris


def GetAverageOrbit(listODebris):
    features=[0,0,0,0]
    for deb in listODebris:
        features[0]=features[0]+deb.period
        features[1]=features[1]+deb.inclination
        features[2]=features[2]+deb.apogee
        features[3]=features[3]+deb.perigee
    features = [x / len(listODebris) for x in features]
    return( Debris("Average Orbit", "Average", features[0], features[1], features[2], features[3], "AVG") )