import os
import requests
import schedule
import time
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TLUMACZENIA = {
    "JOLTS Job Openings": "Liczba ofert pracy JOLTS",
    "Non Farm Payrolls": "Payrollsy (NFP)",
    "Consumer Price Index": "Inflacja CPI",
    "Federal Reserve Interest Rate Decision": "Decyzja stóp procentowych FED",
    "GDP Growth Rate": "Wzrost PKB",
    "Unemployment Rate": "Stopa bezrobocia",
    "Retail Sales": "Sprzedaż detaliczna",
    "Producer Price Index": "Inflacja PPI",
    "FOMC Meeting": "Posiedzenie FOMC",
    "Fed Interest Rate Decision": "Decyzja stóp FED",
    "Powell Speech": "Wystąpienie Powella"
}

KLUCZOWE = [
    "JOLTS",
    "Payrolls",
    "CPI",
    "Fed",
    "FOMC",
    "Powell",
    "Inflation",
    "Interest Rate"
]

def tlumacz_event(nazwa):
    for ang, pl in TLUMACZENIA.items():
        if ang.lower() in nazwa.lower():
            return pl
    return nazwa

def czy_kluczowy_news(nazwa):
    for slowo in KLUCZOWE:
        if slowo.lower() in nazwa.lower():
            return True
    return False

def get_news():
    url = "https://api.tradingeconomics.com/calendar?c=guest:guest&f=json"
    response = requests.get(url)
    data = response.json()

    for event in data[:50]:
        waluta = event.get("Currency", "")
        waznosc = event.get("Importance", 0)
        nazwa_raw = event.get("Event", "")

        if waluta == "USD" and str(waznosc) == "3":
            nazwa = tlumacz_event(nazwa_raw)

            czas_raw = event.get("Date", "")
            try:
                czas = datetime.fromisoformat(czas_raw.replace("Z", ""))
                godzina = czas.strftime("%d.%m.%Y • %H:%M")
            except:
                godzina = czas_raw

            embed = {
                "title": "🚨 KLUCZOWY NEWS DLA NASDAQ / GOLD",
                "description": (
                    f"📰 **{nazwa}**\n\n"
                    f"🌍 **Kraj:** USA\n"
                    f"📊 **Rynek:** NASDAQ / GOLD\n"
                    f"🕒 **Godzina:** {godzina}\n"
                    f"🔴 **Wpływ:** Wysoki\n"
                    f"📈 **Efekt:** Możliwa silna zmienność na US100 i XAUUSD"
                ),
                "color": 16753920,
                "footer": {
                    "text": "Automatyczny bot newsów • NASDAQ / GOLD"
                }
            }

requests.post(WEBHOOK_URL, json={"embeds": [embed]})
print("🚀 Wysłano premium news NASDAQ/GOLD")

schedule.every().day.at("14:20").do(get_news)
schedule.every().day.at("15:50").do(get_news)

while True:
    schedule.run_pending()
    time.sleep(30)
   
