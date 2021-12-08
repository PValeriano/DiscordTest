import requests
import json
from datetime import date, datetime, timedelta
import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def Precio_red_electrica():


	#Fecha inicio y fin peticion de precios
	fecha = date.today() + timedelta(days=1)
	start_date = f"{fecha}T00:00"
	end_date = f"{fecha}T23:59"


	#Endpoint Red Electrica de España
	Red_electrica_API = f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={start_date}&end_date={end_date}&time_trunc=hour"

	#Peticion HTTP
	red_electrica = requests.get(Red_electrica_API)
	
	if red_electrica.status_code == 200:

		red_electrica = red_electrica.json()

		#posición 0 = PVPC (€/MWh) / posición 1 = Precio mercado spot (€/MWh)
		last_update = red_electrica["included"][0]["attributes"]["last-update"].split('+')[0]
		last_update = datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%S.%f')
		values = red_electrica["included"][0]["attributes"]["values"]

		d = pd.DataFrame()

		for value in values:
			precio = round(value['value']/1000,4)
			hora_inicio = datetime.strptime(value['datetime'].split('+')[0].split('T')[1], '%H:%M:%S.%f').strftime('%H:%M %p')
			hora_fin = datetime.strptime(value['datetime'].split('+')[0].split('T')[1], '%H:%M:%S.%f') + timedelta(hours=1)
			hora_fin = hora_fin.time().strftime('%H:%M %p')
			d1 = pd.DataFrame({"€/kWh": precio, "Fecha" : fecha.strftime('%d/%m/%y'), "Hora inicio" : hora_inicio, "Hora fin" : hora_fin}, index = [0])
			d = d.append(d1)
		
		return last_update, d, d[d['€/kWh'] == min(d['€/kWh'])]
		#return d

	else:
		print(red_electrica.status_code)
		print(red_electrica.json()['errors'])


if __name__ == '__main__':
	last_update, datos, minimo = Precio_red_electrica()
	#data = Precio_red_electrica()
	print(minimo.to_string(index=False, justify='left'))
