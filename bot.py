# bot.py
import os
import discord
from dotenv import load_dotenv
import editor

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def send_img(message, file_bytes):
    discord_file = discord.File(file_bytes, filename='gamer.png')
    await message.channel.send('here it is muchacho', file=discord_file)
    # await message.channel.send(f"here it is {message.content[5:]}", file=await message.attachments[0].to_file())


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print('attachments', len(message.attachments))

    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in ['png', 'jpg', 'jpeg']):
            image_bytes = await attachment.read()
            print(f'[+] Attachment {attachment.filename} has been read into bytes')

            new_file_bytes = editor.draw_headphones(image_bytes)
            if new_file_bytes is None:
                await message.channel.send('No face found :(')
                return

            await send_img(message=message, file_bytes=new_file_bytes)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
