import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
import random

# =========================
# GEMINI CLIENT
# =========================
client = genai.Client(api_key="AIzaSyCKMhXE0Af3_cel6joCT0SkOHIU2qm-naQ")

# =========================
# AI MESSAGE FUNCTION
# =========================
styles = [
    "very casual and fun",
    "friendly and polite",
    "short and energetic",
    "warm and appreciative",
    "cool and playful"
]

def ai_write_body(name, meal):
    try:
        style = random.choice(styles)

        prompt = f"""
Write a short, friendly email reminder for a college student.

Student name: {name}
Meal: {meal}

Instructions:
- Ask the student to scan the QR code and give mess food feedback
- Include a polite thank-you line
- Write the message in a {style} tone
- Change wording and emoji every time

Style rules:
- 2-3 lines only
- Use emojis naturally
"""

        response = client.models.generate_content(
            model="models/gemini-pro-latest",
            contents=prompt,
            config={
                "temperature": 0.9,
                "top_p": 0.95
            }
        )

        return response.text.strip()

    except Exception as e:
        print("⚠️ AI failed, using fallback:", e)
        return f"Hey {name}! 🍽️ Please scan the QR code and share your {meal} feedback 😊"

# =========================
# EMAIL CONFIG
# =========================
SENDER_EMAIL = "dsalaar98@gmail.com"
APP_PASSWORD = "skul mfth bvcx pvae"
MEAL_TYPE = "Lunch"

students = [
    {"name": "Tejesh", "email": "tejesh6414@gmail.com"},
    {"name": "IYKY", "email": "nagabhusanam63@gmail.com"}
]

# =========================
# SEND EMAILS
# =========================
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

try:
    server.login(SENDER_EMAIL, APP_PASSWORD)
    print("✅ Logged in to Gmail SMTP")

    for student in students:
        ai_message = ai_write_body(student["name"], MEAL_TYPE)

        final_body = ai_message

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = student["email"]
        msg["Subject"] = f"🍽️ Mess Food Feedback – {MEAL_TYPE}"

        msg.attach(MIMEText(final_body, "plain"))
        server.sendmail(SENDER_EMAIL, student["email"], msg.as_string())

        print(f"📧 Email sent to {student['name']}")

    server.quit()
    print("✅ All emails sent successfully")

except smtplib.SMTPAuthenticationError:
    print("❌ Gmail authentication failed")
