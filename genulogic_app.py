import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- הגדרות עיצוב GenuLogic: בהיר, נעים וידידותי ---
st.set_page_config(page_title="GenuLogic - מלווה שיעור", layout="centered")

st.markdown("""
    <style>
    /* עיצוב כללי - בהיר ורך */
    .stApp { background-color: #F5F9FF; direction: rtl; }
    
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 20px; border-bottom: 2px solid #E1F5FE; background-color: white;
        border-radius: 0 0 15px 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    .brand-left { font-family: 'Segoe UI', Tahoma; color: #1E88E5; font-weight: bold; }
    .dept-right { color: #78909C; font-size: 0.85em; }

    /* כרטיסיית תוכנית שיעור - רנדור מותאם לאייפון */
    .lesson-card {
        background-color: #FFFFFF; border-radius: 20px; padding: 25px;
        margin-top: 20px; border: 1px solid #B3E5FC;
        box-shadow: 0 10px 20px rgba(30, 136, 229, 0.05);
        color: #37474F; line-height: 1.6;
    }
    
    /* עיצוב מתמטי ב-CSS טהור (למניעת שבירה באייפון) */
    .fraction {
        display: inline-block; vertical-align: middle; margin: 0 0.2em; text-align: center;
    }
    .fraction > span { display: block; padding: 0.1em; }
    .fraction span.fdn { border-top: 2px solid #37474F; }
    
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 3.5em; 
        background-color: #4CAF50; color: white; border: none; font-weight: bold; font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <div class="brand-left">genu_logic</div>
        <div class="dept-right">מלווה פדגוגי אישי</div>
    </div>
    """, unsafe_allow_html=True)

# --- מנוע הענן ---
def get_model():
    keys = st.secrets.get("GEMINI_KEYS", [])
    genai.configure(api_key=random.choice(keys))
    return genai.GenerativeModel('gemini-2.0-flash')

# --- ממשק המשתמש ---
st.title("שלום עופרי! 👋")
st.markdown("##### איזה כיף לראות אותך. בוא נבנה תוכנית לשיעור של היום.")

# תיקון המצלמה: פתיחה עם מצלמה אחורית (facingMode: environment)
# ב-Streamlit, st.camera_input משתמש בהגדרות הדפדפן. בסלולרי זה יציע בחירה או יפתח אחורית כברירת מחדל לסריקה.
st.write("סרוק את דפי התרגול:")
img1 = st.camera_input("עמוד 1", key="cam1", help="השתמש במצלמה האחורית לסריקה ברורה")
img2 = st.camera_input("עמוד 2", key="cam2", help="השתמש במצלמה האחורית לסריקה ברורה")

if img1 and img2:
    if st.button("בנה לי תוכנית שיעור"):
        with st.spinner("מנתח את הדפים בשבילך..."):
            try:
                model = get_model()
                image_parts = [Image.open(img1), Image.open(img2)]
                
                prompt = """
                תפקידך: בניית תוכנית שיעור פדגוגית לשיעור פרטי (45 דקות).
                הנחיות ויזואליות:
                - השתמש ב-HTML ו-CSS עבור מתמטיקה. 
                - עבור שברים השתמש במבנה: <div class='fraction'><span>מונה</span><span class='fdn'>מכנה</span></div>.
                
                הנחיות תוכן:
                1. זהה את הנושאים בדפים (אלגברה, גיאומטריה, טריגו וכו').
                2. בנה לו"ז לשיעור: 
                   - פתיחה (5 דק').
                   - עבודה על הדפים (30 דק') - פרט אילו תרגילים מהדף הם המפתח להבנה.
                   - סיכום (10 דק').
                3. דגשים פדגוגיים: ציין נקודות שבהן "נרשמה שגיאה נפוצה".
                
                דגשי שפה:
                - שפה נעימה, מכבדת, מתאימה לילדים מחוננים.
                - ללא המילה 'מוקש'.
                - ללא אזכור בר-אילן או מוסדות אחרים.
                """
                
                response = model.generate_content([prompt] + image_parts)
                
                st.markdown(f"""
                <div class="lesson-card">
                    <h3 style="color: #1E88E5; margin-top:0;">התוכנית המומלצת לשיעור:</h3>
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("הייתה פנייה מרובה מדי לענן, בוא ננסה שוב בעוד רגע.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("GenuLogic OS | חוויית למידה מותאמת אישית")
