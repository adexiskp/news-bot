import requests
import schedule
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1488317285318918164/njcqeAgHoa-Gkce2Sit4FY1F_0CFQkH3-BSAPRrFA2ZrTGuFzhaAgUiKgClLOHJbUCtZ"

def send_news():
    today = datetime.now().strftime("%d.%m.%Y")

    embed = {
        "title": "📢 Kalendarz ekonomiczny",
        "description": (
            f"🇺🇸 **USD - Liczba ofert pracy JOLTS**\n"
            f"📅 **{today}**\n"
            f"🕒 **15:00**\n"
            f"🔴 **Wysoki wpływ na rynek**\n\n"
            f"📈 **Prognoza:** 6.89M\n"
            f"📊 **Poprzedni odczyt:** 6.95M"
        ),
        "color": 16711680,
        "footer": {
            "text": "Automatyczne wiadomości • Bot ekonomiczny"
        }
    }

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    print("✅ Wysłano nową wiadomość")

schedule.every().day.at("01:00").do(send_news)

while True:
    schedule.run_pending()
    time.sleep(1)
