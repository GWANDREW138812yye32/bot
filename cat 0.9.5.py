import discord
import youtube_dl
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import time
import os


TOKEN = "NTAxMDcwMTQxODY2Mzc3MjM2.DqUJpQ.tr3OEo06JU0jHTeCASyCt2TI37k"
client = commands.Bot(command_prefix = '%')
client.remove_command('help')

players = {}


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Written with Atom Prefix is %'))
    print('cat working')


@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)


@client.command()
async def ping():
    await client.say('Pong!')


@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


@client.command(pass_context=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('messages were deleted')


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author


    Embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    Embed.set_author(name='Help')
    Embed.add_field(name='Help', value='%ping returns pong | %echo (message here) says what you put after %echo | %join bot joins your voice channel | %leave bot leaves your voice chnnel | %play (youtube url) plays audio of a youtube video in your voice channel | %pause pauses the sound of the video in the voice channel | %resume resumes the sound of the youtube video in your channel | %stop stops the youtube vieo sound | %clear (number) deletes a number of messages min 2 max 500 | if you want this bot here is the invite link https://discordapp.com/api/oauth2/authorize?client_id=501070141866377236&permissions=0&scope=bot ', inline=False)

    await client.send_message(author, embed=Embed)

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()






client.run(TOKEN)
