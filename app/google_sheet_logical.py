import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from config import Config


# Log in and get service - an instance of API access
def get_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        Config.CREDENTIALS_FILE, Config.GOOGLE_API
    )
    httpAuth = credentials.authorize(httplib2.Http())
    return apiclient.discovery.build("sheets", "v4", http=httpAuth)


def take_data_from_google_sheet(range, majorDimension="ROWS"):
    values = (
        get_service()
        .spreadsheets()
        .values()
        .get(
            spreadsheetId=Config.SPREADSHEET_ID,
            range=range,
            majorDimension=majorDimension,
        )
        .execute()
    )
    return values


def data_from_ops():
    values = take_data_from_google_sheet("'Ops'!A12:C")
    return values["values"]


def data_from_first_choice():
    total_units = take_data_from_google_sheet("'FirstChoice_Data'!T2:T")
    sku = take_data_from_google_sheet("'FirstChoice_Data'!P2:P")
    values = [
        [sku, total_units]
        for sku, total_units in zip(sku["values"], total_units["values"])
    ]
    return values


def data_from_podata_time():
    total_quantity = take_data_from_google_sheet("'PODATA_TIME'!J6:J")
    mid_sku = take_data_from_google_sheet("'PODATA_TIME'!S6:S")
    destination = take_data_from_google_sheet("'PODATA_TIME'!W6:W")
    origin = take_data_from_google_sheet("'PODATA_TIME'!X6:X")
    values = [
        [total_quantity, mid_sku, destination, origin]
        for total_quantity, mid_sku, destination, origin in zip(
            total_quantity["values"],
            mid_sku["values"],
            destination["values"],
            origin["values"],
        )
    ]
    return values


def data_from_uncommon_data():
    sku = take_data_from_google_sheet("'Uncommon_Data'!N3:N")
    total_units = take_data_from_google_sheet("'Uncommon_Data'!S3:S")
    values = [
        [sku, total_units]
        for sku, total_units in zip(sku["values"], total_units["values"])
    ]
    return values


def data_from_southwest_data():
    sku = take_data_from_google_sheet("'Southwest_Data'!R4:R")
    total_units = take_data_from_google_sheet("'Southwest_Data'!V4:V")
    values = [
        [sku, total_units]
        for sku, total_units in zip(sku["values"], total_units["values"])
    ]
    return values
