from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi"):
        return "Hey!"

    if user_message in ("who are you"):
        return "I am a chat bot"
    if user_message in ("time"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y")
        return str(date_time)
