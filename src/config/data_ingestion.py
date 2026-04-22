"""Configuration classes for data ingestion pipeline.

This module defines dataclasses that encapsulate configuration parameters
for MongoDB connection and file paths used in the data ingestion process.
"""

import os
import sys
from dotenv import load_dotenv
from dataclasses import dataclass
from src.exception.exception import CustomException

load_dotenv()


@dataclass
class DataIngestionConfig:
    """Configuration for data ingestion from MongoDB.
    
    Attributes:
        MONGODB_URL (str): Connection URL for MongoDB Atlas.
        MONGODB_DATABASE (str): Name of the MongoDB database.
        MONGODB_COLLECTION (str): Name of the MongoDB collection to fetch data from.
        RAW_DATA_PATH (str): File path for saving raw data.
        TRAIN_DATA_PATH (str): File path for saving training data.
        TEST_DATA_PATH (str): File path for saving test data.
        TRAIN_TEST_SPLIT_RATIO (float): Ratio of test data (e.g., 0.25 for 25% test data).
    """
    try:
        MONGODB_URL: str = os.getenv("MONGODB_URL")
        MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE")
        MONGODB_COLLECTION: str = os.getenv("MONGODB_COLLECTION")
        RAW_DATA_PATH: str = "raw_data.csv"
        TRAIN_DATA_PATH: str = "train_data.csv"
        TEST_DATA_PATH: str = "test_data.csv"
        TRAIN_TEST_SPLIT_RATIO: float = 0.25
    except Exception as e:
        raise CustomException(e, sys)


@dataclass
class DataIngestionArtifacts:
    """Artifacts produced by the data ingestion process.
    
    Attributes:
        RAW_DATA_PATH (str): Path to the raw, unprocessed data file.
        TRAIN_DATA_PATH (str): Path to the training data file.
        TEST_DATA_PATH (str): Path to the test data file.
    """
    try:
        RAW_DATA_PATH: str
        TRAIN_DATA_PATH: str
        TEST_DATA_PATH: str
    except Exception as e:
        raise CustomException(e, sys)
