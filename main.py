# pip install discord
# pip install python-dotenv

import os
import asyncio
from dotenv import load_dotenv
from discord import Intents, Client, TextChannel

# Carga las variables de entorno
load_dotenv()
DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN')
CHANNEL_ID: int = int(os.getenv('CHANNEL_ID'))

# Crea el cliente de Discord
intents: Intents = Intents.default()
client: Client = Client(intents=intents)

async def send_message() -> None:
    channel: TextChannel  = client.get_channel(CHANNEL_ID)
    while True:
        await channel.send(content="Este es un mensaje periódico del bot.")
        await asyncio.sleep(10)  # Espera 10 segundos antes de enviar el próximo mensaje

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')
    asyncio.create_task(send_message())  # Crea una tarea para enviar mensajes

def start_bot() -> None:
    client.run(token=DISCORD_TOKEN)

if __name__ == '__main__':
    start_bot()