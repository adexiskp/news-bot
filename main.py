import requests
import schedule
import time
from datetime import datetime, timedelta

WEBHOOK_URL = "https://discord.com/api/webhooks/1488317285318918164/njcqeAgHoa-Gkce2Sit4FY1F_0CFQkH3-BSAPRrFA2ZrTGuFzhaAgUiKgClLOHJbUCtZ"

sent_news = set()


def send_news():
    try:
        print("🔍 Sprawdzam newsy...")

        url = (
            "https://api.tradingeconomics.com/calendar/"
            "country/united%20states?c=guest:guest&importance=3&f=json"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        now = datetime.utcnow()
        next_7d = now + timedelta(days=7)

        found_any = False

        for event in data:
            title = event.get("Event", "")
            date_raw = event.get("Date", "")
            forecast = event.get("Forecast", "brak")
            previous = event.get("Previous", "brak")

            try:
                event_time = datetime.fromisoformat(date_raw.replace("Z", ""))
            except:
                continue

            # tylko newsy z najbliższych 7 dni
           if event_time <= now:
    continue

            unique_id = f"{title}_{date_raw}"

            if unique_id in sent_news:
                continue

            sent_news.add(unique_id)
            found_any = True

            date_txt = event_time.strftime("%d.%m.%Y")
            hour_txt = event_time.strftime("%H:%M")

            embed = {
                "title": "📢 Nadchodzący ważny news USD",
                "description": (
                    f"**{title}**\n"
                    f"📅 {date_txt}\n"
                    f"🕒 {hour_txt}\n"
                    f"🔴 High impact\n\n"
                    f"📈 **Prognoza:** {forecast}\n"
                    f"📉 **Poprzedni:** {previous}"
                ),
            }

            try:
                requests.post(
                    WEBHOOK_URL,
                    json={"embeds": [embed]},
                    timeout=10
                )
                print("📢 Wysłano:", title)
            except Exception as e:
                print("❌ Błąd wysyłki Discord:", e)

        if not found_any:
            print("✅ Brak nowych newsów")

    except Exception as e:
        print("❌ Błąd API:", e)


print("🚀 BOT STARTED")

schedule.every(30).minutes.do(send_news)

send_news()

while True:
    try:
        schedule.run_pending()
        time.sleep(30)
    except Exception as e:
        print("❌ Błąd pętli:", e)
        time.sleep(30)
