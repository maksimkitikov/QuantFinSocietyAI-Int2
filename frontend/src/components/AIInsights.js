import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AIInsights = ({ symbol }) => {
  const [insights, setInsights] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [insightsResponse, predictionResponse] = await Promise.all([
          axios.post(`/api/v1/market/insights/${symbol}`),
          axios.post(`/api/v1/market/predict/${symbol}`)
        ]);

        setInsights(insightsResponse.data);
        setPrediction(predictionResponse.data);
        setError(null);
      } catch (err) {
        setError('Ошибка при загрузке данных');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (symbol) {
      fetchData();
    }
  }, [symbol]);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>{error}</div>;
  if (!insights || !prediction) return <div>Нет данных</div>;

  return (
    <div className="p-4 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-4">AI-инсайты</h2>
        <div className="prose max-w-none">
          <p className="text-gray-700">{insights.insights}</p>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">Прогноз цены</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">Текущая цена</p>
            <p className="text-xl font-semibold">${prediction.current_price.toFixed(2)}</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">Прогноз</p>
            <p className="text-xl font-semibold">{prediction.prediction}</p>
          </div>
        </div>
      </div>

      <div className="mt-6 text-sm text-gray-500">
        <p>Последнее обновление: {new Date(prediction.timestamp).toLocaleString()}</p>
      </div>
    </div>
  );
};

export default AIInsights; 