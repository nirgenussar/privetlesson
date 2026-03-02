import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- הגדרות דף: בהיר, רחב וצמוד לימין ---
st.set_page_config(page_title="GenuLogic - מערך שיעור", layout="centered")

# CSS ממוקד לפתרון בעיות התצוגה והיישור
st.markdown("""
    <style>
    /* הגדרת רקע בהיר ויישור לימין */
    .stApp { 
        background-color: #F5F9FF; 
        direction: rtl; 
        text-align: right; 
    }
    
    /* כותרת עליונה נקייה */
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 20px; border-bottom: 2px solid #BBDEFB; background-color: white;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    .brand-left { color: #1E88E5; font-weight: bold; font-family: 'Segoe UI', Tahoma; }
    .dept-right { color: #546E7A; font-size: 0.9em; }

    /* כרטיסיית שיעור מעוצבת ובהירה */
    .lesson-card {
        background-color: white; border-radius: 15px; padding: 25px;
        border-right: 8px solid #4CAF50; border-left: 1px solid #E1F5FE;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        color: #263238; font-size: 1.1em;
    }
    
    .solution-block {
        background-color: #FAFAFA; border: 1px dashed #90CAF9;
        padding: 15px; border-radius: 10px; margin-top: 10px;
        font-family: 'Courier New', monospace; direction: ltr; text-align: left;
    }

    /* כפתור גדול וירוק */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #4CAF50; color: white; border: none; font-weight: bold;
    }
    
    /* הסתרת אלמנטים מיותרים של Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <div class="brand-left">genu_logic</div>
        <div class="dept-right">מערך שיעור פדגוגי</div>
    </div>
    """, unsafe_allow_html=True)

def get_model():
    keys = st.secrets.get("GEMINI_KEYS", [])
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-2.0-flash')

st.title("שלום עופרי! 👋")
st.markdown("### בוא נבנה מערך שיעור מלא כולל פתרונות.")

# הנחיה למצלמה
st.info("בסלולרי: אם המצלמה נפתחת עליך, לחץ על כפתור 'החלף מצלמה' בתוך חלונית הצילום.")

img1 = st.camera_input("סריקת עמוד 1", key="scan1")
img2 = st.camera_input("סריקת עמוד 2", key="scan2")

if img1 and img2:
    if st.button("צור מערך שיעור ופתרונות מלאים"):
        with st.spinner("מנתח את הדפים ומייצר פתרונות..."):
            try:
                model = get_model()
                image_parts = [Image.open(img1), Image.open(img2)]
                
                # הנחיה מחמירה למניעת קוד HTML חשוף ודיוק פדגוגי
                prompt = """
                אתה סוכן פדגוגי של GenuLogic. עליך לייצר מערך שיעור ל-45 דקות על בסיס התמונות.
                
                דרישות התוכן:
                1. זיהוי נושאים מדויק (למשל: זהויות טריגונומטריות, אי-שוויונות).
                2. מבנה זמן: פתיחה (5), עבודה מרכזית (30), סיכום (10).
                3. פתרונות מלאים: בחר את 2 התרגילים הכי חשובים בדף וכתוב עבורם פתרון אלגברי מלא ומפורט (עד 20 שורות לפתרון).
                4. דגש פדגוגי: היכן "נרשמה שגיאה נפוצה"? (ללא המילה 'מוקש').

                דרישות תצוגה (חשוב מאוד!):
                - אל תשתמש בסימני $ או ב-LaTeX מורכב. השתמש בטקסט נקי או ב-HTML פשוט.
                - אל תציג תגיות HTML כטקסט.
                - כתוב הכל בעברית, צמוד לימין.
                - עבור פתרונות מתמטיים, השתמש בסימנים פשוטים: ^ לחזקה, / לשבר, sqrt לשורש.
                """
                
                response = model.generate_content([prompt] + image_parts)
                
                # ניקוי בסיסי של הפלט למקרה שהמודל חרג מההנחיות
                clean_text = response.text.replace("```html", "").replace("```", "")
                
                st.markdown("---")
                st.markdown("### 📋 תוכנית שיעור מאושרת")
                
                # הצגה בתוך כרטיסייה בהירה
                st.markdown(f"""
                <div class="lesson-card">
                    {clean_text}
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error("הענן עמוס, נסה שוב בעוד כמה שניות.")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("GenuLogic OS | v2.5 | פתרונות למידה חכמים")
