def lireFichier (emplacement) :
    fichTemp = open(emplacement)
    contenu = fichTemp.read()
    fichTemp.close()
    return contenu

def recupTemp (contenuFich) :
    secondeLigne = contenuFich.split("\n")[1]
    temperatureData = secondeLigne.split(" ")[9]
    temperature = float(temperatureData[2:])
    temperature = temperature / 1000
    return temperature

contenuFich1 = lireFichier("/sys/bus/w1/devices/28-97d68f1d64ff/w1_slave")
contenuFich2 = lireFichier("/sys/bus/w1/devices/28-f5d58f1d64ff/w1_slave")
contenuFich3 = lireFichier("/sys/bus/w1/devices/28-fdda8f1d64ff/w1_slave")

temperature1 = recupTemp (contenuFich1)
temperature2 = recupTemp (contenuFich2)
temperature3 = recupTemp (contenuFich3)

print "Temperature Capteur Jaune : " ,
print temperature1
print "Temperature Capteur Vert : " ,
print temperature2
print "Temperature Capteur Bleu : " ,
print temperature3
