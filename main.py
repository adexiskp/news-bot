import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def send_news():
    print("🔍 Pobieram newsy...")

    url = (
        "https://api.tradingeconomics.com/calendar/"
        "country/united%20states?c=guest:guest&f=json"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

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
            data_txt = event_time.strftime("%d.%m.%Y")
            godzina_txt = event_time.strftime("%H:%M")
        except Exception:
            data_txt = "brak"
            godzina_txt = "brak"

        opis = (
            f"📌 **{title}** ({country})\n"
            f"📅 Data: {data_txt}\n"
            f"🕒 Godzina: {godzina_txt}\n"
            f"📈 Prognoza: {forecast}\n"
            f"📉 Poprzedni: {previous}\n"
            f"🔥 Ważność: {importance}/3"
        )

        opisy.append(opis)
        licznik += 1

        if licznik == 5:
            break

    if not opisy:
        print("❌ API nic nie zwróciło")
        return

    embed = {
        "title": "📰 Najbliższe ważne newsy",
        "description": "\n\n".join(opisy),
        "color": 16753920
    }

    response = requests.post(
        WEBHOOK_URL,
        json={"embeds": [embed]},
        timeout=10
    )

    print("📢 Discord status:", response.status_code)


if __name__ == "__main__":
    send_news()
