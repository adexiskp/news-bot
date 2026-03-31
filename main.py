import os
import requests
import schedule
import time

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_news():
    embed = {
        "title": "📅 Kalendarz ekonomiczny",
        "description": "🇺🇸 USD - JOLTS Job Openings\n🔴 WYSOKI WPŁYW",
        "color": 16711680
    }

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    print("Wysłano")

schedule.every().day.at("01:00").do(send_news)

while True:
    schedule.run_pending()
    time.sleep(30)
