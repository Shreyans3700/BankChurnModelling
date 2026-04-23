export interface PredictRequest {
  CreditScore: number;
  Geography: string;
  Gender: string;
  Age: number;
  Tenure: number;
  Balance: number;
  NumOfProducts: number;
  HasCrCard: number;
  IsActiveMember: number;
  EstimatedSalary: number;
}

export interface PredictResponse {
  success: boolean;
  message: string;
  prediction?: number;
  probability?: number;
}

export interface TrainingResponse {
  success: boolean;
  message: string;
  details?: Record<string, string>;
}

export interface HealthResponse {
  status: string;
  service: string;
}
