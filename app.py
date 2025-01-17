import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
import certifi
ca = certifi.where()
import pymongo

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from networksecurity.utils.main_utils.utils5 import load_object
from networksecurity.constants.trainining_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME

client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]

## creating interface with fast api
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='./templates')

@app.get("/",tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")

@app.get("/train")
async def train():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is completed")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile= File(...)):
    try:
        df = pd.read_csv(file.file)
        processor = load_object("final_model/processor.pkl")
        best_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(processor=processor,model=best_model)
        y_pred=network_model.predict(df)
        print(y_pred)
        df["predicted_column"] = y_pred
        df.to_csv('predicted_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
if __name__ == "__main__":
    app_run(app,host = "localhost",port = 8000)
