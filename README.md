# 주식 가치 분석 시각화 앱

200주 이동평균선을 기준으로 주식의 가치 구간을 분석하고 시각화하는 앱입니다.

## 기능

- 주별 종가 기준 차트 표시
- 200주 이동평균선(200W MA) 표시 (흰색)
- Y축 로그 스케일 적용
- 가치 구간별 색상 표시:
  - **매우 저렴 (Very Cheap)**: 파란색 - 200W MA 미만
  - **저렴 (Cheap)**: 초록색 - 200W MA 이상 50% extension 미만
  - **적정가치 (Fair Value)**: 노란색 - 50% extension 이상 100% extension 미만
  - **비싼편 (Expensive)**: 주황색 - 100% extension 이상 150% extension 미만
  - **매우 비쌈 (Very Expensive)**: 빨간색 - 150% extension 이상

## 설치 및 실행

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 앱 실행:
```bash
streamlit run main.py
```

3. 브라우저에서 앱이 자동으로 열립니다.

## 사용법

1. 주식 티커를 입력하세요 (예: AAPL, GOOGL, TSLA)
2. 차트가 자동으로 생성되어 표시됩니다.
3. 현재 주가, 200주 이동평균, 가치 구간 정보를 확인할 수 있습니다.

## 파일 구조

- `main.py`: Streamlit 웹 앱 메인 파일
- `stock_analyzer.py`: 주식 데이터 분석 클래스
- `chart_visualizer.py`: 차트 시각화 클래스
- `requirements.txt`: 필요한 Python 패키지 목록