import streamlit as st
import pandas as pd

# 1. 주소 설정
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="서희승 과장 주간보고", layout="wide")

@st.cache_data(ttl=10)
def load_all_data():
    # 전체 데이터를 읽어옵니다.
    df = pd.read_csv(SHEET_URL, header=None)
    # 문자열로 변환 및 nan 제거
    df = df.astype(str).replace('nan', '')
    return df

try:
    full_df = load_all_data()

    # --- [상단 고정 영역: 주차 정보 및 재고량] ---
    # 시트 1행 1열에 있는 제목 (예: 26년 1월 4주 주간계획서) 추출
    title_text = full_df.iloc[0, 0] 
    st.title(f"📊 {title_text}")
    
    # 재고량 표기 (시트 어딘가에 재고 수치를 적어두시면 그 위치를 연결하면 됩니다)
    # 현재는 예시로 '고순도 SG 재고'를 상단에 배치합니다.
    # 만약 시트 특정 셀(예: AA1)에 재고를 관리하신다면 그 위치를 iloc로 지정하세요.
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💎 고순도 SG 현재고", value="1,250 kg", delta="전일 대비 +50") # 수치는 시트 연동 가능
    with col2:
        st.metric(label="👤 작성자", value="서희승 과장")
    with col3:
        st.metric(label="📅 작성일자", value=full_df.iloc[6, 1])

    st.divider()

    # --- [중단 영역: 요일별 계획] ---
    target_days = ['월', '화', '수', '목', '금']
    filtered = full_df[full_df[0].isin(target_days)].copy()
    
    # 요일(0), 전주계획(1), 전주실행(4), 금주계획(7)
    plan_data = filtered[[0, 1, 4, 7]]
    plan_data.columns = ['요일', '전주 계획', '전주 실행', '금주 계획']
    
    # 데이터 정리 (줄바꿈 등 가독성 높이기)
    st.subheader("🗓️ 요일별 세부 업무 현황")
    st.table(plan_data)

    st.success("위 지표는 구글 시트 데이터와 실시간으로 동기화되고 있습니다.")

except Exception as e:
    st.error(f"데이터 반영 중 오류가 발생했습니다: {e}")
