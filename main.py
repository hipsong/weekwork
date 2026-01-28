import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="주간 업무 계획서", layout="wide")

# 구글 시트 주소 (공유 URL의 ID 부분만 교체하세요)
# 예: https://docs.google.com/spreadsheets/d/이부분이ID입니다/edit
SHEET_ID = "1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60) # 1분마다 자동 갱신
def load_data():
    # 주간계획서는 양식이 복잡하므로 스킵해야 할 행이 있을 수 있습니다.
    # 일단 전체를 불러온 뒤 정리합니다.
    df = pd.read_csv(SHEET_URL)
    return df

st.title("📅 주간 업무 계획 보고 (실시간)")
st.markdown("---")

try:
    df = load_data()

    # 상단 기본 정보 (시트의 특정 셀 위치에 따라 조정 필요)
    # 아래는 예시입니다. 실제 데이터 위치에 맞춰 행/열 인덱스를 수정해야 합니다.
    st.sidebar.header("📋 보고 정보")
    st.sidebar.write(f"**작성자:** {df.iloc[4, 1] if len(df)>4 else '확인필요'}") # 작성자 이름 위치
    st.sidebar.write(f"**작성일자:** {df.iloc[6, 1] if len(df)>6 else '확인필요'}")

    # 메인 화면 - 주간 계획 표
    st.subheader("💡 이번 주 핵심 계획 및 실행")
    
    # 엑셀 양식의 요일별 데이터를 보기 좋게 가공하여 출력
    # 데이터 프레임의 범위를 계획서 내용이 들어있는 부분만 슬라이싱합니다.
    plan_df = df.iloc[9:15, [0, 1, 4, 7]] # 요일, 전주계획, 전주실행, 금주계획 컬럼만 선택 (예시)
    plan_df.columns = ["요일", "전주 계획", "전주 실행", "금주 계획"]
    
    st.table(plan_df) # 사장님이 보기 편하시게 깔끔한 표(Table) 형태로 출력

    st.success("위 내용은 구글 시트와 실시간으로 연동되어 있습니다.")
    
    # 누락 방지 알림
    st.info("💡 팁: 매주 월요일 오전 9시에 데이터가 업데이트되었는지 확인하세요!")

except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
    st.info("구글 시트 공유 설정이 '링크가 있는 모든 사용자'로 되어 있는지 확인해 주세요.")
