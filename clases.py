from datetime import date, datetime, timedelta
import requests
import json
import pandas as pd
import numpy as np

class PrecioLuz():
    """
    Clase para scrapear el precio de la luz para el día t+1 en España.
    """
    def __init__(self, url = "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real"):
        self.fecha = date.today() + timedelta(days = 1)
        self.inicio = f"{self.fecha}T00:00"
        self.fin = f"{self.fecha}T23:59"
        self.url = f"{url}?start_date={self.inicio}&end_date={self.fin}&time_trunc=hour"
        self.response = requests.get(self.url)
        self.status = self.response.status_code
        
    def PVPC(self):
        """
        Precio PVPC (€/MWh).
        Valor de interés para el público.
        """
        if self.status == 200:
            red_electrica = self.response.json()
            values = red_electrica["included"][0]["attributes"]["values"]
            datos = pd.DataFrame()
            for value in values:
                precio = round(value['value']/1000,4)
                hora_inicio = datetime.strptime(value['datetime'].split('+')[0].split('T')[1], '%H:%M:%S.%f').strftime('%H:%M %p')
                hora_fin = datetime.strptime(value['datetime'].split('+')[0].split('T')[1], '%H:%M:%S.%f') + timedelta(hours=1)
                hora_fin = hora_fin.time().strftime('%H:%M %p')
                d1 = pd.DataFrame({"€/kWh": precio, "Fecha" : self.fecha.strftime('%d/%m/%y'), "Hora inicio" : hora_inicio, "Hora fin" : hora_fin}, index = [0])
                datos = datos.append(d1)
                
            return datos
        else:
            return self.status
        
    def PMS(self):
        """
        Precio mercado spot (€/MWh).
        """
        if self.status == 200:
            red_electrica = self.response.json()
            values = red_electrica["included"][0]["attributes"]["values"]
            datos = pd.DataFrame()
            for value in values:
                precio = round(value['value']/1000,4)
                hora_inicio = datetime.strptime(value['datetime'].split('+')[0].split('T')[1], '%H:%M:%S.%f').strftime('%H:%M %p')
                hora_fin = datetime.strptime(value['datetime'].split('+')[0].split('T')[1], '%H:%M:%S.%f') + timedelta(hours=1)
                hora_fin = hora_fin.time().strftime('%H:%M %p')
                d1 = pd.DataFrame({"€/kWh": precio, "Fecha" : self.fecha.strftime('%d/%m/%y'), "Hora inicio" : hora_inicio, "Hora fin" : hora_fin}, index = [0])
                datos = datos.append(d1)
                
            return d
        else:
            return self.status
    
    @property
    def last_update(self):
        """
        Fecha de actualización de los datos.
        """
        if self.status == 200:
            red_electrica = self.response.json()
            last_update = red_electrica["included"][1]["attributes"]["last-update"].split('+')[0]
            last_update = datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%S.%f')
            return last_update
        else:
            return self.status
        
        

if __name__ == "__main__":
    precio = PrecioLuz()
    print(precio.PVPC())
    