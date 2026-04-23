import type { PredictResponse } from '../types';

interface ResultCardProps {
  result: PredictResponse;
}

export default function ResultCard({ result }: ResultCardProps) {
  const willChurn = result.prediction === 1;
  const probability = result.probability ?? 0;
  const pct = Math.round(probability * 100);

  return (
    <div className={`rounded-xl border-2 p-6 shadow-sm ${willChurn ? 'border-red-300 bg-red-50' : 'border-green-300 bg-green-50'}`}>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Prediction Result</h2>

      <div className="flex items-center gap-4 mb-6">
        <span
          className={`text-3xl font-extrabold ${willChurn ? 'text-red-700' : 'text-green-700'}`}
        >
          {willChurn ? 'Will Churn' : 'Will Stay'}
        </span>
        <span
          className={`px-3 py-1 rounded-full text-sm font-bold ${
            willChurn ? 'bg-red-200 text-red-800' : 'bg-green-200 text-green-800'
          }`}
        >
          {willChurn ? 'High Risk' : 'Low Risk'}
        </span>
      </div>

      <div>
        <div className="flex justify-between text-sm font-medium text-gray-700 mb-1.5">
          <span>Churn Probability</span>
          <span>{pct}%</span>
        </div>
        <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              pct >= 60 ? 'bg-red-500' : pct >= 40 ? 'bg-yellow-500' : 'bg-green-500'
            }`}
            style={{ width: `${pct}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>0% (Safe)</span>
          <span>50% (Threshold)</span>
          <span>100% (Certain)</span>
        </div>
      </div>

      <p className="mt-4 text-xs text-gray-500">
        The model predicts a <strong>{pct}%</strong> probability that this customer will leave the bank.
        {willChurn
          ? ' Consider retention actions for this customer.'
          : ' This customer is likely to remain.'}
      </p>
    </div>
  );
}
