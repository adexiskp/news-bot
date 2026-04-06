import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def send_news():
    print("🔍 Wysyłam przykładowe newsy...")

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    embed = {
        "title": "📰 Aktualizacja newsów ekonomicznych",
        "description": (
            f"📌 **USD - Non Farm Payrolls**\n"
            f"📅 Data: {now}\n"
            f"📈 Prognoza: 180K\n"
            f"📉 Poprzedni: 151K\n"
            f"🔥 Wpływ: WYSOKI\n\n"

            f"📌 **USD - CPI m/m**\n"
            f"📅 Data: {now}\n"
            f"📈 Prognoza: 0.3%\n"
            f"📉 Poprzedni: 0.2%\n"
            f"🔥 Wpływ: WYSOKI"
        ),
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
