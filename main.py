# pip install discord
# pip install python-dotenv
# pip install requests
# pip install beautifulsoup4

import os
import requests
from discord import Client
from dotenv import load_dotenv
from discord_bot import DiscordBot
from bs4 import BeautifulSoup

class WebCrawler(DiscordBot):
     def __init__(self, channel_id_: int):

          # Hace llamar el constructor de DiscordBot
          super().__init__(channel_id=channel_id_)

          self.url: str = 'https://www.cursosdev.com/coupons'

     # El metodo debe retornar una lista de diccionarios
     def get_response(self) -> list:
          # Realiza la solicitud HTTP
          response = requests.get(self.url)
          
          if response.status_code == 200:
               courses = []

               soup = BeautifulSoup(response.content, 'html.parser')
               course_elements = soup.find_all('a', class_='c-card')

               for element in course_elements:
                    title = element.find('h2').text.strip()
                    if self.keyword.lower() in title.lower():
                         link = element.get('href')
                         if link != self.last_course:
                              courses.append({
                                   'title': title,
                                   'link': link
                                   })
                              if self.last_course == None:
                                   break
                         else:
                              break
               
               if len(courses) and self.last_course != courses[0]['link']:
                    self.last_course = courses[0]['link']
               return courses
          
          else:
               print('La solicitud no fue exitosa')
               return []
          

if __name__ == '__main__':

     # Carga las variables de entorno
     load_dotenv()
     TOKEN: str = os.getenv('DISCORD_TOKEN')
     CHANNEL_ID: int = int(os.getenv('CHANNEL_ID'))

     # Crea el cliente de Discord
     client: Client = WebCrawler(channel_id_=CHANNEL_ID)
     client.run(token=TOKEN)