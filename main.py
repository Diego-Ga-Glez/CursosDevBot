# pip install discord
# pip install python-dotenv
# pip install requests
# pip install beautifulsoup4

import os
import requests
import asyncio
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
          search = True
          courses = []
          page = 1
          while search:
               url = self.url + '?page=' + str(page)
               # Realiza la solicitud HTTP
               response = requests.get(url)
               
               if response.status_code != 200:
                    print('La solicitud a la página ' + str(page) + ' no fue exitosa')
                    break

               soup = BeautifulSoup(response.content, 'html.parser')

               divs_courses = soup.find_all('div', class_='w-screen') #
               if len(divs_courses) >= 2:
                    div_free_courses = divs_courses[1]
               else:
                    break #

               expired_courses = div_free_courses.find_all('span', string='Expired') #
               if len(expired_courses) == 20:
                    break #

               course_elements = div_free_courses.find_all('a', class_='c-card') #
               if not course_elements:
                    break

               for element in course_elements:
                    expired = element.find('span', string='Expired') #
                    title = element.find('h2').text.strip()
                    if not expired and self.keyword.lower() in title.lower(): #
                         link = element.get('href')
                         if link != self.last_course:
                              courses.append({
                                   'title': title,
                                   'link': link
                              })
                              if self.last_course == None:
                                   search = False
                                   break
                         else:
                              search = False
                              break
               
               if search:
                    page += 1
                    asyncio.sleep(1)
               
          if len(courses):
               self.last_course = courses[0]['link']

          return courses
          

if __name__ == '__main__':

     # Carga las variables de entorno
     load_dotenv()
     TOKEN: str = os.getenv('DISCORD_TOKEN')
     CHANNEL_ID: int = int(os.getenv('CHANNEL_ID'))

     # Crea el cliente de Discord
     client: Client = WebCrawler(channel_id_=CHANNEL_ID)
     client.run(token=TOKEN)