import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
    
    def get_weekly_data(self, period="10y"):
        try:
            hist = self.stock.history(period=period, interval="1wk", auto_adjust=True, prepost=True)
            if hist.empty:
                hist = self.stock.history(period="5y", interval="1wk")
            if hist.empty:
                raise ValueError(f"No data found for ticker {self.ticker}. Please check if the ticker is correct.")
            return hist
        except Exception as e:
            raise ValueError(f"Failed to fetch data for ticker {self.ticker}: {str(e)}")
    
    def calculate_200w_ma(self, data):
        return data['Close'].rolling(window=200, min_periods=200).mean()
    
    def calculate_price_zones(self, current_price, ma_200w):
        latest_ma = ma_200w.iloc[-1]
        
        zones = {
            'very_cheap': (0, latest_ma),
            'cheap': (latest_ma, latest_ma * 1.5),
            'fair_value': (latest_ma * 1.5, latest_ma * 2.0),
            'expensive': (latest_ma * 2.0, latest_ma * 2.5),
            'very_expensive': (latest_ma * 2.5, float('inf'))
        }
        
        return zones, latest_ma
    
    def get_current_zone(self, current_price, zones):
        for zone_name, (lower, upper) in zones.items():
            if lower <= current_price < upper:
                return zone_name
        return 'very_expensive'