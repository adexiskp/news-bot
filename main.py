import os
import requests
from datetime import datetime, timedelta

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def send_news():
    print("🔍 Sprawdzam newsy...")

    url = (
        "https://api.tradingeconomics.com/calendar/"
        "country/united%20states?c=guest:guest&f=json"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    now = datetime.utcnow()
    next_7d = now + timedelta(days=7)

    opisy = []
    licznik = 0

    for event in data:
        title = event.get("Event", "")
        country = event.get("Country", "")
        date_raw = event.get("Date", "")
        forecast = event.get("Forecast", "brak")
        previous = event.get("Previous", "brak")
        importance = event.get("Importance", 0)

        if importance < 2:
            continue

        try:
            event_time = datetime.fromisoformat(date_raw.replace("Z", ""))
        except Exception:
            continue

        if not (now <= event_time <= next_7d):
            continue

        opis = (
            f"📌 **{title}** ({country})\n"
            f"📅 Data: {event_time.strftime('%d.%m.%Y')}\n"
            f"🕒 Godzina: {event_time.strftime('%H:%M')}\n"
            f"📈 Prognoza: {forecast}\n"
            f"📉 Poprzedni: {previous}\n"
            f"🔥 Ważność: {importance}/3\n"
        )

        opisy.append(opis)
        licznik += 1

        if licznik == 5:
            break

    if not opisy:
        print("✅ Brak nowych newsów")
        return

    embed = {
        "title": "📰 Nadchodzące ważne newsy USD",
        "description": "\n\n".join(opisy),
        "color": 16753920,
    }

    response = requests.post(
        WEBHOOK_URL,
        json={"embeds": [embed]},
        timeout=10
    )

    print("📢 Wysłano newsy:", response.status_code)


if __name__ == "__main__":
    send_news()
