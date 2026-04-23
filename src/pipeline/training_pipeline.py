import sys
from src.config.data_ingestion import DataIngestionConfig, DataIngestionArtifacts
from src.config.data_transformation import (
    DataTransformationConfig,
    DataTransformationArtifacts,
)
from src.config.model_trainer import ModelTrainerConfig, ModelTrainerArtifact
from src.config.training_pipeline import TrainingPipelineArtifact
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception.exception import CustomException
from src.logger.logging import logging


class TrainingPipeline:
    def __init__(self):
        pass

    def start_data_ingestion(
        self, ingestion_config: DataIngestionConfig
    ) -> DataIngestionArtifacts:
        try:
            logging.info("Starting data ingestion...")
            data_ingestion = DataIngestion(config=ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifacts
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(
        self,
        data_transformation_config: DataTransformationConfig,
        data_ingestion_artifacts: DataIngestionArtifacts,
    ) -> DataTransformationArtifacts:
        try:
            logging.info("Starting data transformation...")
            data_transformation = DataTransformation(
                ingestion_config=data_ingestion_artifacts,
                config=data_transformation_config,
            )
            data_transformation_artifacts = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Data transformation completed successfully.")
            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_trainer(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifacts: DataTransformationArtifacts,
    ) -> ModelTrainerArtifact:
        try:
            logging.info("Starting model training...")
            model_trainer = ModelTrainer(
                config=model_trainer_config,
                transformation_artifacts=data_transformation_artifacts,
            )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Model training completed successfully.")
            return model_trainer_artifacts
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self) -> ModelTrainerArtifact:
        try:
            data_ingestion_config = DataIngestionConfig()
            data_ingestion_artifacts = self.start_data_ingestion(
                ingestion_config=data_ingestion_config
            )

            data_transformation_config = DataTransformationConfig()
            data_transformation_artifacts = self.start_data_transformation(
                data_transformation_config=data_transformation_config,
                data_ingestion_artifacts=data_ingestion_artifacts,
            )

            model_trainer_config = ModelTrainerConfig()
            model_trainer_artifacts = self.start_model_trainer(
                model_trainer_config=model_trainer_config,
                data_transformation_artifacts=data_transformation_artifacts,
            )
            logging.info("All stages of the pipeline completed successfully.")
            return TrainingPipelineArtifact(
                PREDICTION_MODEL_FILE_PATH=model_trainer_artifacts.MODEL_FILE_PATH,
                TRANSFORMATION_MODEL_FILE_PATH=data_transformation_artifacts.TARGET_TRANSFORMATION_OBJECT_PATH,
            )
        except Exception as e:
            raise CustomException(e, sys)
