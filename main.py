import os
import requests
from datetime import datetime, timedelta

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def send_news():
    print("🔍 Pobieram newsy...")

    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    data = requests.get(url, timeout=20).json()

    now = datetime.utcnow()
    jutro = now + timedelta(days=1)

    znalezione = []

    for event in data:
        waluta = event.get("country", "")
        tytul = event.get("title", "")
        data_raw = event.get("date", "")
        impact = event.get("impact", "")
        forecast = event.get("forecast", "brak")
        previous = event.get("previous", "brak")

        if waluta not in ["USD", "EUR"]:
            continue

        if impact != "High":
            continue

        try:
            event_time = datetime.fromisoformat(data_raw.replace("Z", ""))
        except:
            continue

        if not (now <= event_time <= jutro):
            continue

        znalezione.append(
            f"📌 **{waluta} - {tytul}**\n"
            f"📅 {event_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"📈 Prognoza: {forecast}\n"
            f"📉 Poprzedni: {previous}\n"
            f"🔥 Wpływ: WYSOKI"
        )

    if not znalezione:
        print("❌ API nic nie zwróciło")
        return

    embed = {
        "title": "📰 Najważniejsze newsy ekonomiczne (24h)",
        "description": "\n\n".join(znalezione[:5]),
        "color": 16711680
    }

    response = requests.post(
        WEBHOOK_URL,
        json={"embeds": [embed]},
        timeout=10
    )

    print("📢 Discord status:", response.status_code)


if __name__ == "__main__":
    send_news()
