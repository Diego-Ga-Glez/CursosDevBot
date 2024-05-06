import asyncio
from discord import Intents, Client, TextChannel, Message

class DiscordBot(Client):

    def __init__(self, channel_id: int):

        # Hace llamar el constructor del paquete de discord
        intents: Intents = Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        self.task: asyncio.Task = None
        self.last_course: str = None
        self.keyword: str = None

        self.channel_id: int = channel_id
        self.channel: TextChannel = None
        
    async def on_ready(self):
        print(f'Conectado como {self.user}')
        self.channel = self.get_channel(self.channel_id)
        print(f'Los mensajes de {self.user} seran enviados a {self.channel.name}')

    
    async def send_message(self) -> None:
        while True:

            response: list = self.get_response()
            for r in response:
                await self.channel.send(content=self.format_response(r))

            await asyncio.sleep(10)  # Espera 10 segundos antes de enviar el próximo mensaje

    async def on_message(self, message: Message) -> None:
        # Verifica que el mensaje no sea del bot
        if message.author == self.user:
            return

        self.keyword = message.content
        await self.channel.send(content=f'¡Perfecto! A partir de ahora, te enviaré cursos específicos sobre {self.keyword}. Aquí tienes el último en la serie.')

        if self.task is not None:
            self.task.cancel()
        self.task = asyncio.create_task(self.send_message())