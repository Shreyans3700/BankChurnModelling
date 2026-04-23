import sys
from dataclasses import dataclass
from src.exception.exception import CustomException

class ModelTrainerConfig:
    """
    Class for model trainer constants.
    """
    try:
        MODEL_TRAINER_DIR_NAME: str = "models"
        MODEL_TRAINER_MODEL_FILE_NAME: str = "model.h5"
    except Exception as e:
        raise CustomException(e, sys)


@dataclass
class ModelTrainerArtifact:
    """
    Class for model trainer artifact.
    """
    try:
        MODEL_DIR_PATH: str
        MODEL_FILE_PATH: str
    except Exception as e:
        raise CustomException(e, sys)