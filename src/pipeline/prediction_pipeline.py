import sys
import numpy as np
import pandas as pd
from src.logger.logging import logging
from src.exception.exception import CustomException


class PredictionPipeline:
    def __init__(self, model: object, transformation_object: object):
        """
        Initialize the Prediction Pipeline with pre-loaded models.

        Args:
            model: The trained prediction model
            transformation_object: The data transformation object

        Raises:
            CustomException: If models are None
        """
        try:
            if model is None or transformation_object is None:
                raise ValueError("Model and transformation object cannot be None")
            self.model = model
            self.transformation_object = transformation_object
            logging.info(
                "PredictionPipeline initialized successfully with loaded models"
            )
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, features: pd.DataFrame):
        """
        Make a prediction using the loaded model and transformation object.

        Args:
            features: DataFrame of input features for prediction

        Returns:
            dict: Prediction class (0 or 1) and probability
        """
        try:
            logging.info("Starting prediction...")
            # Apply transformation to features
            transformed_features = self.transformation_object.transform(features)

            # Make prediction (returns probabilities)
            predictions = self.model.predict(transformed_features)

            logging.info(f"Raw predictions: {predictions}")

            # Extract probability and prediction class
            # For binary classification with sigmoid activation
            if isinstance(predictions, np.ndarray):
                # If output is 2D array (batch predictions), take first sample
                if len(predictions.shape) > 1:
                    probability = (
                        float(predictions[0][0])
                        if predictions.shape[1] == 1
                        else float(predictions[0].max())
                    )
                    # Apply threshold at 0.5 for binary classification
                    prediction_class = 1 if probability >= 0.5 else 0
                else:
                    probability = float(predictions[0])
                    prediction_class = 1 if probability >= 0.5 else 0
            else:
                probability = float(predictions)
                prediction_class = 1 if probability >= 0.5 else 0

            logging.info(
                f"Prediction class: {prediction_class}, Probability: {probability}"
            )

            return {"prediction": prediction_class, "probability": probability}
        except Exception as e:
            logging.error(f"Error during prediction: {str(e)}")
            raise CustomException(e, sys)
