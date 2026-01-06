import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from google.genai import types


# ================== AI MESSAGE GENERATOR ==================

class AIMessageGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.styles = [
            "very casual and fun",
            "friendly and polite",
            "short and energetic",
            "warm and appreciative"
        ]

    def generate(self, name, meal):
        try:
            style = random.choice(self.styles)

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
- Use 1-2 emojis naturally
"""

            response = self.client.models.generate_content(model="models/gemini-pro-latest",
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                       temperature=0.9,
                                        top_p=0.95,)
                                                           )

            return response.text.strip()

        except Exception:
            return f"Hey {name}! 🍽️ Please scan the QR code and share your feedback 😊"


# ================== EMAIL SENDER ==================

class EmailSender:
    def __init__(self, sender_email, app_password):
        self.sender_email = sender_email
        self.app_password = app_password
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()

    def login(self):
        self.server.login(self.sender_email, self.app_password)

    def send(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        self.server.sendmail(self.sender_email, to_email, msg.as_string())

    def close(self):
        self.server.quit()


# ================== MAIN NOTIFIER ==================

class MessFeedbackNotifier:
    def __init__(self, ai_generator, email_sender, meal_name):
        self.ai_generator = ai_generator
        self.email_sender = email_sender
        self.meal_name = meal_name

    def notify_students(self, students):
        for student in students:
            message = self.ai_generator.generate(
                student["name"],
                self.meal_name
            )

            subject = f"🍽️ Mess Food Feedback – {self.meal_name}"

            self.email_sender.send(
                student["email"],
                subject,
                message
            )


# ================== CONFIG ==================

GEMINI_API_KEY = "AIzaSyCKMhXE0Af3_cel6joCT0SkOHIU2qm-naQ"
SENDER_EMAIL = "dsalaar98@gmail.com"
APP_PASSWORD = "skul mfth bvcx pvae"
MEAL_TY = "Today's Meal"

students = [
    {"name": "MIKE", "email": "tejesh6414@gmail.com"},
    {"name": "EL", "email": "nagabhusanam63@gmail.com"}
]


# ================== RUN ==================

if __name__ == "__main__":
    ai_gen = AIMessageGenerator(GEMINI_API_KEY)
    mailer = EmailSender(SENDER_EMAIL, APP_PASSWORD)

    try:
        mailer.login()
        print("✅ Logged in to Gmail")

        notifier = MessFeedbackNotifier(ai_gen, mailer, MEAL_TY)
        notifier.notify_students(students)

        print("✅ All emails sent successfully")

    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail authentication failed")

    finally:
        mailer.close()
