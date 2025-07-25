import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime
import matplotlib.font_manager as fm

# 한글 폰트 설정 (크로스 플랫폼)
import platform
import os

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = ['Malgun Gothic', 'sans-serif']
else:
    # Linux/Mac용 (Streamlit Cloud)
    try:
        # 폰트 캐시 재빌드
        fm._rebuild()
        # 사용 가능한 폰트 확인
        font_list = [f.name for f in fm.fontManager.ttflist]
        korean_fonts = [f for f in font_list if 'Nanum' in f or 'Gothic' in f]
        
        if korean_fonts:
            plt.rcParams['font.family'] = korean_fonts[0]
        else:
            # fallback
            plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
    except:
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
    
plt.rcParams['axes.unicode_minus'] = False

class ChartVisualizer:
    def __init__(self):
        self.colors = {
            'very_cheap': 'blue',
            'cheap': 'green', 
            'fair_value': 'yellow',
            'expensive': 'orange',
            'very_expensive': 'red'
        }
        
    def create_chart(self, data, ma_200w, zones, current_zone, ticker):
        fig, ax = plt.subplots(figsize=(14, 8))
        
        dates = data.index
        prices = data['Close']
        
        price_line = ax.plot(dates, prices, color='black', linewidth=1.5, label=f'{ticker} Price')[0]
        ma_line = ax.plot(dates, ma_200w, color='white', linewidth=2, label='200W Moving Average')[0]
        
        zone_patches = self._add_zone_backgrounds(ax, dates, zones)
        
        ax.set_yscale('log')
        ax.set_title(f'{ticker} Stock Analysis Chart (Current Zone: {self._get_zone_english(current_zone)})', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (Log Scale)', fontsize=12)
        
        # Create legend with explicit order
        handles = [price_line, ma_line] + zone_patches
        labels = [f'{ticker} Price', '200W Moving Average'] + [f'{self._get_zone_english(zone_name)} Zone' for zone_name in ['very_expensive', 'expensive', 'fair_value', 'cheap', 'very_cheap']]
        ax.legend(handles, labels, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def _add_zone_backgrounds(self, ax, dates, zones):
        x_min, x_max = ax.get_xlim() if ax.get_xlim() != (0, 1) else (0, len(dates))
        
        zone_order = ['very_expensive', 'expensive', 'fair_value', 'cheap', 'very_cheap']
        zone_patches = []
        
        for zone_name in zone_order:
            lower, upper = zones[zone_name]
            color = self.colors[zone_name]
            
            if upper == float('inf'):
                upper = max(zones['expensive'][1] * 2, lower * 2)
            
            rect = patches.Rectangle(
                (dates[0] if len(dates) > 0 else 0, lower),
                (dates[-1] - dates[0]) if len(dates) > 1 else 1,
                upper - lower,
                linewidth=0,
                edgecolor='none',
                facecolor=color,
                alpha=0.2
            )
            ax.add_patch(rect)
            zone_patches.append(rect)
        
        return zone_patches
    
    def _get_zone_korean(self, zone_name):
        zone_names = {
            'very_cheap': '매우 저렴',
            'cheap': '저렴',
            'fair_value': '적정가치',
            'expensive': '비싼편',
            'very_expensive': '매우 비쌈'
        }
        return zone_names.get(zone_name, zone_name)
    
    def _get_zone_english(self, zone_name):
        zone_names = {
            'very_cheap': 'Very Cheap',
            'cheap': 'Cheap',
            'fair_value': 'Fair Value',
            'expensive': 'Expensive',
            'very_expensive': 'Very Expensive'
        }
        return zone_names.get(zone_name, zone_name)
    
    def create_interactive_chart(self, data, ma_200w, zones, current_zone, ticker):
        fig = go.Figure()
        
        
        dates = data.index
        prices = data['Close']
        
        # 모든 주가 데이터 추가
        fig.add_trace(go.Scatter(
            x=dates, 
            y=prices, 
            mode='lines',
            name=f'{ticker} 주가',
            line=dict(color='black', width=2),
            hovertemplate='날짜: %{x}<br>가격: $%{y:.2f}<extra></extra>'
        ))
        
        # 200주 이동평균선 추가 (NaN 값도 포함해서 전체 기간 표시)
        fig.add_trace(go.Scatter(
            x=ma_200w.index, 
            y=ma_200w, 
            mode='lines',
            name='200주 이동평균선',
            line=dict(color='red', width=3),
            connectgaps=False,  # NaN 구간은 연결하지 않음
            hovertemplate='날짜: %{x}<br>200주 이동평균: $%{y:.2f}<extra></extra>'
        ))
        
        # 가격 영역 배경 추가
        self._add_plotly_zone_backgrounds(fig, dates, zones)
        
        # 레이아웃 설정 (y축 범위 제한 제거)
        fig.update_layout(
            title=f'{ticker} 주식 분석 차트 (현재 구간: {self._get_zone_korean(current_zone)})',
            xaxis_title='날짜',
            yaxis_title='가격 (로그 스케일)',
            yaxis_type="log",
            hovermode='x unified',
            height=600,
            font=dict(family="Malgun Gothic, sans-serif"),
            showlegend=True
        )
        
        # 격자 추가
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')
        
        return fig
    
    def _add_plotly_zone_backgrounds(self, fig, dates, zones):
        zone_order = ['very_expensive', 'expensive', 'fair_value', 'cheap', 'very_cheap']
        
        # 색상을 더 진하게 변경
        plotly_colors = {
            'very_cheap': 'rgba(0,0,255,0.3)',  # 파란색
            'cheap': 'rgba(0,128,0,0.3)',       # 초록색
            'fair_value': 'rgba(255,255,0,0.3)', # 노란색
            'expensive': 'rgba(255,165,0,0.3)',  # 오렌지색
            'very_expensive': 'rgba(255,0,0,0.3)' # 빨간색
        }
        
        for zone_name in zone_order:
            lower, upper = zones[zone_name]
            color = plotly_colors[zone_name]
            
            if upper == float('inf'):
                upper = max(zones['expensive'][1] * 3, lower * 3)
            
            # 배경 영역 추가
            fig.add_shape(
                type="rect",
                x0=dates[0],
                x1=dates[-1],
                y0=lower,
                y1=upper,
                fillcolor=color,
                line_width=0,
                layer="below"
            )
            
            # 범례용 더미 trace
            fig.add_trace(go.Scatter(
                x=[dates[0]], 
                y=[lower],
                mode='markers',
                marker=dict(size=12, color=color.replace('0.3', '0.7')),
                name=f'{self._get_zone_korean(zone_name)} 구간',
                showlegend=True,
                visible='legendonly'
            ))