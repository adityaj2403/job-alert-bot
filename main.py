import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.sarkariresult.com/latestjob/"


def send_telegram_message(text):
  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": CHAT_ID,
      "text": text,
      "parse_mode": "Markdown",
      "disable_web_page_preview": False,
  }
  try:
    requests.post(url, json=payload)
  except Exception as e:
    print("Error sending message:", e)


def check_for_jobs():
  print("Fetching Sarkari Result jobs...")

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }

  try:
    response = requests.get(URL, headers=headers, timeout=15)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # Pure page se sabhi <a> tags dhundho
    links = soup.find_all("a")
    print(f"Total links found on page: {len(links)}")

    sent_count = 0

    # Extended keywords (chote-bade letters dono handle honge)
    keywords = [
        "iti",
        "technician",
        "mechanic",
        "apprentice",
        "electronic",
        "railway",
        "rrb",
        "isro",
        "drdo",
        "trade",
        "loco",
        "alp",
        "recruitment",
        "form",
        "online",
        "admit",
        "apply",
    ]

    for link in links:
      title = link.get_text().strip()
      href = link.get("href", "")

      if not title or len(title) < 5 or not href.startswith("http"):
        continue

      # Title match check
      if any(kw in title.lower() for kw in keywords):
        message = (
            f"🚨 *JOB ALERT!* 🚨\n\n📌 *Post:* {title}\n\n🔗 [Apply Here]({href})"
        )
        send_telegram_message(message)
        print(f"MATCH FOUND & SENT: {title}")
        sent_count += 1
        if sent_count >= 5:  # Test ke liye maximum 5 messages bheje
          break

    if sent_count == 0:
      # Agar abhi bhi koi keyword match na ho, toh top 3 jobs test ke liye bhej do
      send_telegram_message(
          "ℹ️ *System Test:* Scraper working, but no exact ITI keyword"
          " match found on front page right now."
      )
      print("No exact match found, sent info message.")

  except Exception as e:
    print("Error scraping jobs:", e)


if __name__ == "__main__":
  if not BOT_TOKEN or not CHAT_ID:
    print("Error: Secrets missing!")
  else:
    check_for_jobs()
    
