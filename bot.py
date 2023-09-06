import os 
import discord
# Custom imports
import spreadsheet 
import datafunctions
import auxiliaries
# import specific functions
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks

# load env variables
load_dotenv()

# Bot Token & Variables
TOKEN = os.environ.get('TOKEN')
key_path = os.environ.get('KEYPATH')
worksheet_name = os.environ.get('WORKSHEET')
sheet_name = os.environ.get('SHEET')
channel1 = int(os.environ.get('CHANNEL1'))
channel2 = int(os.environ.get('CHANNEL2'))
channel3 = int(os.environ.get('CHANNEL3'))
channel4 = int(os.environ.get('CHANNEL4'))
column_start = os.environ.get('COLUMNSTART')
column_end = os.environ.get('COLUMNEND')

# database related functions
def log_error(connection, error, current_time):
    query = auxiliaries.error_query(error, current_time)
    
    datafunctions.execute_query(connection, query)

def get_row_counts(connection):
    query = auxiliaries.get_row_counts_query()

    result = datafunctions.execute_read_query(connection, query)

    return list(result[0])

def update_row_counts(connection, row_start, row_end, time):
    query = auxiliaries.update_row_counts_query(row_start, row_end, time)

    try: 
        datafunctions.execute_query(connection, query)
    except Error as e:
        raise Exception('Failed to update row_counts!')

    print(f'Updated the following rows...\nROW_START: {row_start} -> {row_start + 4}\nROW_END {row_end} -> {row_end + 4}')

# channel + embed related functions
async def send_to_channel(channel_num, message, bot):
    ch = bot.get_channel(channel_num)
    await ch.send(message)

async def assemble_embeded(channel_num, item, bot):

    # item keys 
    item_keys = item.keys()

    # Base embed
    embed = discord.Embed(
        # colour=discord.Colour.dark_magenta(),
        title=item["TITLE"],
        url=item["AMZLINK"]
    )

    # This logic should be redone in the future. A long if statement isn't ideal!
    for key in item_keys:

        if(key != "TITLE" and key != "AMZLINK" and key != "ROI" and key != "NOTE" and key !="CATEGORY"):
            if(key == "THUMBNAIL"):
                embed.set_thumbnail(url=item["THUMBNAIL"])
            elif(key == "SOURCEURL"):
                product_link = f'[View Product]({item["SOURCEURL"]})'
                embed.add_field(name="Buy Here:", value=product_link, inline=False)
            elif("PROFIT" in key):
                profit_and_roi = f'{item["PROFIT"]} | {item["ROI"]}'
                embed.add_field(name="Profit | ROI", value=profit_and_roi, inline=False)
            elif("CHECK" in key):
                approval_check = f'[Check for Approval]({item[key]})'
                embed.add_field(name="Check Restrictions:", value=approval_check, inline=False)
            elif("SALESRANK" in key):
                sales_rank = f'{item[key]} in {item["CATEGORY"]}'
                embed.add_field(name="Sales Rank:", value=sales_rank, inline=False)
            elif("KEEPA" in key):
                embed.set_image(url=item[key])
            elif(("BACKEND" in key) and item[key] and len(item[key]) > 1):
                footer_text = f'Note: {item[key]}'
                embed.set_footer(text=footer_text)
            elif(item[key] and len(item[key]) > 1):
                name = f'{key}:'
                embed.add_field(name=name, value=item[key], inline=False)
    
    ch = bot.get_channel(channel_num)
    await ch.send(embed=embed)

## Main Functions

async def send_embedded_messages(items, bot):

    count = 0
        
    for item in items:
    
        channel_number = channel1

        if(count == 1):
            channel_number = channel2
        elif(count == 2):
            channel_number = channel3
        elif(count > 2):
            channel_number = channel4

        await assemble_embeded(channel_number, item, bot)
        
        count += 1

async def send_spreadsheet_data(bot, sql_connection):

    print('Attempting to send messages.....')

    # Get row_counts from sql...
    row_counts = get_row_counts(sql_connection)

    row_start = row_counts[0]
    row_end = row_counts[1]

    # Get spreadsheet
    spread_sheet_raw = spreadsheet.open_worksheet(key_path, worksheet_name, sheet_name)
    
    # Get column values in first row of range (based on COLUMNSTART and COLUMNEND)
    column_base_range = f'{column_start}1:{column_end}1'
    spread_sheet_columns = spreadsheet.get_worksheet_values(column_base_range, spread_sheet_raw)

    # Organize actual columns into an order...
    spread_sheet_true_columns = auxiliaries.get_column_order(spread_sheet_columns)
    
    # Get raw spreadsheet values 
    target_range = f'{column_start}{row_start}:{column_end}{row_end}'
    spread_sheet_vals = spreadsheet.get_worksheet_values(target_range, spread_sheet_raw)
    
    # Get formatted values
    formatted_values = auxiliaries.format_sheet_data(spread_sheet_vals, spread_sheet_true_columns)
    
    # Once you have your values, send messages based on count...

    if(formatted_values and len(formatted_values) >= 4):

        await send_embedded_messages(formatted_values, bot)

        # if all is good, go ahead and send everything out...            
        current_time = datetime.now()

        update_row_counts(sql_connection, row_start, row_end, current_time)
                    
        print(f'OK\n Messages sent at: {current_time}\n------')
    else: 
        print('Not enough messages to send...skipping for now until 4 entries are made...\n------')

def run_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    connection = datafunctions.create_connection('./db/database.db')

    @tasks.loop(hours=1)
    async def try_to_send_messages():
        try:
            await send_spreadsheet_data(bot, connection)
        except Exception as error:
            current_time = datetime.now()
            print(f'MESSAGE SENDING FAILED at ({current_time})\nERROR: {error}\n------')
            log_error(connection, error, current_time)

    @bot.event
    async def on_ready():
        print(f'Andromeda is running...\n------')
        try_to_send_messages.start()

    @bot.command()
    async def greeting(ctx):
        response = 'Hey!'
        await ctx.send(response)

    @bot.command()
    async def hello(ctx):
        await ctx.send('I exist to serve the will of Pontius')

    bot.run(TOKEN)

