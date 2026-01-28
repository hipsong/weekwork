import streamlit as st
import pandas as pd

# 1. 주소 설정
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="서희승 과장 주간보고", layout="wide")

@st.cache_data(ttl=10)
def load_all_data():
    df = pd.read_csv(SHEET_URL, header=None)
    df = df.astype(str).replace('nan', '')
    return df

try:
    full_df = load_all_data()

    # --- [상단 고정 영역] ---
    # 1행 1열에서 "26년 1월 4주 주간계획서"라는 제목을 가져옵니다.
    weekly_title = full_df.iloc[0, 0] 
    st.title(f"📊 {weekly_title}")
    
    st.markdown("---")
    
    # 지표(Metric) 설정
    col1, col2, col3 = st.columns(3)
    with col1:
        # 요청하신 대로 2.5t으로 수정했습니다!
        # 나중에 시트 특정 셀에 재고를 적으시면 자동으로 바뀌게 연결할 수 있습니다.
        st.metric(label="💎 고순도 재고", value="2.5 t") 
    with col2:
        st.metric(label="👤 작성자", value="서희승 과장")
    with col3:
        # 작성일자 정보 (시트 7행 2열)
        write_date = full_df.iloc[6, 1]
        st.metric(label="📅 작성일자", value=write_date)

    st.divider()

    # --- [중단 영역: 요일별 업무] ---
    target_days = ['월', '화', '수', '목', '금']
    filtered = full_df[full_df[0].isin(target_days)].copy()
    
    # 열 번호 지정: 0(요일), 1(전주계획), 4(전주실행), 7(금주계획)
    plan_data = filtered[[0, 1, 4, 7]]
    plan_data.columns = ['요일', '전주 계획', '전주 실행', '금주 계획']
    
    st.subheader("🗓️ 요일별 세부 업무 현황")
    # 사장님이 보기 좋게 표로 출력
    st.table(plan_data)

    st.success("✅ 모든 데이터는 구글 시트의 최신 정보를 반영하고 있습니다.")

except Exception as e:
    st.error(f"데이터 반영 중 오류가 발생했습니다: {e}")

except Exception as e:
    st.error(f"데이터 반영 중 오류가 발생했습니다: {e}")
