# Objet du script :
# Exemple de configuration des GPIO pour une gestion des boutons de la NUCLEO-WB55

from machine import Pin # Contrôle des broches
from time import sleep_ms # Pour faire des pauses système

from time import sleep_ms, time # Pour gérer les temporisations et l'horodatage
import bluetooth # Pour gérer le protocole BLE 
import ble_sensor # Pour l'implémentation du protocole GATT Blue-ST
import pyb # pour gérer les GPIO

from machine import I2C

# On utilise l'I2C n°1 de la carte NUCLEO-W55 pour communiquer avec les capteurs
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instance du HTS221
#sensor = hts221.HTS221(i2c)

# Tension de référence / étendue de mesure de l'ADC : +3.3V
varef = 3.3

# Résolution de l'ADC 12 bits = 2^12 = 4096 (mini = 0, maxi = 4095)
RESOLUTION = const(4096)

# Quantum de l'ADC
quantum = varef / (RESOLUTION -1)

# Initialisation de l'ADC sur la broche A0
adc_A0 = pyb.ADC(pyb.Pin( 'A0' ))

# Initialisations pour calcul de la moyenne
Nb_Mesures = 500
Inv_Nb_Mesures = 1 / Nb_Mesures

command = """curl.exe -v -X POST -d "{\"temperature\": 12}" https://im2ag-thingboard.univ-grenoble-alpes.fr/api/v1/pl5LW7U0HSxHrrhpelJI/telemetry --header "Content-Type:application/json" --ssl-no-revoke"""


ble = bluetooth.BLE() # Instance de la classe BLE
ble_device = ble_sensor.BLESensor(ble) # Instance de la classe Blue-ST


while True: # Boucle "infinie" (sans clause sortie)	
	somme_tension = 0
	moyenne_poids = 0
	
	# Calcul de la moyenne de la tension aux bornes du potentiomètre

	for i in range(Nb_Mesures): # On fait Nb_Mesures conversions de la tension d'entrée
		
		# Lit la conversion de l'ADC (un nombre entre 0 et 4095 proportionnel à la tension d'entrée)
		valeur_numerique = adc_A0.read()
		
		# On calcule à présent la tension (valeur analogique) 
		tension = valeur_numerique * quantum

		# On l'ajoute à la valeur calculée à l'itération précédente
		somme_tension = somme_tension + tension

		# Temporisation pendant 1 ms
		sleep_ms(1)
	
	# On divise par Nb_Mesures pour calculer la moyenne de la tension du potentiomètre
	moyenne_poids = somme_tension * Inv_Nb_Mesures
	moyenne_poids = moyenne_poids * 100
	
	# Affichage de la tension moyenne sur le port série de l'USB USER
	print( "Le poids est : %d g\n" %moyenne_poids)


# while True: # Boucle sans clause de sortie
	somme_tension = 0
	moyenne_poids = 0
	timestamp = time()
	# Temporisation pendant 300ms
	sleep_ms(300)
	
	# Calcul de la moyenne de la tension aux bornes du potentiomètre

	for i in range(Nb_Mesures): # On fait Nb_Mesures conversions de la tension d'entrée
		
		# Lit la conversion de l'ADC (un nombre entre 0 et 4095 proportionnel à la tension d'entrée)
		valeur_numerique = adc_A0.read()
		
		# On calcule à présent la tension (valeur analogique) 
		tension = valeur_numerique * quantum

		# On l'ajoute à la valeur calculée à l'itération précédente
		somme_tension = somme_tension + tension

		# Temporisation pendant 1 ms
		sleep_ms(1)
	
	# On divise par Nb_Mesures pour calculer la moyenne de la tension du potentiomètre
	moyenne_poids = somme_tension * Inv_Nb_Mesures
	moyenne_poids = int(moyenne_poids * 100)
	
	# Affichage de la tension moyenne sur le port série de l'USB USER
	print( "Le poids est : %d g\n" %moyenne_poids)
	
	stime = str(timestamp)
    
	# Envoi en BLE de l'horodatage et de la température en choisissant de notifier l'application
	ble_device.set_data_temperature(timestamp, moyenne_poids, notify=1) 


