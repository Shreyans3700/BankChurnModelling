import os
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.logger.logging import logger
from src.exception.exception import CustomException
from src.config.data_ingestion import DataIngestionArtifacts
from src.config.data_transformation import (
    DataTransformationConfig,
    DataTransformationArtifacts,
)
from src.utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    """Handles data transformation tasks for the Bank Churn Modelling project.

    This class is responsible for transforming raw data into a format suitable for
    machine learning models. It includes methods for handling missing values, encoding
    categorical variables, and scaling features.
    """

    def __init__(
        self, ingestion_config: DataIngestionArtifacts, config: DataTransformationConfig
    ):
        """Initialize DataTransformation with necessary configurations."""
        self.raw_train_data_path = ingestion_config.TRAIN_DATA_PATH
        self.raw_test_data_path = ingestion_config.TEST_DATA_PATH
        self.target_column = config.TARGET_COLUMN
        self.data_transormation_dir = os.path.join(
            os.getcwd(), "artifacts", "transformed_data"
        )
        self.transformed_train_data_path = os.path.join(
            self.data_transormation_dir, config.TRANSFORMED_TRAIN_DATA_PATH
        )
        self.transformed_test_data_path = os.path.join(
            self.data_transormation_dir, config.TRANSFORMED_TEST_DATA_PATH
        )
        self.transformation_object_dir = os.path.join(
            os.getcwd(), config.TRANSFORMATION_OBJECT_DIR
        )
        self.target_transformation_object_path = os.path.join(
            self.transformation_object_dir, config.TRANSFORMATION_OBJECT_PATH
        )
        self.cols_to_drop = list(config.COLS_TO_DROP)   

    def read_data(self, data_path: str) -> pd.DataFrame:
        try:
            data = pd.read_csv(data_path, index_col=False)
            logger.info(f"Data read successfully from {data_path}")
            return data
        except Exception as e:
            raise CustomException(e, sys)

    def create_preprocessing_pipeline(self) -> ColumnTransformer:
        """Create a preprocessing pipeline for data transformation.

        This method defines the transformations to be applied to numerical and categorical features.

        Returns:
            ColumnTransformer: A scikit-learn ColumnTransformer object with the defined transformations.
        """
        try:
            # Define numerical and categorical columns
            numerical_cols = [
                "CreditScore",
                "Age",
                "Tenure",
                "Balance",
                "NumOfProducts",
                "EstimatedSalary",
            ]
            categorical_cols = ["Geography", "Gender"]

            pipeline = ColumnTransformer(
                [
                    ("num_pipeline", StandardScaler(), numerical_cols),
                    ("cat_pipeline", OneHotEncoder(), categorical_cols),
                ]
            )
            return pipeline
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        """Execute the data transformation process.

        Args:
            data_ingestion_artifacts (DataIngestionArtifacts): Artifacts from the data ingestion process,
                containing paths to raw, train, and test data files.
        Returns:
            DataTransformationArtifacts: Artifacts containing paths to transformed train and test data files.
        """
        try:
            logger.info("Starting data transformation process.")
            train_df = self.read_data(self.raw_train_data_path)
            train_df = train_df.drop(columns=self.cols_to_drop, errors="ignore")
            X_train = train_df.drop(columns=[self.target_column], errors="ignore")
            y_train = train_df[self.target_column]
            test_df = self.read_data(self.raw_test_data_path)
            test_df = test_df.drop(columns=self.cols_to_drop, errors="ignore")
            X_test = test_df.drop(columns=[self.target_column], errors="ignore")
            y_test = test_df[self.target_column]

            preprocessing_pipeline = self.create_preprocessing_pipeline()
            # Fit the pipeline on the training data and transform both train and test data
            X_train = preprocessing_pipeline.fit_transform(X_train)
            X_test = preprocessing_pipeline.transform(X_test)


            os.makedirs(self.data_transormation_dir, exist_ok=True)
            save_numpy_array_data(self.transformed_train_data_path, X_train, y_train)
            save_numpy_array_data(self.transformed_test_data_path, X_test, y_test)

            os.makedirs(self.transformation_object_dir, exist_ok=True)
            save_object(self.target_transformation_object_path, preprocessing_pipeline)
            logger.info("Data transformation process completed successfully.")
            return DataTransformationArtifacts(
                TRANSFORMED_TRAIN_DATA_PATH=self.transformed_train_data_path,
                TRANSFORMED_TEST_DATA_PATH=self.transformed_test_data_path,
                TARGET_TRANSFORMATION_OBJECT_PATH=self.target_transformation_object_path,
            )
        except Exception as e:
            raise CustomException(e, sys)
