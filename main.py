import os
from dotenv import load_dotenv
import asyncio
import discord
from datetime import datetime
from red_electrica import Precio_red_electrica


load_dotenv()
#Env variables
token = os.environ['TOKEN']
total_channel = os.environ['TOT']
min_channel = os.environ['MIN']

#Instancia cliente discord
client = discord.Client()


@client.event
async def on_ready():
	#Canales que recibirán los mensajes
	canal_min = client.get_channel(int(min_channel))
	canal_total = client.get_channel(int(total_channel))
	
	#Return de la API de REE.es
	'''
	lupdate: last_update: hora de carga de los datos por parte de REE
	datos: conjunto completo de datos de precios PVPC (€/MWh)
	minimo: slice del minimo
	'''
	lupdate, datos, minimo = Precio_red_electrica()

	#Envío de mensajes de precios
	minimo_formateado = minimo.to_string(justify='left',index=False)

	#Envío de datos mínimos ordenados por precio.
	#El triple acento grave da formato al mensaje en Discord para que los datos se asemejen a una tabla.
	await canal_min.send(f'```Precios mínimos por hora.\n{minimo_formateado}```')

	#Envío de datos diarios.
	total = datos.to_string(justify='left', index=False)
	await canal_total.send(f'```Precios diarios por hora.\n{total}```')

	await client.logout()

		
'''
@client.event
async def on_message(message):
		if message.author == client.user:
			return
		
		if message.content.startswith('test'):
			await message.channel.send('Bao')
		
		if message.content.startswith('canal'):
			print(message.channel.id)

		if message.content.startswith('$mantenimiento'):
				await message.channel.send('Cerrando!')
				await client.logout()

'''

client.run(token)