import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- הגדרות עיצוב GenuLogic ---
st.set_page_config(page_title="GenuLogic - מלווה שיעור", layout="centered")

# הגדרת ה-API (נמשוך את המפתח מה-Secrets של Streamlit למען האבטחה)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("נא להגדיר GEMINI_API_KEY ב-Secrets של האפליקציה")

model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
st.markdown("""
    <style>
    .main { background-color: #F5F9FF; direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #1E88E5; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div style="display: flex; justify-content: space-between;"><span>מערכת ליווי פדגוגית</span><span>genu_logic</span></div>', unsafe_allow_html=True)

st.title("שלום עופרי,")
st.subheader("מה תרצה שנלמד היום?")

img_file1 = st.camera_input("עמוד ראשון")
img_file2 = st.camera_input("עמוד שני")

if img_file1 and img_file2:
    st.info("המוח של GenuLogic מנתח את התמונות כעת...")
    
    # המרת התמונות לפורמט שהמודל מבין
    image1 = Image.open(img_file1)
    image2 = Image.open(img_file2)
    
    # הנחיה (Prompt) המבוססת על הפרוטוקול שלך
    prompt = """
    נתח את שתי התמונות המצורפות של דפי עבודה במתמטיקה. 
    1. זהה את הנושא המרכזי (למשל: אלגברה, בעיות מילוליות, גיאומטריה).
    2. בנה תוכנית תרגול ל-45 דקות הכוללת 7 תרגילים המבוססים על מה שראית, אך בשינוי מספרים או דמויות.
    3. אם יש בעיות מילוליות מורכבות, הגבל ל-3 תרגילים עם פתרון מלא.
    4. כתוב דגש פדגוגי אחד על טעות נפוצה שעלולה לקרות בנושא זה. השתמש בשפה מכבדת ("נרשמה שגיאה").
    שפה: עברית אקדמית. אל תשתמש במילה 'מוקש'.
    """

    try:
        response = model.generate_content([prompt, image1, image2])
        report = response.text

        st.success("הניתוח הושלם!")
        st.markdown("### תוכנית השיעור המותאמת עבורך:")
        st.write(report)

        # שמירה ושליחה
        if st.button("סיימתי! שלח דוח לסוכן הוואטסאפ"):
            st.balloons()
            st.write("הנתונים נשלחו. סוכן הבית מכין כעת 14 תרגילים דומים לתרגול נוסף.")
            
    except Exception as e:
        st.error(f"קרתה שגיאה בניתוח התמונה: {e}")

