## database related functions
def error_query(error, time):
    query = f'INSERT INTO error_log (error, eventTime) VALUES (\'{error}\', \'{time}\');'

    return query 

def get_row_counts_query():

    query = 'SELECT row_start, row_end FROM spreadsheet_cursor;'

    return query

def update_row_counts_query(row_start, row_end, time):

    new_start = row_start + 4 
    new_end = row_end + 4
    
    query = f'UPDATE spreadsheet_cursor SET row_start = {new_start}, row_end = {new_end}, modified = \'{time}\' WHERE id = 1;'

    return query 

## Spreadsheet stuff
def format_item(item, columns):

    # Data examples:
    # columns = { "0" : "IMAGEURL", "1" : "AMAZONURL", "PRODUCTNAME" : 2, ....}
    # item = ["https://whatever.foobar", "amazonurl", "productname"]

    formatted_item = {}

    count = 0

    for value in item:
        current_column = columns[f'{count}']

        if("NAME" in current_column):
            formatted_item["TITLE"] = value
        elif("AMAZONURL" in current_column):
            formatted_item["AMZLINK"] = value 
        elif("IMAGE" in current_column):
            formatted_item["THUMBNAIL"] = value
        else: 
            formatted_item[current_column] = value 

        count += 1

    return formatted_item

def get_column_order(columns):
    column_count = 0
    column_order = {}

    for val in columns[0]:
        column_order[f'{column_count}'] = val.replace(" ", "").upper()
        column_count += 1

    return column_order

def format_sheet_data(sheet_data, columns):
    
    result = []

    if(len(sheet_data) > 1):

        for item in sheet_data:
            formatted_item = format_item(item, columns)
            result.append(formatted_item)

    else:
        result = False

    return result 

## generic message function

# async def send_message(msg, user_msg, is_private):

#     try:
#         response = responses.handle_response(user_msg)
        
#         if(is_private):
#             await msg.author.send(response) 
        
#         else: 
#             await msg.channel.send(response)
    
#     except Exception as e: 
#         print(e)
