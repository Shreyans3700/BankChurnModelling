import os
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from src.utils.utils import load_numpy_array_data, save_object
from src.exception.exception import CustomException
from src.config.data_transformation import DataTransformationArtifacts
from src.config.model_trainer import ModelTrainerArtifact, ModelTrainerConfig
from src.logger.logging import logging


class ModelTrainer:
    def __init__(
        self,
        config: ModelTrainerConfig,
        transformation_artifacts: DataTransformationArtifacts,
    ):
        try:
            self.model_dir_name = os.path.join(
                os.getcwd(), config.MODEL_TRAINER_DIR_NAME
            )
            self.model_file_name = config.MODEL_TRAINER_MODEL_FILE_NAME
            self.train_features_path = (
                transformation_artifacts.TRANSFORMED_TRAIN_DATA_PATH
            )
            self.test_features_path = (
                transformation_artifacts.TRANSFORMED_TEST_DATA_PATH
            )
        except Exception as e:
            raise CustomException(e, sys)

    def artificial_neural_network(
        self,
        hidden_layer_size: int = 64,
        epochs: int = 100,
        batch_size: int = 32,
        learning_rate: float = 0.001,
        optimizer: str = "adam",
        input_shape: int = 10,
    ) -> Sequential:
        try:
            logging.info("Artificial Neural Network training initiated.")
            model = Sequential(
                [
                    Dense(
                        hidden_layer_size,
                        activation="relu",
                        input_shape=(input_shape,),
                    ),
                    Dense(int(hidden_layer_size / 2), activation="relu"),
                    Dense(1, activation="sigmoid"),
                ]
            )

            model.compile(
                optimizer=optimizer,
                loss="binary_crossentropy",
                metrics=["accuracy"],
            )

            return model
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Model training initiated.")
            train_df = load_numpy_array_data(self.train_features_path)
            test_df = load_numpy_array_data(self.test_features_path)
            logging.info(
                "Successfully loaded training and test data for model training."
            )
            X_train, y_train = train_df
            X_test, y_test = test_df
            model = self.artificial_neural_network(
                hidden_layer_size=64,
                epochs=100,
                batch_size=32,
                learning_rate=0.001,
                optimizer="adam",
                input_shape=X_train.shape[1],
            )

            early_stopping = EarlyStopping(
                monitor="val_loss",
                patience=5,
                restore_best_weights=True,
            )

            model.fit(
                X_train,
                y_train,
                validation_data=(X_test, y_test),
                epochs=100,
                batch_size=32,
                callbacks=[early_stopping],
            )

            save_object(
                file_path=os.path.join(self.model_dir_name, self.model_file_name),
                obj=model,
            )

            return ModelTrainerArtifact(
                MODEL_DIR_PATH=self.model_dir_name,
                MODEL_FILE_PATH=os.path.join(self.model_dir_name, self.model_file_name),
            )

            logging.info(model.summary())
        except Exception as e:
            raise CustomException(e, sys)
