interface HeaderProps {
  serverOnline: boolean;
  modelReady: boolean;
}

export default function Header({ serverOnline, modelReady }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Bank Churn Predictor</h1>
        <p className="text-sm text-gray-500 mt-0.5">Neural network-based customer churn analysis</p>
      </div>
      <div className="flex items-center gap-3">
        <span
          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
            serverOnline
              ? 'bg-blue-50 text-blue-700'
              : 'bg-red-50 text-red-700'
          }`}
        >
          <span
            className={`w-2 h-2 rounded-full ${serverOnline ? 'bg-blue-500' : 'bg-red-500'}`}
          />
          {serverOnline ? 'API Online' : 'API Offline'}
        </span>
        <span
          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
            modelReady
              ? 'bg-green-50 text-green-700'
              : 'bg-yellow-50 text-yellow-700'
          }`}
        >
          <span
            className={`w-2 h-2 rounded-full ${modelReady ? 'bg-green-500' : 'bg-yellow-500'}`}
          />
          {modelReady ? 'Model Ready' : 'Model Not Trained'}
        </span>
      </div>
    </header>
  );
}
