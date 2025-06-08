import os
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from openai import OpenAI
from app.core.config import settings
import openai
from datetime import datetime, timedelta
import json

# Инициализация моделей
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4-turbo-preview"

    async def analyze_sentiment(self, text: str) -> Dict:
        """Анализ тональности текста"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Вы - эксперт по анализу финансовых новостей. Проанализируйте тональность текста и определите его влияние на рынок."},
                    {"role": "user", "content": f"Проанализируйте следующий текст и определите его тональность (позитивная/негативная/нейтральная) и влияние на рынок (сильное/среднее/слабое):\n\n{text}"}
                ]
            )
            
            analysis = response.choices[0].message.content
            return {
                "text": text,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Ошибка при анализе тональности: {str(e)}")

    async def predict_price(self, symbol: str, historical_data: List[Dict]) -> Dict:
        """Прогноз цены акции"""
        try:
            # Подготовка данных для анализа
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # Расчет технических индикаторов
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['sma_50'] = df['close'].rolling(window=50).mean()
            df['rsi'] = self._calculate_rsi(df['close'])
            
            # Формируем контекст для GPT
            context = f"""
            Символ акции: {symbol}
            Текущая цена: {df['close'].iloc[-1]}
            Изменение за день: {df['close'].pct_change().iloc[-1] * 100:.2f}%
            SMA 20: {df['sma_20'].iloc[-1]:.2f}
            SMA 50: {df['sma_50'].iloc[-1]:.2f}
            RSI: {df['rsi'].iloc[-1]:.2f}
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Вы - эксперт по техническому анализу и прогнозированию цен на акции. Проанализируйте данные и сделайте прогноз."},
                    {"role": "user", "content": f"На основе следующих данных сделайте прогноз движения цены акции на ближайшие 5 дней:\n\n{context}"}
                ]
            )
            
            prediction = response.choices[0].message.content
            return {
                "symbol": symbol,
                "current_price": df['close'].iloc[-1],
                "prediction": prediction,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Ошибка при прогнозировании цены: {str(e)}")

    async def generate_insights(self, symbol: str, market_data: Dict) -> Dict:
        """Генерация AI-инсайтов"""
        try:
            context = f"""
            Символ акции: {symbol}
            Название: {market_data.get('name', '')}
            Сектор: {market_data.get('sector', '')}
            Индустрия: {market_data.get('industry', '')}
            Текущая цена: {market_data.get('price', '')}
            Изменение: {market_data.get('change', '')}
            Объем: {market_data.get('volume', '')}
            Рыночная капитализация: {market_data.get('market_cap', '')}
            P/E: {market_data.get('pe_ratio', '')}
            EPS: {market_data.get('eps', '')}
            Дивидендная доходность: {market_data.get('dividend_yield', '')}
            Бета: {market_data.get('beta', '')}
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Вы - финансовый аналитик. Проанализируйте данные компании и предоставьте краткие инсайты."},
                    {"role": "user", "content": f"На основе следующих данных предоставьте краткий анализ компании и рекомендации:\n\n{context}"}
                ]
            )
            
            insights = response.choices[0].message.content
            return {
                "symbol": symbol,
                "insights": insights,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Ошибка при генерации инсайтов: {str(e)}")

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Расчет RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

ai_service = AIService()

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Анализ тональности текста с помощью FinBERT
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)
    
    return {
        "positive": float(scores[0][0]),
        "negative": float(scores[0][1]),
        "neutral": float(scores[0][2])
    }

def get_ai_insights(symbol: str, data: pd.DataFrame) -> Dict[str, Any]:
    """
    Получение AI-инсайтов с помощью GPT
    """
    # Подготовка данных для GPT
    price_data = data.tail(30).to_dict('records')
    current_price = price_data[-1]['close']
    price_change = ((current_price - price_data[0]['close']) / price_data[0]['close']) * 100
    
    prompt = f"""
    Analyze the following stock data for {symbol}:
    Current price: ${current_price:.2f}
    30-day price change: {price_change:.2f}%
    
    Provide:
    1. Brief market analysis
    2. Key technical indicators interpretation
    3. Short-term price prediction
    4. Investment recommendation
    
    Keep the response concise and professional.
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional stock market analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "current_price": current_price,
        "price_change": price_change
    }

def predict_price(data: pd.DataFrame, days: int = 7) -> List[Dict[str, Any]]:
    """
    Прогнозирование цены с помощью технического анализа
    """
    # Расчет технических индикаторов
    data['SMA20'] = data['close'].rolling(window=20).mean()
    data['SMA50'] = data['close'].rolling(window=50).mean()
    
    # Расчет RSI
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Расчет MACD
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    # Прогноз на основе технических индикаторов
    last_price = data['close'].iloc[-1]
    last_sma20 = data['SMA20'].iloc[-1]
    last_sma50 = data['SMA50'].iloc[-1]
    last_rsi = data['RSI'].iloc[-1]
    last_macd = data['MACD'].iloc[-1]
    
    # Генерация прогноза
    predictions = []
    current_price = last_price
    
    for i in range(days):
        # Простая модель на основе технических индикаторов
        if last_rsi > 70:  # Перекупленность
            change = -0.01
        elif last_rsi < 30:  # Перепроданность
            change = 0.01
        else:
            change = np.random.normal(0, 0.005)
        
        if last_macd > 0:  # Восходящий тренд
            change += 0.002
        else:  # Нисходящий тренд
            change -= 0.002
        
        current_price *= (1 + change)
        predictions.append({
            "date": (pd.Timestamp.now() + pd.Timedelta(days=i+1)).isoformat(),
            "price": round(current_price, 2)
        })
    
    return predictions 