



#Eingabewerte
raumhoehe = 3 # in meter
raumflaeche = 40 # in qm
anzfenster = 2
anzaussenwaende = 3
staerkedaemmung = 6 #in cm
staerkeaussenwand = 25 # in cm

#Fixwerte
aufschlagfenster = 0.05 # 5%
aufschlagwaende = 0.05 # 5%
aufschlagueberdimensionierung = 0.1 # 10%
abschlagdaemmung = 0.02 # 2%

#uwert Berechnung - je nach Bauweise
#Wert steht in Baustofftabelle - je nach Baustoff hat man anderen lambdabaustoffwert
#kommt aus der baustoffliste- jeder Baustoff hat einen Lambdawert - finde ich in der Tabelle
lambdabaustoff = 82.5

uwert = (1-0.02*staerkedaemmung)*lambdabaustoff/staerkeaussenwand

print("uwert: ", uwert)

#Berechnung Raumvolumen
raumvolumen = raumhoehe * raumflaeche

print ("Raumvolumen:", raumvolumen)

if uwert < 1.5:
    aufschlaguwert = 0
elif uwert > 1.5 and uwert < 2.0:
    aufschlaguwert = 0.05
elif uwert > 2.0 and uwert < 2.5:
    aufschlaguwert = 0.1
elif uwert > 2.5 and uwert < 3.5:
    aufschlaguwert = 0.15
elif uwert > 3.5:
    aufschlaguwert = 0.2
else:
    print("kann uwert nicht berechnen")

print("aufschlaguwert: ", aufschlaguwert)

#prozentualen gesamtaufschlag berechnen
gesamtaufschlag = (anzfenster * aufschlagfenster) + \
                  (anzaussenwaende * aufschlagwaende) + \
                  aufschlaguwert + aufschlagueberdimensionierung - \
                  (abschlagdaemmung * staerkedaemmung)

print("gesamtaufschlag", gesamtaufschlag )

#volumenäquivalent
volumenaequivalent = raumvolumen + raumvolumen * gesamtaufschlag
print("volumenaequivalent", volumenaequivalent)

anzS = 0
anzM = 0
anzL = 0

while volumenaequivalent > 0:
    print("volaequ.: ", volumenaequivalent)
    if volumenaequivalent < 0:
        break
    elif volumenaequivalent <= 20:
        anzS = anzS + 1
        volumenaequivalent = volumenaequivalent - 20
    elif volumenaequivalent <= 50:
        anzM = anzM + 1
        volumenaequivalent = volumenaequivalent - 50
    elif volumenaequivalent >= 50:
        anzL = anzL + 1
        volumenaequivalent = volumenaequivalent - 75

print("anzS: ", anzS)
print("anzM: ", anzM)
print("anzL: ", anzL)
print("volaequ.: ", volumenaequivalent)

alternative = "x"

if alternative == "x":
    if anzS == 1 and anzL > 0:
        anzS = anzS - 1
        anzL = anzL - 1
        anzM = anzM + 2

print("nach alternative")
print("anzS: ", anzS)
print("anzM: ", anzM)
print("anzL: ", anzL)

#Heizkostenberechnung:
