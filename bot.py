import discord
from discord.ext import commands
import responses

# Main Token 
# This Token shouldn't live here. Please move this into a .env file
TOKEN = 'MTA1NzQ5ODI5ODQ2MzgyNjA5MQ.GFMkaf.rR0vNdKMvK-RPVcFmm8FfEyPrBYc2Qr7Onmt2U'

async def send_message(msg, user_msg, is_private):

    try:
        response = responses.handle_response(user_msg)
        
        if(is_private):
            await msg.author.send(response) 
        
        else: 
            await msg.channel.send(response)
    
    except Exception as e: 
        print(e)

def run_bot():
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():

        print(f'{client.user} is now running ')

    
    @client.event 
    async def on_message(msg):
        if msg.author == client.user: 
            return 
        
        username = str(msg.author)
        user_msg = str(msg.content)
        channel = str(msg.channel)


        print(f'User {username} said \'{user_msg}\' in {channel}')

        # if(user_msg[0] == '?'):
        #     user_message = user_msg[1:]
        #     await send_message(msg, user_message, is_private=True)
        # else:
        #     await send_message(msg, user_message, is_private=False)
        print(msg)
        print(f'USER MESSAGE: {user_msg}')
    
    # Everything must be declared before this event
    client.run(TOKEN)


def run_neo_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Andromeda is running...')
        print('------')

    @bot.command()
    async def greeting(ctx):

        print(ctx.author)

        response = ''

        if(ctx.author == 'minwoah#4946'):
            response = 'Fuck you faggot'
        else: 
            response = 'Hey!'

        await ctx.send(response)

    @bot.command()
    async def hello(ctx):
        await ctx.send('I exist to serve the will of Pontius')


    bot.run(TOKEN)

