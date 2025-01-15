import csv
import io
from fastapi import FastAPI, File, UploadFile

from helpers.baubuddyClient import get_vehicles
from helpers.baubuddySerializer import merge_based_on_similarity, filter_data_by_column_is_not_none, setup_colors

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    content_str = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content_str), delimiter=";")
    result = [row for row in csv_reader]

    api_response = get_vehicles()
    merged_vehicles = merge_based_on_similarity(api_response, result)

    filtered = filter_data_by_column_is_not_none(merged_vehicles)
    colored = setup_colors(filtered)


    return colored
