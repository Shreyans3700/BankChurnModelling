# Bank Churn Modelling

A full-stack application that predicts whether a bank customer will churn (leave the bank) using a neural network trained on customer profile data.

## Overview

- **Backend**: FastAPI REST API (port 8080)
- **Frontend**: React + Vite + TypeScript + Tailwind CSS (port 5173)
- **Model**: TensorFlow sequential neural network (binary classification)
- **Database**: MongoDB Atlas (stores the training dataset)

## Project Structure

```
BankChurnModelling/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env                             # MongoDB connection config
├── models/                          # Saved model artifacts
│   ├── model.h5                     # Trained neural network
│   └── transformation_object.pkl    # Preprocessing pipeline
├── artifacts/                       # Pipeline-generated data
│   ├── raw_data/                    # CSVs from MongoDB
│   └── transformed_data/            # Scaled/encoded NPZ files
├── src/
│   ├── components/                  # Data ingestion, transformation, training
│   ├── pipeline/                    # Training and prediction orchestration
│   ├── config/                      # Dataclass configs for each stage
│   ├── utils/                       # MongoDB client, pickle I/O helpers
│   ├── logger/                      # Rotating file logger
│   └── exception/                   # Custom exception with traceback info
└── frontend/                        # React frontend
    └── src/
        ├── api/client.ts            # Typed fetch wrappers
        ├── types.ts                 # Shared TypeScript interfaces
        └── components/             # Header, TrainSection, PredictionForm, ResultCard
```

## Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB Atlas account (connection string in `.env`)

### 1. Clone and install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
MONGODB_URL=your_mongodb_connection_string
MONGODB_DATABASE=Churn_Modelling_DB
MONGODB_COLLECTION=ChurnData
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

## Running the Application

Open two terminals:

**Terminal 1 — Backend**
```bash
python main.py
```
API will be available at `http://localhost:8080`

**Terminal 2 — Frontend**
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

## Usage

1. **Train the model** — Click "Train Model" on the dashboard. This fetches data from MongoDB, preprocesses features, and trains the neural network. This may take a few minutes.

2. **Predict churn** — Once training completes (status badge turns green), fill in the customer details form and click "Predict Churn".

3. **View results** — The result card shows whether the customer "Will Churn" or "Will Stay" along with a churn probability bar.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/train` | Trigger full training pipeline |
| `POST` | `/predict` | Predict churn for a single customer |

### Prediction Request Body

```json
{
  "CreditScore": 650,
  "Geography": "France",
  "Gender": "Male",
  "Age": 35,
  "Tenure": 5,
  "Balance": 50000.0,
  "NumOfProducts": 2,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 60000.0
}
```

### Prediction Response

```json
{
  "success": true,
  "message": "Prediction completed successfully",
  "prediction": 0,
  "probability": 0.23
}
```

`prediction`: `0` = will stay, `1` = will churn  
`probability`: churn confidence score between 0.0 and 1.0

## Model Details

**Architecture**: Sequential neural network
- Input layer → 64 neurons (ReLU) → 32 neurons (ReLU) → 1 neuron (Sigmoid)
- Optimizer: Adam | Loss: Binary Crossentropy
- Training: up to 100 epochs with early stopping (patience=5)

**Preprocessing**:
- Numerical features (CreditScore, Age, Tenure, Balance, NumOfProducts, EstimatedSalary): StandardScaler
- Categorical features (Geography, Gender): OneHotEncoder
- Dropped columns: RowNumber, CustomerId, Surname

**Dataset**: 10,000 customer records, 75/25 train/test split

## Interactive API Docs

FastAPI auto-generates docs at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
