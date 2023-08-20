import os 
import discord
import responses
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands
# Custom 
import ss 

# Bot Token 
TOKEN = os.environ.get('TOKEN')

# Other Variables
key_path = os.environ.get('KEYPATH')
worksheet_name = os.environ.get('WORKSHEET')
sheet_name = os.environ.get('SHEET')
channel1 = int(os.environ.get('CHANNEL1'))
channel2 = int(os.environ.get('CHANNEL2'))
channel3 = int(os.environ.get('CHANNEL3'))

# Auxiliaries

async def send_message(msg, user_msg, is_private):

    try:
        response = responses.handle_response(user_msg)
        
        if(is_private):
            await msg.author.send(response) 
        
        else: 
            await msg.channel.send(response)
    
    except Exception as e: 
        print(e)

async def send_to_channel(channel_num, message, bot):
    ch = bot.get_channel(channel_num)
    await ch.send(message)

## Spreadsheet stuff
def format_item(item):

    # Note: This is too trusting. Need to come up with a better way to get specific items 
    # from item array....
    formated_item = {
        "DATE" : date.today(),
        "IMAGE" : item[2],
        "NAME" : item[3],
        "ASIN" : item[4],
        "AMZLINK" : item[5],
        "LINK": item[6],
        "COST" : item[7],
        "SALEPRICE": item[8],
        "PROFIT" : item[9],
        "ROI" : item[10]
    }

    return formated_item
         
def format_sheet_data(sheet_data):
    
    result = None

    if(len(sheet_data) > 1):
        
        payload = map(format_item, sheet_data)
        result = list(payload)
    else:
        result = False

    return result 


def write_message(item):
    msg1 = f'[{item["NAME"]}]({item["AMZLINK"]})'
    msg2 = f'\n**Buy Here:**\n[View Product]({item["LINK"]})'
    msg3 = f'\n**ASIN:**\n{item["ASIN"]}'
    msg4 = f'\n**Cost:**\n{item["COST"]}'
    msg5 = f'\n**Sale Price:**\n{item["SALEPRICE"]}'
    msg6 = f'\n**Profit|ROI:**\n{item["PROFIT"]}|${item["ROI"]}'

    return msg1 + msg2 + msg3 + msg4 + msg5 + msg6


## Main Functions

async def send_spreadsheet_data(bot):

    # Get spreadsheet values
    spread_sheet_raw = ss.open_worksheet(key_path, worksheet_name, sheet_name)
    # Get raw spreadsheet values | Note: val should be generated... not hard coded
    spread_sheet_vals = ss.get_worksheet_values("A5:K7", spread_sheet_raw)
    # Get formatted values
    formatted_values = format_sheet_data(spread_sheet_vals)
    # Once you have your values, send messages based on count...
    count = 0

    for formattedItem in formatted_values:

        message = write_message(formattedItem)
        
        channel_number = channel1

        if(count == 1):
            channel_number = channel2
        elif(count > 1):
            channel_number = channel3

        await send_to_channel(channel_number, message, bot)

        count += 1
    
    print("OK| Messages Sent!")


def run_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Andromeda is running...')
        print('------')
        print('Attempting to send messages.....')
        await send_spreadsheet_data(bot)

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


    # ctx = context
    # @bot.command()
    # async def ping(ctx):
    #     # It's an interger
    #     channel = bot.get_channel(1141489875124752524)
    #     await channel.send('Hello Channel!')


    bot.run(TOKEN)

