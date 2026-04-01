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

    embeds = []

    for event in data:
        currency = event.get("Currency", "")
        importance = str(event.get("Importance", ""))
        title = event.get("Event", "")
        date_raw = event.get("Date", "")
        forecast = event.get("Forecast", "Brak")
        previous = event.get("Previous", "Brak")

        if currency == "USD" and importance == "3":
            unique_id = f"{title}_{date_raw}"
            if unique_id in sent_news:
                continue

            sent_news.add(unique_id)

            try:
                dt = datetime.fromisoformat(date_raw.replace("Z", ""))
                date_txt = dt.strftime("%d %b")
                hour_txt = dt.strftime("%H:%M")
            except:
                date_txt = date_raw
                hour_txt = "?"

            embed = {
                "title": f"🇺🇸 USD - {title}",
                "description": (
                    f"📅 {date_txt}\n"
                    f"🕒 {hour_txt}\n"
                    f"🔴 HIGH impact\n\n"
                    f"**Forecast:** {forecast}\n"
                    f"**Previous:** {previous}"
                ),
                "color": 65280,
                "footer": {
                    "text": "Powered by TradingEconomics"
                }
            }

            embeds.append(embed)

    if embeds:
        requests.post(WEBHOOK_URL, json={"embeds": embeds[:10]})
        print("✅ Wysłano newsy")

schedule.every(5).minutes.do(send_news)

send_news()

while True:
    schedule.run_pending()
    time.sleep(30)
