import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- הגדרות עיצוב GenuLogic ---
st.set_page_config(page_title="GenuLogic - מלווה שיעור", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F5F9FF; direction: rtl; font-family: 'Segoe UI', sans-serif; }
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 20px; border-bottom: 2px solid #E3F2FD; background-color: white;
    }
    .exercise-card {
        background-color: white; border-radius: 15px; padding: 20px;
        margin-bottom: 20px; border-right: 5px solid #1E88E5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .pedagogical-focus {
        background-color: #E3F2FD; border-radius: 10px; padding: 10px;
        font-size: 0.9em; margin-top: 10px; color: #1565C0;
    }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #1E88E5; color: white; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <div style="color: #1565C0; font-weight: bold;">genu_logic</div>
        <div style="color: #546E7A; font-size: 0.9em;">מחלקה פדגוגית</div>
    </div>
    """, unsafe_allow_html=True)

# --- מנגנון רוטציית מפתחות (Anti-429) ---
def get_model():
    keys = st.secrets.get("GEMINI_KEYS", [])
    if not keys:
        st.error("לא הוגדרו מפתחות API ב-Secrets.")
        st.stop()
    
    # בחירת מפתח רנדומלי כדי לפזר את העומס
    random_key = random.choice(keys)
    genai.configure(api_key=random_key)
    return genai.GenerativeModel('gemini-2.0-flash')

# --- ממשק משתמש ---
st.title("שלום עופרי,")
st.subheader("מה תרצה שנלמד היום?")

img1 = st.camera_input("עמוד תרגול 1")
img2 = st.camera_input("עמוד תרגול 2")

if img1 and img2:
    if st.button("בנה תוכנית תרגול מותאמת"):
        with st.spinner("מנתח נתונים בשרת..."):
            try:
                model = get_model()
                image_parts = [Image.open(img1), Image.open(img2)]
                
                # הנחיה מחמירה לפורמט ויזואלי ודיוק מתמטי
                prompt = """
                פעל כסוכן פדגוגי בכיר ב-GenuLogic. נתח את הדפים המצורפים.
                עליך להחזיר תגובה בפורמט Markdown ברור הכולל:
                1. זיהוי מדויק של הנושא (למשל: משוואות מעריכיות).
                2. יצירת תרגילים מותאמים (7 לאלגברה / 3 לבעיות מילוליות).
                3. לכל תרגיל כתוב פתרון סופי בתוך בלוק קוד.
                4. לכל תרגיל הוסף 'דגש פדגוגי' (שימוש במונח 'נרשמה שגיאה נפוצה').
                5. השתמש ב-LaTeX עבור נוסחאות מתמטיות (למשל $x^2 + 5x + 6 = 0$).
                
                חשוב: ודא שהמספרים בתרגילים החדשים הגיוניים ויוצרים פתרונות נוחים ללמידה.
                אל תשתמש במילה 'מוקש'.
                """
                
                response = model.generate_content([prompt] + image_parts)
                
                # הצגת התוצאה בתוך קונטיינר מעוצב
                st.markdown("---")
                st.markdown("### תוכנית השיעור שנבנתה עבורך:")
                
                # פיצול התגובה לפי תרגילים (בהנחה שהמודל משתמש במספור)
                exercises = response.text.split("תרגיל")
                for ex in exercises[1:]: # דילוג על הפתיח
                    st.markdown(f"""
                    <div class="exercise-card">
                        <strong>תרגיל {ex.splitlines()[0]}</strong>
                        <p>{chr(10).join(ex.splitlines()[1:])}</p>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("סיימתי! שלח דוח ביצועים"):
                    st.balloons()
            
            except Exception as e:
                if "429" in str(e):
                    st.error("עומס זמני על השרת (429). המערכת תנסה להחליף מפתח באופן אוטומטי, אנא נסה ללחוץ שוב בעוד כמה שניות.")
                else:
                    st.error(f"שגיאה בעיבוד: {e}")

st.markdown("---")
st.caption("GenuLogic OS | פיתוח תוכניות למידה")
