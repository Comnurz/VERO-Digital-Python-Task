import csv
import io
from fastapi import FastAPI, File, UploadFile

from helpers.baubuddy_client import BaubuddyClient
from helpers.baubuddy_serializer import merge_based_on_similarity, filter_data_by_column_is_not_none, setup_colors

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    content_str = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content_str), delimiter=";")
    csv_result = [row for row in csv_reader]
    client = BaubuddyClient()
    api_response = client.get_vehicles()
    merged_vehicles = merge_based_on_similarity(api_response, csv_result)

    filtered = filter_data_by_column_is_not_none(merged_vehicles)
    colored = setup_colors(filtered, client)


    return colored
