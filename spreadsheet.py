import gspread
import sys

def open_worksheet(keyPath, worksheet_name, sheet_name):

    opened_worksheet = []

    try:
        service_account = gspread.service_account(filename=keyPath)

        raw_worksheet = service_account.open(worksheet_name)

        opened_worksheet = raw_worksheet.worksheet(sheet_name)

    except:
        e = sys.exc_info()[0]
        raise Exception(e)

    return opened_worksheet

def get_worksheet_values(value_range_string, worksheet):
    
    #with_forumla_option = gspread.utils.ValueRenderOption.formula

    worksheet_values = []

    try:
        # , value_render_option=with_forumla_option
        worksheet_values = worksheet.get_values(value_range_string)
    except:
        e = sys.exc_info()[0]
        raise Exception(e)

    return worksheet_values
