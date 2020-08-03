import time
import datetime
import sqlite3
import csv
import requests
import RPi.GPIO as GPIO

def toggleFridge (temp):
    print("temperature blue : " + str(temp))
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    channel = 15
    GPIO.setup(channel, GPIO.OUT)
    fridgeStatus = GPIO.input(channel)
    print("fridgeStatus : " + str(fridgeStatus))
    if fridgeStatus == 1:
        if temp < 11:
            GPIO.output(15, 0)
            print("turning fridge off")
    else:
        if temp > 15:
            GPIO.output(15, 1)
            print("turning fridge on")
    print("new fridge status : " + str(GPIO.input(channel)))
    # GPIO.cleanup()

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

def sauvegardeDansDb(temperature_blue, temperature_green, temperature_yellow, date, db):
    temperature_average = (temperature_blue + temperature_green + temperature_yellow) / 3
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO temperatures(date,  temperature_blue, temperature_green, temperature_yellow, temperature_average) VALUES (?, ?, ?, ?, ?)", (date, temperature_blue, tempe$
    conn.commit()
    conn.close()

def sauvegardeDansDb_old(temperature_blue, temperature_green, temperature_yellow, date, db):
    temperature_average = (temperature_blue + temperature_green + temperature_yellow) / 3
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO temperatures VALUES (?, ?, ?, ?, ?)", (date, temperature_blue, temperature_green, temperature_yellow, temperature_average))
    conn.commit()
    conn.close()

def postData(temperature_blue, temperature_green, temperature_yellow, date, url):
    data = {"date": date, "temperature_blue": temperature_blue, "temperature_green":temperature_green,  "temperature_yellow":temperature_yellow}
    response = requests.post(url, json=data, auth=('rasp', 'apiipa'))
    print(response.status_code)


date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
contenuFich_blue = lireFichier("/sys/bus/w1/devices/28-fdda8f1d64ff/w1_slave")
temperature_blue = recupTemp(contenuFich_blue)
contenuFich_green = lireFichier("/sys/bus/w1/devices/28-f5d58f1d64ff/w1_slave")
temperature_green = recupTemp(contenuFich_green)
contenuFich_yellow = lireFichier("/sys/bus/w1/devices/28-97d68f1d64ff/w1_slave")
temperature_yellow = recupTemp(contenuFich_yellow)
sauvegarde(temperature_blue, temperature_green, temperature_yellow, date, "/home/pi/Desktop/TemperatureConnected/TemperatureTexte.csv")
sauvegardeDansDb(temperature_blue, temperature_green, temperature_yellow, date, "/home/pi/Desktop/TemperatureConnected/temperatures.db")
postData(temperature_blue, temperature_green, temperature_yellow, date, "http://3.20.162.22:6789/temperatures/v2.0")
toggleFridge(temperature_blue)