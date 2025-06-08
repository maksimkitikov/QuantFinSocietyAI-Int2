import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from app.services.market_data import market_data_service
from app.services.ai import ai_service
import talib
from datetime import datetime, timedelta

st.set_page_config(
    page_title="StockAI - Advanced Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("StockAI")
symbol = st.sidebar.text_input("Symbol", value="AAPL").upper()
timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
)
period = st.sidebar.selectbox(
    "Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"]
)

# Main content
try:
    # Get market data
    stock_data = market_data_service.get_stock_data(symbol, timeframe, period)
    historical_data = market_data_service.get_historical_data(symbol, timeframe, period)
    
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2]
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=[d['date'] for d in historical_data],
            open=[d['open'] for d in historical_data],
            high=[d['high'] for d in historical_data],
            low=[d['low'] for d in historical_data],
            close=[d['close'] for d in historical_data],
            name="OHLC"
        ),
        row=1, col=1
    )

    # Volume
    fig.add_trace(
        go.Bar(
            x=[d['date'] for d in historical_data],
            y=[d['volume'] for d in historical_data],
            name="Volume"
        ),
        row=2, col=1
    )

    # Technical indicators
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # RSI
    rsi = talib.RSI(df['close'].values)
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=rsi,
            name="RSI"
        ),
        row=3, col=1
    )

    # Add horizontal lines for RSI
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    # Update layout
    fig.update_layout(
        title=f"{symbol} - {stock_data['name']}",
        yaxis_title="Price",
        yaxis2_title="Volume",
        yaxis3_title="RSI",
        xaxis_rangeslider_visible=False,
        height=800,
        template="plotly_dark"
    )

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

    # Market data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Price", f"${stock_data['price']:.2f}", f"{stock_data['change']*100:.2f}%")
    with col2:
        st.metric("Market Cap", stock_data['market_cap'])
    with col3:
        st.metric("P/E Ratio", stock_data['pe_ratio'])
    with col4:
        st.metric("Volume", f"{stock_data['volume']:,}")

    # Technical indicators
    st.subheader("Technical Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("RSI", f"{stock_data['technical_indicators']['rsi']:.2f}")
    with col2:
        st.metric("MACD", f"{stock_data['technical_indicators']['macd']:.2f}")
    with col3:
        st.metric("SMA 20", f"{stock_data['technical_indicators']['sma_20']:.2f}")
    with col4:
        st.metric("SMA 50", f"{stock_data['technical_indicators']['sma_50']:.2f}")

    # AI Insights
    st.subheader("AI Analysis")
    insights = ai_service.generate_insights(symbol, stock_data)
    st.write(insights['insights'])

    # Price prediction
    st.subheader("Price Prediction")
    prediction = ai_service.predict_price(symbol, historical_data)
    st.write(prediction['prediction'])

    # News
    st.subheader("Latest News")
    news = market_data_service.get_market_news(symbol)
    for item in news[:5]:
        with st.expander(item['title']):
            st.write(f"Source: {item['publisher']}")
            st.write(f"Published: {item['published']}")
            st.write(f"Type: {item['type']}")
            st.markdown(f"[Read more]({item['link']})")

except Exception as e:
    st.error(f"Error: {str(e)}") 