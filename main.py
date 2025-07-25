import streamlit as st
import matplotlib.pyplot as plt
from stock_analyzer import StockAnalyzer
from chart_visualizer import ChartVisualizer
import pandas as pd

st.set_page_config(page_title="주식 시각화 앱", page_icon="📈", layout="wide")

# CSS로 통일된 폰트 설정 (크로스 플랫폼)
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans CJK KR', sans-serif !important;
    }
    .stMetric-value {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans CJK KR', sans-serif !important;
    }
    .stMarkdown {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans CJK KR', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📈 Stock Value Analysis Visualization")
    st.markdown("Enter a stock ticker to see a value analysis chart based on the 200-week moving average.")
    
    # 인기 티커 목록
    popular_tickers = [
        "AAPL - Apple Inc.",
        "MSFT - Microsoft Corporation", 
        "GOOGL - Alphabet Inc.",
        "AMZN - Amazon.com Inc.",
        "TSLA - Tesla Inc.",
        "NVDA - NVIDIA Corporation",
        "META - Meta Platforms Inc.",
        "NFLX - Netflix Inc.",
        "BTC-USD - Bitcoin USD",
        "ETH-USD - Ethereum USD",
        "GLD - SPDR Gold Trust",
        "SPY - SPDR S&P 500 ETF",
        "QQQ - Invesco QQQ Trust"
    ]
    
    # 드롭다운과 텍스트 입력 조합
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Enter Stock Ticker", 
            value="", 
            placeholder="e.g., AAPL, BTC-USD"
        )
    
    with col2:
        selected_ticker = st.selectbox(
            "Or Select Popular Stock",
            [""] + popular_tickers,
            index=0
        )
    
    # Use selected ticker if available
    if selected_ticker:
        ticker_input = selected_ticker.split(" - ")[0]
    
    if ticker_input:
        try:
            with st.spinner(f'Loading {ticker_input} data...'):
                analyzer = StockAnalyzer(ticker_input)
                data = analyzer.get_weekly_data()
                ma_200w = analyzer.calculate_200w_ma(data)
                
                current_price = data['Close'].iloc[-1]
                zones, latest_ma = analyzer.calculate_price_zones(current_price, ma_200w)
                current_zone = analyzer.get_current_zone(current_price, zones)
                
                visualizer = ChartVisualizer()
                fig = visualizer.create_chart(data, ma_200w, zones, current_zone, ticker_input.upper())
                
                st.pyplot(fig)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Price", f"${current_price:.2f}")
                
                with col2:
                    st.metric("200W Moving Average", f"${latest_ma:.2f}")
                
                with col3:
                    zone_english = visualizer._get_zone_english(current_zone)
                    st.metric("Current Value Zone", zone_english)
                
                with st.expander("Price Ranges by Zone"):
                    zone_order = ['very_expensive', 'expensive', 'fair_value', 'cheap', 'very_cheap']
                    for zone_name in zone_order:
                        lower, upper = zones[zone_name]
                        zone_en = visualizer._get_zone_english(zone_name)
                        if upper == float('inf'):
                            st.write(f"**{zone_en}**: {lower:.2f} and above")
                        else:
                            st.write(f"**{zone_en}**: {lower:.2f} - {upper:.2f}")
        
        except ValueError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()