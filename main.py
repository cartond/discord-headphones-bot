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
            print(attachment.filename)
            # Will overwrite any dupes, could use GUID and pass it along.
            await attachment.save(f'attachments/{attachment.filename}') # 'attachments/{{attachment.filename}' is the PATH to where the attachmets/images will be saved. Example: home/you/Desktop/attachments/{{attachment.filename}
            print(f'[+] Attachment {attachment.filename} has been saved to directory/folder > attachments. attachments/ {attachment.filename}')

            new_file_bytes = editor.draw_headphones(f'attachments/{attachment.filename}')
            await send_img(message=message, file_bytes=new_file_bytes)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# @client.event
# async def on_message(message):
#     print('hi')
#     if message.author == client.user:
#         return
    
#     print(message)
#     print(message.content)

#     if message.attachments:
#         print('hi again')
#         for attachment in message.attachments:
#             if attachment.url.endswith(('png', 'jpg', 'jpeg', 'gif')):
#                 response = requests.get(attachment.url)
#                 with open(f'photos/{attachment.filename}', 'wb') as f:
#                     f.write(response.content)
#                 await message.channel.send(f'{attachment.filename} has been saved to the photos folder.')
#     print('bye')


client.run(TOKEN)

