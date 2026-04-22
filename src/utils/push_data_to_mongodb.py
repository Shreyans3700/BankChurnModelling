"""Data extraction and MongoDB upload utilities.

This module provides utilities for converting CSV data to JSON format and
pushing the data to MongoDB collections.
"""

import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from src.exception.exception import CustomException
from src.logger.logging import logging

load_dotenv()

mongoodb_url = os.getenv("MONGODB_URL_KEY")
ca = certifi.where()


class NetworkDataExtractor:
    """Extract and push network/data records to MongoDB.
    
    This class handles conversion of CSV data to JSON and uploading to MongoDB
    databases and collections.
    """
    def __init__(self, database, collection):
        """Initialize the data extractor with database and collection info.
        
        Args:
            database (str): Name of the MongoDB database.
            collection (str): Name of the MongoDB collection.
            
        Raises:
            CustomException: If MongoDB connection fails.
        """
        try:
            self.database = database
            self.collection = collection
            self.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)
        except Exception as e:
            raise CustomException(e, sys)

    def csv_to_json_converter(self, csv_file_path: str):
        """Convert CSV file to JSON format.
        
        Args:
            csv_file_path (str): Path to the input CSV file.
            
        Returns:
            list: List of dictionaries representing JSON records.
            
        Raises:
            CustomException: If CSV conversion fails.
        """
        try:
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())

            return records

        except Exception as e:
            raise CustomException(e, sys)

    def push_data_to_mongodb(self, data: list):
        """Push data records to MongoDB collection.
        
        Args:
            data (list): List of dictionaries to insert into MongoDB.
            
        Returns:
            bool: True if insertion was successful, False otherwise.
            
        Raises:
            CustomException: If MongoDB insertion fails.
        """
        try:
            db = self.client[self.database]
            collection = db[self.collection]
            collection.insert_many(data)

            return True
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    FILE_PATH = os.path.join("Churn_Modelling.csv")
    DATABASE = "Churn_Modelling_DB"
    COLLECTION = "ChurnData"

    network_obj = NetworkDataExtractor(database=DATABASE, collection=COLLECTION)
    data = network_obj.csv_to_json_converter(csv_file_path=FILE_PATH)
    status = network_obj.push_data_to_mongodb(data=data)
    if status:
        logging.info("Data pushed to MongoDB successfully.")
    else:
        logging.error("Failed to push data to MongoDB.")
