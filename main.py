# Aqui se ejecuta todo lo relacionado al web crawler
# get_response puede llegar a utilizar la variable
# last_course y keyword declaradas en main.py

import os
from discord import Client
from dotenv import load_dotenv
from discord_bot import DiscordBot

class WebCrawler(DiscordBot):
     def __init__(self, channel_id_: int):

          # Hace llamar el constructor de DiscordBot
          super().__init__(channel_id=channel_id_)

          self.url: str = 'https://www.cursosdev.com/coupons'

     # El metodo debe retornar una lista de diccionarios
     def get_response(self) -> list:
          # return [
          #           {
          #                'titulo' : 'curso1',
          #                'descripcion:' : 'Este es el curso 1'
          #           }, 
          #           {
          #                'titulo' : 'curso2',
          #                'descripcion:' : 'Este es el curso 2'
          #           }
          #        ]

          return[]
     
     # Metodo opcional (?)
     def format_response(self, response: dict) -> str:
          return response['titulo']
          

if __name__ == '__main__':

     # Carga las variables de entorno
     load_dotenv()
     TOKEN: str = os.getenv('DISCORD_TOKEN')
     CHANNEL_ID: int = int(os.getenv('CHANNEL_ID'))

     # Crea el cliente de Discord
     client: Client = WebCrawler(channel_id_=CHANNEL_ID)
     client.run(token=TOKEN)