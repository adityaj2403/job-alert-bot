import os
import requests
from bs4 import BeautifulSoup

# GitHub Secrets se tokens lena
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.sarkariresult.com/latestjob/"
SEEN_JOBS_FILE = "seen_jobs.txt"


def load_seen_jobs():
  if not os.path.exists(SEEN_JOBS_FILE):
    return set()
  with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as f:
    return set(line.strip() for line in f if line.strip())


def save_seen_job(job_title):
  with open(SEEN_JOBS_FILE, "a", encoding="utf-8") as f:
    f.write(job_title + "\n")


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
  print("Checking for ITI / Technical jobs...")
  seen_jobs = load_seen_jobs()

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }

  try:
    response = requests.get(URL, headers=headers, timeout=15)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # Sabhi links fetch karna
    post_links = soup.find_all("a")

    new_jobs_found = 0

    # Extended keywords list taaki koi job na choote
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
        "loco pilot",
        "alp",
    ]

    for link in post_links:
      title = link.get_text().strip()
      href = link.get("href", "")

      if not title or not href.startswith("http"):
        continue

      # Title check
      if any(kw in title.lower() for kw in keywords):
        if title not in seen_jobs:
          message = (
              f"🚨 *NEW ITI / TECHNICAL JOB ALERT!* 🚨\n\n"
              f"📌 *Post:* {title}\n\n"
              f"🔗 [Apply / Details Here]({href})"
          )
          send_telegram_message(message)
          save_seen_job(title)
          seen_jobs.add(title)
          new_jobs_found += 1
          print(f"Sent alert for: {title}")

    if new_jobs_found == 0:
      print("No new matching jobs found right now.")
    else:
      print(f"Found and sent {new_jobs_found} job alerts!")

  except Exception as e:
    print("Error scraping jobs:", e)


if __name__ == "__main__":
  if not BOT_TOKEN or not CHAT_ID:
    print("Error: Secrets are missing!")
  else:
    check_for_jobs()
      
