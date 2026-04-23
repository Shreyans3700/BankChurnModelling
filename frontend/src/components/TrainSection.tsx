import { useState } from 'react';
import { trainModel } from '../api/client';

interface TrainSectionProps {
  onModelReady: () => void;
}

export default function TrainSection({ onModelReady }: TrainSectionProps) {
  const [isTraining, setIsTraining] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  async function handleTrain() {
    setIsTraining(true);
    setStatus(null);
    try {
      const res = await trainModel();
      if (res.success) {
        setStatus({ type: 'success', message: res.message });
        onModelReady();
      } else {
        setStatus({ type: 'error', message: res.message });
      }
    } catch {
      setStatus({ type: 'error', message: 'Training failed — is the backend running?' });
    } finally {
      setIsTraining(false);
    }
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">Train Model</h2>
          <p className="text-sm text-gray-500 mt-1">
            Fetches data from MongoDB, transforms features, and trains the neural network. This may take a few minutes.
          </p>
        </div>
        <button
          onClick={handleTrain}
          disabled={isTraining}
          className="flex-shrink-0 inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
        >
          {isTraining ? (
            <>
              <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
              </svg>
              Training…
            </>
          ) : (
            'Train Model'
          )}
        </button>
      </div>

      {status && (
        <div
          className={`mt-4 px-4 py-3 rounded-lg text-sm font-medium ${
            status.type === 'success'
              ? 'bg-green-50 text-green-800 border border-green-200'
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}
        >
          {status.message}
        </div>
      )}
    </div>
  );
}
