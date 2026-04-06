import os
import requests
from datetime import datetime, timedelta

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


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

        for event in data:
            title = event.get("Event", "")
            date_raw = event.get("Date", "")
            forecast = event.get("Forecast", "brak")
            previous = event.get("Previous", "brak")

            try:
                event_time = datetime.fromisoformat(date_raw.replace("Z", ""))
            except:
                continue

            if not (now <= event_time <= next_7d):
                continue

            embed = {
                "title": "📢 Nadchodzący ważny news USD",
                "description": (
                    f"**{title}**\n"
                    f"📈 Prognoza: {forecast}\n"
                    f"📉 Poprzedni: {previous}"
                ),
            }

            requests.post(
                WEBHOOK_URL,
                json={"embeds": [embed]},
                timeout=10
            )

            print("📢 Wysłano:", title)
            break

    except Exception as e:
        print("❌ ERROR:", e)
        raise


if __name__ == "__main__":
    send_news()
