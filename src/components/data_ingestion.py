"""Data ingestion component for the Bank Churn Modelling project.

This module handles fetching data from MongoDB, splitting it into train and test sets,
and saving the data to CSV files.
"""

import os
import sys
import pandas as pd
from src.logger.logging import logging
from src.utils.utils import get_mongodb_client
from src.exception.exception import CustomException
from src.config.data_ingestion import DataIngestionConfig, DataIngestionArtifacts
from sklearn.model_selection import train_test_split


class DataIngestion:
    """Handles data ingestion from MongoDB and train-test splitting.
    
    This class manages the complete data ingestion pipeline including:
    - Connecting to MongoDB
    - Fetching data from a specified collection
    - Splitting data into train and test sets
    - Saving data to CSV files for downstream processing
    """
    def __init__(self, config: DataIngestionConfig):
        """Initialize DataIngestion with configuration.
        
        Args:
            config (DataIngestionConfig): Configuration object containing MongoDB credentials,
                database/collection names, and file paths.
                
        Raises:
            CustomException: If initialization fails.
        """
        try:
            self.mongodb_url = config.MONGODB_URL
            self.data_artifact_dir = os.path.join(os.getcwd(), "artifacts", "raw_data")
            self.raw_data_path = os.path.join(
                self.data_artifact_dir, config.RAW_DATA_PATH
            )
            self.train_data_path = os.path.join(
                self.data_artifact_dir, config.TRAIN_DATA_PATH
            )
            self.test_data_path = os.path.join(
                self.data_artifact_dir, config.TEST_DATA_PATH
            )
            self.mongodb_client = get_mongodb_client(self.mongodb_url)
            self.database = self.mongodb_client[config.MONGODB_DATABASE]
            self.collection = self.database[config.MONGODB_COLLECTION]
            self.train_test_split_ratio = config.TRAIN_TEST_SPLIT_RATIO
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """Execute the data ingestion pipeline.
        
        Fetches data from MongoDB, performs train-test split, and saves data to CSV files.
        
        Returns:
            DataIngestionArtifacts: Object containing paths to raw, train, and test data files.
            
        Raises:
            CustomException: If data ingestion fails at any stage.
        """
        try:
            logging.info("Starting data ingestion process.")
            raw_df = pd.DataFrame(list(self.collection.find()))
            raw_df = raw_df.drop(columns=["_id"], errors="ignore")
            logging.info(f"Data fetched from MongoDB with shape: {raw_df.shape}")
            train_df, test_df = train_test_split(
                raw_df, test_size=self.train_test_split_ratio, random_state=42
            )
            logging.info(
                f"Train data shape: {train_df.shape}, Test data shape: {test_df.shape}"
            )
            os.makedirs(self.data_artifact_dir, exist_ok=True)
            logging.info(f"Saving raw data to {self.raw_data_path}")
            raw_df.to_csv(self.raw_data_path, index=False)
            logging.info(f"Saving train data to {self.train_data_path}")
            train_df.to_csv(self.train_data_path, index=False)
            logging.info(f"Saving test data to {self.test_data_path}")
            test_df.to_csv(self.test_data_path, index=False)
            logging.info("Data ingestion process completed successfully.")
            return DataIngestionArtifacts(
                RAW_DATA_PATH=self.raw_data_path,
                TRAIN_DATA_PATH=self.train_data_path,
                TEST_DATA_PATH=self.test_data_path,
            )
        except Exception as e:
            raise CustomException(e, sys)
