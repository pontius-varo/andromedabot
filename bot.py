import os 
import discord
import responses
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
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
column_start = os.environ.get('COLUMNSTART')
column_end = os.environ.get('COLUMNEND')

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

async def send_embeded_to_channel(channel_num, item, bot):
    
    # item = { "IMAGEURL" : "URL.com", "AMAZONURL" : "URL.com", "PRODUCTNAME" : "NAME"...}

    # item keys 
    item_keys = item.keys()

    # Base embed
    embed = discord.Embed(
        colour=discord.Colour.dark_magenta(),
        description=item["AMZLINK"],
        title=item["TITLE"]
    )

    # THINK ABOUT THIS!!!! MUST BE FIXED..... VVVVV

    for key in item_keys:
        if(key.find("IMAGE")):
            embed.set_thumbnail(url=item["IMAGE"])
        elif(key.find("SOURCEURL")):
            embed.add_field(name="Buy Here:", value=item[key], inline=False)
        # Should be last...
        elif(key.find("KEEPA")):
            embed.set_image(url=item[key])
        elif(key.find("BACKEND") && item[key]):
            footer_text = f'Note: {item[key]}'
            embed.set_footer(text=footer_text)
    # embed.set_thumbnail(url=item["IMAGE"])
    # # Shouldn't be repeating yourself....
    # embed.add_field(name="Buy Here:", value=product_link, inline=False)
    # embed.add_field(name="ASIN:", value=item["ASIN"], inline=False)
    # embed.add_field(name="Cost:", value=cost, inline=False)
    # embed.add_field(name="Sale Price:", value=sale_price, inline=False)
    # embed.add_field(name="Profit | ROI:", value=profit_and_roi, inline=False)


    ch = bot.get_channel(channel_num)
    await ch.send(embed=embed)



## Spreadsheet stuff
def format_item(item, columns):

    # Data examples:
    # columns = { "0" : "IMAGEURL", "1" : "AMAZONURL", "PRODUCTNAME" : 2, ....}
    # item = ["https://whatever.foobar", "amazonurl", "productname"]

    formatted_item = {}

    count = 0

    for value in item:
        current_column = columns[f'{count}']
        formatted_item[current_column] = value 
        
        if(current_column.find("NAME")):
            formatted_item["TITLE"] = value
        elif(current_column.find("AMAZON")):
            formatted_item["AMZLINK"] = value 
        else: 
            formatted_item[current_column] = value 

        count += 1


    return formated_item

def get_column_order(columns):
    column_count = 0
    column_order = {}

    for val in columns:
        column_order[f'{column_count}'] = val.replace(" ", "").uppercase()
        column_count += 1

    return column_order

def format_sheet_data(sheet_data, columns):
    
    result = []

    if(len(sheet_data) > 1):

        for item in sheet_data
            formatted_item = format_item(item, columns)
            payload.append(formatted_item)

    else:
        result = False

    return result 

## Main Functions

async def send_spreadsheet_data(bot):

    print('Attempting to send messages.....')
    # Get spreadsheet
    spread_sheet_raw = ss.open_worksheet(key_path, worksheet_name, sheet_name)
    # Get column values in first row of range (based on COLUMNSTART and COLUMNEND)
    spread_sheet_columns = ss.get_worksheet_values(f'{column_start}1:{column_end}1', spread_sheet_raw)
    # Organize actual columns into an order...
    spread_sheet_true_columns = get_column_order(spread_sheet_columns)
    
    
    
    # Get raw spreadsheet values | Note: val should be generated... not hard coded
    spread_sheet_vals = ss.get_worksheet_values(f'{column_start}x:{column_end}y', spread_sheet_raw)
    # Get formatted values
    formatted_values = format_sheet_data(spread_sheet_vals, spread_sheet_true_columns)
    # Once you have your values, send messages based on count...
    count = 0

    if(formatted_values):
        for formatted_item in formatted_values:
        
            channel_number = channel1

            if(count == 1):
                channel_number = channel2
            elif(count > 1):
                channel_number = channel3

            await send_embeded_to_channel(channel_number, formatted_item, bot)


            count += 1
    
        current_time = datetime.now()
        print(f'OK\n Messages sent at: {current_time}')
    else: 
        raise Exception('Not enough data to send. Data was less than or equal to 1.....')


def run_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    # Every hour, invoke send spreadsheet data
    @tasks.loop(hours=1)
    async def try_to_send_messages():
        try:
            await send_spreadsheet_data(bot)
        except Exception as e:
            print(f'MESSAGE SENDING FAILED {e}')


    @bot.event
    async def on_ready():
        print(f'Andromeda is running...')
        print('------')
        try_to_send_messages.start()

    @bot.command()
    async def greeting(ctx):

        print(ctx.author)

        response = 'Hey!'
        await ctx.send(response)

    @bot.command()
    async def hello(ctx):
        await ctx.send('I exist to serve the will of Pontius')


    bot.run(TOKEN)

