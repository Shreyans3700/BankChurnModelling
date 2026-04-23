from dataclasses import dataclass
import sys
from src.exception.exception import CustomException

@dataclass
class TrainingPipelineArtifact:
    try:
        PREDICTION_MODEL_FILE_PATH: str
        TRANSFORMATION_MODEL_FILE_PATH: str
    except Exception as e:
        raise CustomException(e, sys)

