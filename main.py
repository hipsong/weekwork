import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 파일 저장 경로
DB_FILE = "weekly_report_db.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame()

st.set_page_config(page_title="제조업 주간계획 시스템", layout="wide")

st.title("🏭 주간 업무 계획/실적 관리")

# 사이드바 메뉴
menu = ["계획 작성 및 저장", "기록 조회"]
choice = st.sidebar.selectbox("메뉴", menu)

days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
rows = ["전주계획", "전주실행", "금주계획"]

if choice == "계획 작성 및 저장":
    st.subheader("📝 주간 계획표 입력")
    
    # 기본 정보 입력
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        write_date = st.date_input("작성 주간 시작일", datetime.now())
    with col_info2:
        dept = st.text_input("부서", value="생산부")
    with col_info3:
        writer = st.text_input("작성자")

    st.divider()

    # 회사 양식에 맞춘 표 형태 입력 창 생성
    data_dict = {"항목": rows}
    
    # 5열 레이아웃을 사용하여 월~금 입력칸 생성
    cols = st.columns(5)
    
    input_data = {} # 데이터를 임시 저장할 딕셔너리
    
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"### {day}")
            day_content = []
            for row in rows:
                content = st.text_area(f"{row}", key=f"{day}_{row}", height=100)
                day_content.append(content)
            input_data[day] = day_content

    if st.button("💾 이 양식대로 저장하기"):
        # 입력 데이터를 데이터프레임으로 변환
        # (날짜/작성자 정보 포함하여 플래트닝)
        new_rows = []
        for row_idx, row_name in enumerate(rows):
            new_entry = {
                "작성일": write_date,
                "부서": dept,
                "작성자": writer,
                "구분": row_name,
                "월": input_data["월요일"][row_idx],
                "화": input_data["화요일"][row_idx],
                "수": input_data["수요일"][row_idx],
                "목": input_data["목요일"][row_idx],
                "금": input_data["금요일"][row_idx]
            }
            new_rows.append(new_entry)
        
        new_df = pd.DataFrame(new_rows)
        old_df = load_data()
        final_df = pd.concat([old_df, new_df], ignore_index=True)
        final_df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
        
        st.success(f"{write_date} 주차 계획이 저장되었습니다!")

elif choice == "기록 조회":
    st.subheader("🔍 주간 계획 및 실적 상세 조회")
    db = load_data()
    
    if not db.empty:
        # 1. 상단 필터링 (날짜와 부서 선택)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            date_list = sorted(db["작성일"].unique(), reverse=True)
            selected_date = st.selectbox("📅 조회할 주간 선택", date_list)
        
        # 데이터 필터링
        display_df = db[db["작성일"] == selected_date].copy()
        
        # 보기 좋게 정렬 (전주계획 -> 전주실행 -> 금주계획 순서)
        order = {"전주계획": 0, "전주실행": 1, "금주계획": 2}
        display_df['sort'] = display_df['구분'].map(order)
        display_df = display_df.sort_values('sort').drop(columns=['sort', '작성일', '부서', '작성자'])

        # 2. 스타일링 적용 (색상 및 테두리)
        def highlight_rows(row):
            if row['구분'] == '전주계획':
                return ['background-color: #f0f2f6'] * len(row)
            elif row['구분'] == '전주실행':
                return ['background-color: #e1f5fe'] * len(row) # 연한 파랑 (실행)
            elif row['구분'] == '금주계획':
                return ['background-color: #e8f5e9'] * len(row) # 연한 녹색 (강조)
            return [''] * len(row)

        # 스타일이 적용된 HTML 표 생성
        styled_df = display_df.style.apply(highlight_rows, axis=1)\
            .set_properties(**{
                'white-space': 'pre-wrap', # 줄바꿈 허용
                'text-align': 'left',
                'border': '1px solid #dee2e6',
                'padding': '10px'
            })\
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#31333F'), ('color', 'white'), ('text-align', 'center')]}
            ])

        # 3. 화면 출력
        st.markdown(f"#### 📋 {selected_date} 보고 (작성자: {db[db['작성일']==selected_date]['작성자'].iloc[0]})")
        st.write(styled_df.to_html(), unsafe_allow_html=True) # HTML로 렌더링하여 스타일 적용
        
        st.divider()
        
        # 엑셀 다운로드 버튼
        csv = display_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 엑셀(CSV) 저장", data=csv, file_name=f"Report_{selected_date}.csv")
        
    else:
        st.info("저장된 데이터가 없습니다.")
