import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- הגדרות עיצוב מתקדמות GenuLogic ---
st.set_page_config(page_title="GenuLogic - מערך שיעור חכם", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    body, .stApp { 
        background-color: #F5F9FF; 
        direction: rtl; 
        text-align: right;
        font-family: 'Assistant', sans-serif;
    }

    /* כותרת עליונה יוקרתית */
    .header-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 25px; background: white; border-bottom: 2px solid #E3F2FD;
        border-radius: 0 0 20px 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    .brand { color: #1E88E5; font-weight: 800; font-size: 1.3em; letter-spacing: 1px; }
    .dept { color: #90A4AE; font-size: 0.9em; font-weight: 400; }

    /* כרטיסיית תוכן מעוצבת */
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 25px; padding: 25px; margin: 20px 0;
        border: 1px solid #E1F5FE; box-shadow: 0 10px 30px rgba(30, 136, 229, 0.08);
    }

    /* רנדור שברים ב-CSS טהור (iPhone Optimized) */
    .frac {
        display: inline-block; vertical-align: middle; text-align: center; margin: 0 4px;
    }
    .frac > span { display: block; padding: 0 2px; }
    .frac span.bottom { border-top: 2px solid #263238; padding-top: 2px; }

    /* עיצוב טבלאות */
    table { width: 100%; border-collapse: collapse; margin-top: 15px; background: white; border-radius: 12px; overflow: hidden; }
    th { background-color: #E3F2FD; color: #1565C0; padding: 12px; text-align: right; }
    td { padding: 12px; border-bottom: 1px solid #F1F8E9; font-size: 0.95em; }

    /* כפתור הפעלה */
    .stButton>button { 
        width: 100%; border-radius: 18px; height: 3.8em; 
        background: linear-gradient(135deg, #4CAF50 0%, #45A049 100%);
        color: white; border: none; font-weight: 700; font-size: 1.1em;
        transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- תצוגת Header ---
st.markdown("""
    <div class="header-bar">
        <div class="brand">genu_logic</div>
        <div class="dept">מחלקה פדגוגית | מלווה שיעור</div>
    </div>
    """, unsafe_allow_html=True)

def get_model():
    keys = st.secrets.get("GEMINI_KEYS", [])
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-2.0-flash')

st.title("שלום עופרי! 👋")
st.markdown("##### בוא ננתח את דפי התרגול וניצור מערך שיעור מושלם.")

col1, col2 = st.columns(2)
with col1:
    img1 = st.camera_input("סריקת עמוד 1", key="c1")
with col2:
    img2 = st.camera_input("סריקת עמוד 2", key="c2")

if img1 and img2:
    if st.button("ייצר מערך שיעור וניתוח טבלאות"):
        with st.spinner("מנתח נתונים בטכנולוגיית GenuLogic..."):
            try:
                model = get_model()
                image_parts = [Image.open(img1), Image.open(img2)]
                
                prompt = """
                פעל כסוכן פדגוגי בכיר. נתח את דפי התרגול המצורפים.
                
                הנחיות קשיחות לפלט HTML:
                1. זהה את כל התרגילים והטבלאות בדף.
                2. צור טבלת HTML לסיכום הממצאים: | מס' תרגיל | נושא | רמת קושי | דגש פדגוגי |.
                3. עבור שברים, השתמש במבנה: <div class='frac'><span>מונה</span><span class='bottom'>מכנה</span></div>.
                4. בנה תוכנית ל-45 דקות המחולקת לכרטיסיות (HTML div class='content-card').
                5. פתרון מלא: בחר תרגיל אחד מורכב והצג פתרון אלגברי שלב-אחרי-שלב.
                
                דגשי שפה:
                - השתמש בביטוי 'נרשמה שגיאה' בלבד.
                - ללא המילה 'מוקש'.
                - עברית אקדמית, נעימה ומכבדת.
                """
                
                response = model.generate_content([prompt] + image_parts)
                
                # תצוגה
                st.markdown("---")
                st.markdown("### 📋 מערך שיעור מתוכנן")
                
                # ניקוי והצגה
                output = response.text.replace("```html", "").replace("```", "")
                st.markdown(output, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error("הייתה פנייה מרובה מדי, המערכת תתאושש תוך כמה שניות. נסה שוב.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("GenuLogic OS | v3.0 Premium UI")
