import requests
import schedule
import time
from datetime import datetime, timedelta

WEBHOOK_URL = "https://discord.com/api/webhooks/1488317285318918164/njcqeAgHoa-Gkce2Sit4FY1F_0CFQkH3-BSAPRrFA2ZrTGuFzhaAgUiKgClLOHJbUCtZ"

sent_news = set()

def send_news():
    url = "https://api.tradingeconomics.com/calendar/country/united%20states?c=guest:guest&importance=3&f=json"
    response = requests.get(url)
    data = response.json()

    now = datetime.utcnow()
    next_24h = now + timedelta(hours=24)

    for event in data:
        title = event.get("Event", "")
        date_raw = event.get("Date", "")
        forecast = event.get("Forecast", "Brak")
        previous = event.get("Previous", "Brak")

        try:
            event_time = datetime.fromisoformat(date_raw.replace("Z", ""))
        except:
            continue

        # tylko eventy z najbliższych 24h
        if not (now <= event_time <= next_24h):
            continue

        unique_id = f"{title}_{date_raw}"
        if unique_id in sent_news:
            continue

        sent_news.add(unique_id)

        date_txt = event_time.strftime("%d.%m.%Y")
        hour_txt = event_time.strftime("%H:%M")

        embed = {
            "title": "📢 Kalendarz ekonomiczny",
            "description": (
                f"🇺🇸 **USD - {title}**\n"
                f"📅 {date_txt}\n"
                f"🕒 {hour_txt}\n"
                f"🔴 Wysoki wpływ na rynek\n\n"
                f"📈 **Prognoza:** {forecast}\n"
                f"📊 **Poprzedni odczyt:** {previous}"
            ),
            "color": 16711680,
            "footer": {
                "text": "Automatyczne wiadomości • TradingEconomics"
            }
        }

        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
        print("✅ Wysłano:", title)

schedule.every(5).minutes.do(send_news)

send_news()

while True:
    schedule.run_pending()
    time.sleep(30)
