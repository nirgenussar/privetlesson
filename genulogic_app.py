import streamlit as st
import time
import os

# --- הגדרות עיצוב GenuLogic ---
st.set_page_config(page_title="GenuLogic - מלווה שיעור", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F5F9FF; direction: rtl; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #1E88E5; color: white; font-weight: bold; border: none;
    }
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0; border-bottom: 2px solid #E3F2FD; margin-bottom: 20px;
    }
    .brand-left { font-family: 'Segoe UI', Tahoma; color: #1565C0; font-weight: bold; }
    .dept-right { color: #546E7A; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- Header (לפי הפרוטוקול) ---
st.markdown("""
    <div class="header-container">
        <div class="brand-left">genu_logic</div>
        <div class="dept-right">מערכת ליווי פדגוגית</div>
    </div>
    """, unsafe_allow_html=True)

# --- מסך פתיחה ---
st.title("שלום עופרי,")
st.markdown("### מה תרצה שנלמד היום?")

# --- צילום תרגילים (פתיחת מצלמה בסלולרי) ---
st.write("צלם את שני עמודי התרגול:")
img_file1 = st.camera_input("עמוד ראשון")
img_file2 = st.camera_input("עמוד שני")

if img_file1 and img_file2:
    st.info("הקבצים נשלחו לענן. המערכת מנתחת את הלוגיקה...")
    
    # סימולציה של עיבוד ענן (AI Vision)
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        progress_bar.progress(i + 1)
    
    # --- יצירת תוכן הדו"ח (לוגיקה פדגוגית) ---
    # כאן בעתיד ה-AI יחליט אם זה אלגברה או בעיות מילוליות
    is_algebra = True # לצורך ההדגמה
    
    if is_algebra:
        practice_plan = """
        1. פירוק לגורמים (שינוי מספרים)
        2. משוואות ריבועיות (וריאציה של דמויות)
        3. צמצום שברים אלגבריים (פתרון מלא - 20 שורות)
        4. תרגיל העמקה: חקירת פונקציה
        5. תרגיל טכניקה מהיר
        6. תרגיל טכניקה מהיר
        7. סיכום נושא: פירוק לפי קבוצות
        """
    else:
        practice_plan = """
        1. בעיה מילולית כבדה (תנועה) - פתרון מלא
        2. בעיה מילולית (הספק) - שינוי דמויות
        3. בעיה מילולית משולבת - פתרון מלא
        """

    report = f"""--- דוח שיעור: עופרי ---
נושא: אלגברה וטכניקה
זמן תרגול מתוכנן: 45 דקות

תכנית עבודה:
{practice_plan}

דגש פדגוגי:
בניתוח טעויות נפוצות בנושא זה, נרשמה שגיאה במעבר בין אגפים. 
שים לב לשינוי הסימן (+) ו-(-).
"""

    st.success("האפליקציה מוכנה!")
    st.markdown("### תכנית השיעור שלך:")
    st.markdown(f"```\n{report}\n```")

    # שמירת קובץ TXT מקומי
    with open("lesson_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    # כפתור סיום ושליחה
    if st.button("סיימתי! שלח דוח לוואטסאפ"):
        st.balloons()
        st.write("הנתונים נשלחו לסוכן הוואטסאפ. הוא יכין לך תרגול בית (14 תרגילים) בקרוב.")