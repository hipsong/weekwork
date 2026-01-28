import streamlit as st
import pandas as pd

# 1. 설정 (메모해둔 시트 ID를 여기에 넣으세요)
SHEET_ID = "1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="서희승 과장 주간보고", layout="wide")

@st.cache_data(ttl=10)
def load_data():
    # 데이터 전체 로드
    df = pd.read_csv(URL, header=None).astype(str).replace('nan', '')
    return df

try:
    data = load_data()

    # 상단 요약 정보 (1~3행)
    st.title(f"🚀 {data.iloc[0, 1]}") # 제목
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💎 고순도SG 재고", f"{data.iloc[1, 1]} t") # 재고
    with col2:
        st.metric("👤 작성자", data.iloc[2, 1]) # 작성자
    with col3:
        st.metric("📅 확인 시점", pd.Timestamp.now().strftime("%Y-%m-%d"))

    st.divider()

    # 하단 표 정보 (5행부터 끝까지)
    st.subheader("📝 주간 상세 내역 (전주 계획 / 전주 실행 / 금주 계획)")
    
    # 5행을 컬럼명으로 잡고 6행부터 데이터로 취급
    plan_df = data.iloc[5:11, 0:4] # 월~금 데이터만 추출
    plan_df.columns = ["요일", "전주 계획", "전주 실행", "금주 계획"]
    
    # 표 출력
    st.table(plan_df)

    st.success("✅ 구글 시트 업데이트 시 자동으로 반영됩니다.")

except Exception as e:
    st.error(f"시트 연동 에러: {e}")
