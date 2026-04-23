"""Main entry point for the Bank Churn Modelling pipeline.

This module orchestrates the data ingestion process for the bank churn prediction system.
It initializes the data ingestion component and processes data from MongoDB.
"""

import sys
from src.logger.logging import logging
from src.exception.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.config.data_ingestion import DataIngestionConfig
from src.components.data_transformation import DataTransformation
from src.config.data_transformation import (
    DataTransformationConfig,
)
from src.components.model_trainer import ModelTrainer
from src.config.model_trainer import ModelTrainerConfig

if __name__ == "__main__":
    try:
        data_ingestion_obj = DataIngestion(config=DataIngestionConfig())
        data_ingestion_artifacts = data_ingestion_obj.initiate_data_ingestion()
        logging.info(f"Data Ingestion Artifacts: {data_ingestion_artifacts}")
        transformation_obj = DataTransformation(
            ingestion_config=data_ingestion_artifacts, config=DataTransformationConfig()
        )
        transformation_artifacts = transformation_obj.initiate_data_transformation()
        logging.info(f"Data Transformation Artifacts: {transformation_artifacts}")
        model_trainer_obj = ModelTrainer(
            config=ModelTrainerConfig(),
            transformation_artifacts=transformation_artifacts,
        )
        model_trainer_artifacts = model_trainer_obj.initiate_model_trainer()
        logging.info(f"Model Trainer Artifacts: {model_trainer_artifacts}")
    except Exception as e:
        raise CustomException(e, sys)
