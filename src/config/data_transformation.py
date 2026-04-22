import sys
from dataclasses import dataclass
from src.exception.exception import CustomException


@dataclass
class DataTransformationConfig:
    """Configuration for data transformation process.

    Attributes:
        TRANSFORMED_DATA_PATH (str): File path for saving transformed data.
    """

    try:
        TRANSFORMED_TRAIN_DATA_PATH: str = "train_data.npz"
        TRANSFORMED_TEST_DATA_PATH: str = "test_data.npz"
        TARGET_COLUMN: str = "Exited"
        TRANSFORMATION_OBJECT_DIR: str = "models"
        TRANSFORMATION_OBJECT_PATH: str = "transformation_object.pkl"
        COLS_TO_DROP: tuple = ("RowNumber", "CustomerId", "Surname")
    except Exception as e:
        raise CustomException(e, sys)


@dataclass
class DataTransformationArtifacts:
    """Artifacts produced by the data transformation process.

    Attributes:
        TRANSFORMED_TRAIN_DATA_PATH (str): Path to the transformed training data file.
        TRANSFORMED_TEST_DATA_PATH (str): Path to the transformed test data file.
        TARGET_COLUMN (str): The target column name.
        TRANSFORMATION_OBJECT_PATH (str): Path to the transformation object file.
    """

    try:
        TRANSFORMED_TRAIN_DATA_PATH: str
        TRANSFORMED_TEST_DATA_PATH: str
        TARGET_TRANSFORMATION_OBJECT_PATH: str
    except Exception as e:
        raise CustomException(e, sys)
