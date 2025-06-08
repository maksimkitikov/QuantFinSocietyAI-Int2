import React, { useState } from 'react';
import StockChart from './components/StockChart';
import AIInsights from './components/AIInsights';

function App() {
  const [symbol, setSymbol] = useState('AAPL');

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Анализ фондового рынка
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-6">
            <label htmlFor="symbol" className="block text-sm font-medium text-gray-700">
              Символ акции
            </label>
            <div className="mt-1">
              <input
                type="text"
                name="symbol"
                id="symbol"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                placeholder="Например: AAPL"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6">
            <StockChart symbol={symbol} />
            <AIInsights symbol={symbol} />
          </div>
        </div>
      </main>

      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            © 2024 Stock Market Analysis Platform. Все права защищены.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App; 