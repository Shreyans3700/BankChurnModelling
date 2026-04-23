import { useEffect, useState } from 'react';
import { checkHealth } from './api/client';
import type { PredictResponse } from './types';
import Header from './components/Header';
import TrainSection from './components/TrainSection';
import PredictionForm from './components/PredictionForm';
import ResultCard from './components/ResultCard';

export default function App() {
  const [serverOnline, setServerOnline] = useState(false);
  const [modelReady, setModelReady] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);

  useEffect(() => {
    checkHealth()
      .then(() => setServerOnline(true))
      .catch(() => setServerOnline(false));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header serverOnline={serverOnline} modelReady={modelReady} />

      <main className="max-w-5xl mx-auto px-4 py-8 space-y-6">
        {!serverOnline && (
          <div className="px-4 py-3 rounded-lg bg-red-50 border border-red-200 text-red-800 text-sm font-medium">
            Cannot reach the backend at <code>http://localhost:8080</code>. Start it with{' '}
            <code>python main.py</code> and refresh.
          </div>
        )}

        <TrainSection onModelReady={() => setModelReady(true)} />

        <PredictionForm
          modelReady={modelReady}
          onResult={res => {
            setResult(res);
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
          }}
        />

        {result && <ResultCard result={result} />}
      </main>
    </div>
  );
}
