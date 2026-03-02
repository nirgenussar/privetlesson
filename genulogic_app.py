import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- הגדרות עיצוב GenuLogic: בהיר, אקדמי ונגיש ---
st.set_page_config(page_title="GenuLogic - מלווה פדגוגי", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FBFF; direction: rtl; font-family: 'Segoe UI', sans-serif; }
    
    /* עיצוב כותרת עליונה */
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 20px; border-bottom: 2px solid #D1E9FF; background-color: white;
        border-radius: 0 0 15px 15px; margin-bottom: 25px;
    }
    .brand-left { color: #1976D2; font-weight: bold; font-size: 1.1em; }
    .dept-right { color: #607D8B; font-size: 0.85em; }

    /* כרטיסיית תוכנית שיעור מעוצבת */
    .lesson-section {
        background-color: white; border-radius: 15px; padding: 20px;
        margin-bottom: 15px; border-right: 6px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); color: #263238;
    }
    .time-badge {
        background-color: #E8F5E9; color: #2E7D32; padding: 4px 10px;
        border-radius: 20px; font-weight: bold; font-size: 0.9em; margin-left: 10px;
    }
    .topic-title { color: #1565C0; font-weight: bold; font-size: 1.1em; margin-bottom: 10px; }
    
    /* תיקון תצוגת מתמטיקה למובייל */
    .math-content { font-family: 'Cambria Math', 'Times New Roman', serif; font-size: 1.2em; line-height: 1.4; }
    
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #1E88E5; color: white; border: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <div class="brand-left">genu_logic</div>
        <div class="dept-right">מלווה שיעור אישי</div>
    </div>
    """, unsafe_allow_html=True)

def get_model():
    keys = st.secrets.get("GEMINI_KEYS", [])
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-2.0-flash')

st.title("שלום עופרי! 👋")
st.markdown("##### בוא ננתח את דפי התרגול ונבנה תוכנית לשיעור.")

# מצלמה אחורית לסריקה
img1 = st.camera_input("סריקת עמוד 1 (מצלמה אחורית)", key="c1")
img2 = st.camera_input("סריקת עמוד 2 (מצלמה אחורית)", key="c2")

if img1 and img2:
    if st.button("בנה תוכנית שיעור מפורטת"):
        with st.spinner("סורק תכנים ומגדיר יעדים..."):
            try:
                model = get_model()
                image_parts = [Image.open(img1), Image.open(img2)]
                
                # הנחיה לזיהוי מדויק ורינדור נקי
                prompt = """
                אתה סוכן פדגוגי בכיר ב-GenuLogic. נתח את הדפים המצורפים בדייקנות.
                
                שלב 1: זיהוי נושאים (שם לב להבדל בין זהויות טריגונומטריות לאי-שוויונות).
                שלב 2: בניית לו"ז לשיעור של 45 דקות.
                
                פורמט הפלט (חובה להשתמש ב-HTML פשוט עבור כרטיסיות):
                <div class='lesson-section'>
                    <div class='topic-title'>נושאי השיעור שזוהו</div>
                    <p>פרט כאן את הנושאים המדויקים (למשל: אי-שוויונות רציונליים וזהויות טריגונומטריות).</p>
                </div>
                
                <div class='lesson-section'>
                    <div class='topic-title'><span class='time-badge'>0-10 דק'</span>פתיחה ורענון</div>
                    <p>אילו מושגים מהדף דורשים הסבר מקדים?</p>
                </div>
                
                <div class='lesson-section'>
                    <div class='topic-title'><span class='time-badge'>10-35 דק'</span>עבודה על התרגילים</div>
                    <p>אילו תרגילים ספציפיים בדף הם החשובים ביותר? (הצג נוסחאות בטקסט פשוט או ב-LaTeX בסיסי ללא קוד מיותר).</p>
                </div>
                
                <div class='lesson-section'>
                    <div class='topic-title'>דגשים פדגוגיים</div>
                    <p>איפה נרשמה שגיאה נפוצה בדפים אלו?</p>
                </div>

                איסורים: ללא המילה 'מוקש'. ללא אזכור בר-אילן. שפה אקדמית ומכבדת.
                """
                
                response = model.generate_content([prompt] + image_parts)
                
                # הצגת התוצאה המרונדרת
                st.markdown(response.text, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("הענן עמוס כרגע, בוא ננסה שוב בעוד רגע.")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("GenuLogic OS | Smart Lesson Planning")
