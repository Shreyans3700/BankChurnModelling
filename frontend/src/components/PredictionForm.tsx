import { useState } from 'react';
import type { PredictRequest, PredictResponse } from '../types';
import { predict } from '../api/client';

interface PredictionFormProps {
  modelReady: boolean;
  onResult: (result: PredictResponse) => void;
}

const defaultForm: PredictRequest = {
  CreditScore: 650,
  Geography: 'France',
  Gender: 'Male',
  Age: 35,
  Tenure: 5,
  Balance: 50000,
  NumOfProducts: 1,
  HasCrCard: 1,
  IsActiveMember: 1,
  EstimatedSalary: 60000,
};

export default function PredictionForm({ modelReady, onResult }: PredictionFormProps) {
  const [form, setForm] = useState<PredictRequest>(defaultForm);
  const [isPredicting, setIsPredicting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function setField<K extends keyof PredictRequest>(key: K, value: PredictRequest[K]) {
    setForm(prev => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsPredicting(true);
    setError(null);
    try {
      const res = await predict(form);
      if (res.success) {
        onResult(res);
      } else {
        setError(res.message);
      }
    } catch {
      setError('Prediction failed — is the backend running?');
    } finally {
      setIsPredicting(false);
    }
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent';
  const labelCls = 'block text-xs font-semibold text-gray-600 mb-1';

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-900 mb-5">Customer Details</h2>

      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

          <div>
            <label className={labelCls}>Credit Score</label>
            <input
              type="number" min={300} max={900} required
              value={form.CreditScore}
              onChange={e => setField('CreditScore', Number(e.target.value))}
              className={inputCls}
            />
            <p className="text-xs text-gray-400 mt-1">Range: 300 – 900</p>
          </div>

          <div>
            <label className={labelCls}>Geography</label>
            <select
              value={form.Geography}
              onChange={e => setField('Geography', e.target.value)}
              className={inputCls}
            >
              <option>France</option>
              <option>Spain</option>
              <option>Germany</option>
            </select>
          </div>

          <div>
            <label className={labelCls}>Gender</label>
            <select
              value={form.Gender}
              onChange={e => setField('Gender', e.target.value)}
              className={inputCls}
            >
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

          <div>
            <label className={labelCls}>Age</label>
            <input
              type="number" min={18} max={100} required
              value={form.Age}
              onChange={e => setField('Age', Number(e.target.value))}
              className={inputCls}
            />
            <p className="text-xs text-gray-400 mt-1">Range: 18 – 100</p>
          </div>

          <div>
            <label className={labelCls}>Tenure (years)</label>
            <input
              type="number" min={0} max={10} required
              value={form.Tenure}
              onChange={e => setField('Tenure', Number(e.target.value))}
              className={inputCls}
            />
            <p className="text-xs text-gray-400 mt-1">Years as customer (0 – 10)</p>
          </div>

          <div>
            <label className={labelCls}>Balance ($)</label>
            <input
              type="number" min={0} step="0.01" required
              value={form.Balance}
              onChange={e => setField('Balance', Number(e.target.value))}
              className={inputCls}
            />
          </div>

          <div>
            <label className={labelCls}>Number of Products</label>
            <select
              value={form.NumOfProducts}
              onChange={e => setField('NumOfProducts', Number(e.target.value))}
              className={inputCls}
            >
              {[1, 2, 3, 4].map(n => <option key={n} value={n}>{n}</option>)}
            </select>
          </div>

          <div>
            <label className={labelCls}>Estimated Salary ($)</label>
            <input
              type="number" min={0} step="0.01" required
              value={form.EstimatedSalary}
              onChange={e => setField('EstimatedSalary', Number(e.target.value))}
              className={inputCls}
            />
          </div>

          <div className="flex flex-col gap-3 justify-center">
            <label className="flex items-center gap-3 cursor-pointer">
              <button
                type="button"
                onClick={() => setField('HasCrCard', form.HasCrCard === 1 ? 0 : 1)}
                className={`relative w-10 h-6 rounded-full transition-colors ${
                  form.HasCrCard ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-transform ${
                    form.HasCrCard ? 'translate-x-5' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className="text-sm font-medium text-gray-700">Has Credit Card</span>
            </label>

            <label className="flex items-center gap-3 cursor-pointer">
              <button
                type="button"
                onClick={() => setField('IsActiveMember', form.IsActiveMember === 1 ? 0 : 1)}
                className={`relative w-10 h-6 rounded-full transition-colors ${
                  form.IsActiveMember ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-transform ${
                    form.IsActiveMember ? 'translate-x-5' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className="text-sm font-medium text-gray-700">Active Member</span>
            </label>
          </div>
        </div>

        {error && (
          <div className="mt-4 px-4 py-3 rounded-lg bg-red-50 text-red-800 border border-red-200 text-sm">
            {error}
          </div>
        )}

        <div className="mt-6">
          <button
            type="submit"
            disabled={!modelReady || isPredicting}
            title={!modelReady ? 'Train the model first' : undefined}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isPredicting ? (
              <>
                <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
                </svg>
                Predicting…
              </>
            ) : (
              'Predict Churn'
            )}
          </button>
          {!modelReady && (
            <p className="mt-2 text-xs text-gray-400">Train the model above before running predictions.</p>
          )}
        </div>
      </form>
    </div>
  );
}
