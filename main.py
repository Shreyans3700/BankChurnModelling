"""FastAPI entry point for the Bank Churn Modelling pipeline.

This module provides a REST API interface for running the training pipeline.
The API runs on port 8080 and provides endpoints to trigger model training.
"""

import sys
import os
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.exception.exception import CustomException
from src.logger.logging import logging
from src.utils.utils import load_object

app = FastAPI(
    title="Bank Churn Modelling API",
    description="API for running the bank churn prediction model training pipeline",
    version="1.0.0",
)

# Allow frontend clients (local dev + configurable origins) to call the API.
allowed_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global objects for loaded models
prediction_model = None
transformation_model = None


class TrainingResponse(BaseModel):
    """Response model for training endpoint."""

    success: bool
    message: str
    details: dict = None


class PredictRequest(BaseModel):
    """Request model for prediction endpoint."""

    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


class PredictResponse(BaseModel):
    """Response model for prediction endpoint."""

    success: bool
    message: str
    prediction: float = None
    probability: float = None


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Bank Churn Modelling API"}


@app.post("/train", response_model=TrainingResponse, tags=["Training"])
async def train_model():
    """
    Trigger the training pipeline to train the model.

    Returns:
        TrainingResponse: Contains success status and training details.
    """
    global prediction_model, transformation_model

    try:
        logging.info("Starting training pipeline via API endpoint...")
        training_pipeline = TrainingPipeline()
        training_artifacts = training_pipeline.run_pipeline()

        logging.info("Training completed successfully")

        # Load models into global objects
        logging.info(
            f"Loading prediction model from: {training_artifacts.PREDICTION_MODEL_FILE_PATH}"
        )
        prediction_model = load_object(
            file_path=training_artifacts.PREDICTION_MODEL_FILE_PATH
        )

        logging.info(
            f"Loading transformation model from: {training_artifacts.TRANSFORMATION_MODEL_FILE_PATH}"
        )
        transformation_model = load_object(
            file_path=training_artifacts.TRANSFORMATION_MODEL_FILE_PATH
        )

        logging.info("Models loaded into global objects successfully")

        return TrainingResponse(
            success=True,
            message="Model training completed successfully and models loaded into memory",
            details={
                "prediction_model_path": training_artifacts.PREDICTION_MODEL_FILE_PATH,
                "transformation_model_path": training_artifacts.TRANSFORMATION_MODEL_FILE_PATH,
            },
        )
    except CustomException as e:
        logging.error(f"Custom exception during training: {str(e)}")
        raise CustomException(e, sys)


@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
async def predict(request: PredictRequest):
    """
    Make a prediction on whether a customer will churn.

    Args:
        request: PredictRequest containing customer features.

    Returns:
        PredictResponse: Contains prediction result and probability.
    """
    global prediction_model, transformation_model

    try:
        logging.info("Starting prediction via API endpoint...")

        # Check if models are loaded
        if prediction_model is None or transformation_model is None:
            error_msg = "Models not loaded. Please train the model first by calling /train endpoint."
            logging.error(error_msg)
            return PredictResponse(
                success=False,
                message=error_msg,
            )

        # Convert request to features list in the order expected by the model
        features = [
            request.CreditScore,
            request.Geography,
            request.Gender,
            request.Age,
            request.Tenure,
            request.Balance,
            request.NumOfProducts,
            request.HasCrCard,
            request.IsActiveMember,
            request.EstimatedSalary,
        ]

        feature_df = pd.DataFrame(
            [features],
            columns=[
                "CreditScore",
                "Geography",
                "Gender",
                "Age",
                "Tenure",
                "Balance",
                "NumOfProducts",
                "HasCrCard",
                "IsActiveMember",
                "EstimatedSalary",
            ],
        )

        # Instantiate prediction pipeline with loaded models
        prediction_pipeline = PredictionPipeline(
            model=prediction_model, transformation_object=transformation_model
        )
        prediction_result = prediction_pipeline.predict(features=feature_df)

        logging.info(f"Prediction completed successfully: {prediction_result}")

        return PredictResponse(
            success=True,
            message="Prediction completed successfully",
            prediction=prediction_result.get("prediction")
            if isinstance(prediction_result, dict)
            else prediction_result,
            probability=prediction_result.get("probability")
            if isinstance(prediction_result, dict)
            else None,
        )
    except CustomException as e:
        logging.error(f"Custom exception during prediction: {str(e)}")
        raise CustomException(e, sys)
    except Exception as e:
        logging.error(f"Unexpected error during prediction: {str(e)}")
        raise CustomException(e, sys)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
