import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- הגדרות דף ועיצוב GenuLogic ---
st.set_page_config(page_title="GenuLogic - מלווה שיעור", layout="centered")

st.markdown("""
    <style>
    /* רקע Alice Blue עדין לפי הפרוטוקול */
    .main { background-color: #F5F9FF; direction: rtl; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #1E88E5; color: white; font-weight: bold; border: none;
    }
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0; border-bottom: 2px solid #E3F2FD; margin-bottom: 30px;
    }
    .brand-left { font-family: 'Segoe UI', sans-serif; color: #1565C0; font-weight: bold; }
    .dept-right { color: #546E7A; font-size: 0.9em; font-family: 'Segoe UI', sans-serif; }
    div[data-testid="stExpander"] { border: 1px solid #E3F2FD; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- כותרת (Header) ---
st.markdown("""
    <div class="header-container">
        <div class="brand-left">genu_logic</div>
        <div class="dept-right">מחלקה פדגוגית</div>
    </div>
    """, unsafe_allow_html=True)

# --- חיבור למוח (Gemini API) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("נא להגדיר GEMINI_API_KEY ב-Secrets של Streamlit.")
    st.stop()

# שימוש במודל 2.0 פלאש - המהיר והחזק ביותר ל-Vision ב-2026
model = genai.GenerativeModel('gemini-2.0-flash')

# --- ממשק משתמש ---
st.title("שלום עופרי,")
st.subheader("מה תרצה שנלמד היום?")

# צילום עמודים (מצלמה נפתחת אוטומטית בסלולרי)
col1, col2 = st.columns(2)
with col1:
    img1 = st.camera_input("עמוד תרגול 1")
with col2:
    img2 = st.camera_input("עמוד תרגול 2")

if img1 and img2:
    if st.button("צור תוכנית תרגול מותאמת"):
        with st.status("סורק תרגילים ומנתח לוגיקה...", expanded=True) as status:
            try:
                # המרת קבצים לאובייקטי תמונה
                image_parts = [Image.open(img1), Image.open(img2)]
                
                # הנחיה פדגוגית למוח בענן (The Engine)
                prompt = """
                אתה מורה פרטי מומחה במתמטיקה העובד לפי פרוטוקול GenuLogic.
                נתח את התמונות המצורפות ופעל לפי ההנחיות הבאות:
                1. זהה את הנושא המתמטי המופיע בדפים.
                2. בנה תוכנית תרגול מותאמת ל-45 דקות:
                   - אם מדובר באלגברה: צור 7 תרגילים (שינוי מספרים מהמקור).
                   - אם מדובר בבעיות מילוליות מורכבות: צור 3 תרגילים לכל היותר (שינוי דמויות/הקשר), 
                     כאשר פתרון מלא לוקח כ-20 שורות.
                3. עבור כל תרגיל, ציין 'דגש פדגוגי' אחד המבוסס על ניתוח טעויות נפוצות.
                4. שפה וסגנון: אקדמי, מכבד ובגובה העיניים.
                5. איסור מוחלט: אל תשתמש במילה 'מוקש'. השתמש במושג 'ניתוח טעות נפוצה' או 'דגש פדגוגי'.
                6. שפה מכילה: השתמש בביטוי 'נרשמה שגיאה' במקום 'טעית'.
                7. פלט: הצג את התרגילים בפורמט ברור ונוח לקריאה מהסלולרי.
                """
                
                response = model.generate_content([prompt] + image_parts)
                report_text = response.text
                
                status.update(label="הניתוח הושלם בהצלחה!", state="complete", expanded=False)
                
                # הצגת התוצאה
                st.markdown("---")
                st.markdown("### תוכנית השיעור שלך (45 דקות):")
                st.write(report_text)
                
                # שמירת דוח מקומי
                st.session_state['last_report'] = report_text
                
                # כפתור סיום ושליחה לוואטסאפ (סימולציה)
                if st.button("סיימתי תרגול! שלח דוח ביצועים לוואטסאפ"):
                    st.balloons()
                    st.success("הדוח נשלח לסוכן ה-WhatsApp. תרגול הבית (14 תרגילים) בדרך אליך!")
                    
            except Exception as e:
                st.error(f"אירעה שגיאה בעיבוד הענן: {e}")

# סיומת הדף לפי הפרוטוקול
st.markdown("---")
st.caption("GenuLogic OS | פתרונות למידה מתקדמים")
