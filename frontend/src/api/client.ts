import type { HealthResponse, PredictRequest, PredictResponse, TrainingResponse } from '../types';

const BASE = '/api';

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${BASE}/`);
  if (!res.ok) throw new Error('Server unreachable');
  return res.json();
}

export async function trainModel(): Promise<TrainingResponse> {
  const res = await fetch(`${BASE}/train`, { method: 'POST' });
  return res.json();
}

export async function predict(data: PredictRequest): Promise<PredictResponse> {
  const res = await fetch(`${BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}
