import requests
import schedule
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1488317285318918164/njcqeAgHoa-Gkce2Sit4FY1F_0CFQkH3-BSAPRrFA2ZrTGuFzhaAgUiKgClLOHJbUCtZ"

sent_news = set()

def send_news():
    url = "https://api.tradingeconomics.com/calendar?c=guest:guest&f=json"
    response = requests.get(url)
    data = response.json()

    today = datetime.now().strftime("%Y-%m-%d")

    for event in data:
        currency = event.get("Currency", "")
        importance = str(event.get("Importance", ""))
        title = event.get("Event", "")
        date_raw = event.get("Date", "")
        forecast = event.get("Forecast", "Brak")
        previous = event.get("Previous", "Brak")

        if currency != "USD":
            continue

        if importance != "3":
            continue

        if today not in date_raw:
            continue

        uniqueid = f"{title}{date_raw}"
        if unique_id in sent_news:
            continue

        sent_news.add(unique_id)

        try:
            dt = datetime.fromisoformat(date_raw.replace("Z", ""))
            date_txt = dt.strftime("%d.%m.%Y")
            hour_txt = dt.strftime("%H:%M")
        except:
            date_txt = date_raw
            hour_txt = "?"

        embed = {
            "title": " Kalendarz ekonomiczny",
            "description": (
                f" USD - {title}\n"
                f" {date_txt}\n"
                f" {hour_txt}\n"
                f" Wysoki wpływ na rynek\n\n"
                f" Prognoza: {forecast}\n"
                f" Poprzedni odczyt: {previous}"
            ),
            "color": 16711680,
            "footer": {
                "text": "Automatyczne wiadomości • Bot ekonomiczny"
            }
        }

        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
        print(" Wysłano:", title)

schedule.every(5).minutes.do(send_news)

send_news()

while True:
    schedule.run_pending()
    time.sleep(30)
