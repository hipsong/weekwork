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

st.set_page_config(page_title="세라솔 주간계획", layout="wide")

st.title("🏭 주간 업무 계획")

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
    st.subheader("🔍 주간 계획 조회 / 수정 / 삭제")
    db = load_data()
    
    if not db.empty:
        # 1. 조회 필터
        date_list = sorted(db["작성일"].unique(), reverse=True)
        selected_date = st.selectbox("📅 조회할 주간 선택", date_list)
        
        # 선택된 데이터 추출
        mask = db["작성일"] == selected_date
        display_df = db[mask].copy()
        
        # 정렬 순서 정의
        order = {"전주계획": 0, "전주실행": 1, "금주계획": 2}
        display_df['sort'] = display_df['구분'].map(order)
        display_df = display_df.sort_values('sort')

        # ---------------------------------------------------------
        # 2. 수정 및 삭제 버튼 레이아웃
        col_edit, col_del, _ = st.columns([1, 1, 5])
        
        # 수정 모드 상태 관리
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False

        if col_edit.button("✏️ 데이터 수정"):
            st.session_state.edit_mode = True

        if col_del.button("🗑️ 데이터 삭제"):
            # 데이터 삭제 로직
            new_db = db[~mask] # 현재 날짜만 제외하고 나머지 저장
            new_db.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
            st.error(f"{selected_date} 데이터가 삭제되었습니다.")
            st.rerun() # 화면 새로고침

        # ---------------------------------------------------------
        # 3. 데이터 표시 또는 수정 폼
        if st.session_state.edit_mode:
            st.warning("⚠️ 수정 모드입니다. 내용을 고친 후 '수정 완료'를 눌러주세요.")
            updated_rows = []
            
            # 각 요일별/구분별 수정 입력창 생성
            for idx, row in display_df.iterrows():
                st.markdown(f"#### [{row['구분']}]")
                edit_cols = st.columns(5)
                updated_day_values = {}
                for i, day in enumerate(["월", "화", "수", "목", "금"]):
                    updated_day_values[day] = edit_cols[i].text_area(f"{day}요일", value=row[day], key=f"edit_{idx}_{day}")
                
                # 수정한 데이터 구성
                updated_rows.append({
                    "작성일": row["작성일"], "부서": row["부서"], "작성자": row["작성자"],
                    "구분": row["구분"], "월": updated_day_values["월"], "화": updated_day_values["화"],
                    "수": updated_day_values["수"], "목": updated_day_values["목"], "금": updated_day_values["금"]
                })
            
            if st.button("✅ 수정 완료"):
                # 기존 데이터 삭제 후 새 데이터 추가
                other_data = db[~mask]
                updated_df = pd.DataFrame(updated_rows)
                final_df = pd.concat([other_data, updated_df], ignore_index=True)
                final_df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
                st.session_state.edit_mode = False
                st.success("수정이 완료되었습니다!")
                st.rerun()
            
            if st.button("❌ 취소"):
                st.session_state.edit_mode = False
                st.rerun()

        else:
            # 4. 일반 조회 화면 (시인성 강조 스타일)
            def highlight_rows(row):
                if row['구분'] == '전주계획': return ['background-color: #f0f2f6'] * len(row)
                elif row['구분'] == '전주실행': return ['background-color: #e1f5fe'] * len(row)
                elif row['구분'] == '금주계획': return ['background-color: #e8f5e9'] * len(row)
                return [''] * len(row)

            styled_df = display_df.drop(columns=['sort', '작성일', '부서', '작성자']).style.apply(highlight_rows, axis=1)\
                .set_properties(**{'white-space': 'pre-wrap', 'text-align': 'left', 'border': '1px solid #dee2e6', 'padding': '10px'})
            
            st.write(styled_df.to_html(), unsafe_allow_html=True)
            
            # 엑셀 다운로드
            csv = display_df.drop(columns=['sort']).to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button("📥 엑셀(CSV) 다운로드", data=csv, file_name=f"Report_{selected_date}.csv")
            
    else:
        st.info("저장된 데이터가 없습니다.")
