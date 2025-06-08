import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StockChart = ({ symbol }) => {
  const [historicalData, setHistoricalData] = useState([]);
  const [technicalIndicators, setTechnicalIndicators] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [stockData, historicalData] = await Promise.all([
          axios.get(`/api/v1/market/stocks/${symbol}`),
          axios.get(`/api/v1/market/stocks/${symbol}/data`)
        ]);

        setHistoricalData(historicalData.data);
        setTechnicalIndicators(stockData.data.technical_indicators);
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
  if (!historicalData.length) return <div>Нет данных</div>;

  const chartData = {
    labels: historicalData.map(d => d.date),
    datasets: [
      {
        label: 'Цена закрытия',
        data: historicalData.map(d => d.close),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'SMA 20',
        data: historicalData.map(d => d.sma_20),
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
      {
        label: 'SMA 50',
        data: historicalData.map(d => d.sma_50),
        borderColor: 'rgb(54, 162, 235)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${symbol} - График цены`,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-lg">
      <div className="mb-4">
        <h2 className="text-2xl font-bold mb-2">Технические индикаторы</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">RSI</p>
            <p className="text-lg font-semibold">{technicalIndicators.rsi?.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">MACD</p>
            <p className="text-lg font-semibold">{technicalIndicators.macd?.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">Bollinger Upper</p>
            <p className="text-lg font-semibold">{technicalIndicators.bollinger_upper?.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">Bollinger Lower</p>
            <p className="text-lg font-semibold">{technicalIndicators.bollinger_lower?.toFixed(2)}</p>
          </div>
        </div>
      </div>
      <div className="h-96">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default StockChart; 