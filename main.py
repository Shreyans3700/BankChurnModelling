"""Main entry point for the Bank Churn Modelling pipeline.

This module orchestrates the data ingestion process for the bank churn prediction system.
It initializes the data ingestion component and processes data from MongoDB.
"""

import sys
from src.logger.logging import logging
from src.exception.exception import CustomException
from src.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    try:
        logging.info("Starting the Bank Churn Modelling pipeline...")
        training_pipeline = TrainingPipeline()
        training_pipeline_artifacts = training_pipeline.run_pipeline()
        logging.info(f"Training Pipeline Artifacts: {training_pipeline_artifacts}")
        logging.info("Bank Churn Modelling pipeline completed successfully.")
        
    except Exception as e:
        raise CustomException(e, sys)
