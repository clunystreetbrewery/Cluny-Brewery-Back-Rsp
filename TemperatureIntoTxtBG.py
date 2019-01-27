import time
import datetime

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

def sauvegarde (temperature_blue, temperature_green, temperature_yellow, date, emplacement) :
    fichierSauvegarde = open(emplacement, "a")
    fichierSauvegarde.write(str(date)+";")
    fichierSauvegarde.write(str(temperature_blue)+";")
    fichierSauvegarde.write(str(temperature_green)+";")
    fichierSauvegarde.write(str(temperature_yellow)+";")
    temperature_average = (temperature_blue + temperature_green + temperature_yellow) / 3
    fichierSauvegarde.write(str(temperature_average)+'\r\n')
    fichierSauvegarde.close()

while True :
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    contenuFich_blue = lireFichier("/sys/bus/w1/devices/28-fdda8f1d64ff/w1_slave")
    temperature_blue = recupTemp(contenuFich_blue)
    contenuFich_green = lireFichier("/sys/bus/w1/devices/28-f5d58f1d64ff/w1_slave")
    temperature_green = recupTemp(contenuFich_green)
    contenuFich_yellow = lireFichier("/sys/bus/w1/devices/28-97d68f1d64ff/w1_slave")
    temperature_yellow = recupTemp(contenuFich_yellow)
    sauvegarde(temperature_blue, temperature_green, temperature_yellow, date, "TemperatureTexte.csv")
    time.sleep(2000)

