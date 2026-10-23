import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.sarkariresult.com/latestjobs.php"
SEEN_JOBS_FILE = "seen_jobs.txt"

def load_seen_jobs():
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()
    with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_seen_job(job_title):
    with open(SEEN_JOBS_FILE, "a", encoding="utf-8") as f:
        f.write(job_title + "\n")

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(telegram_url, data=payload)

def check_new_jobs():
    seen_jobs = load_seen_jobs()
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_list = soup.find_all("li")

    for job in job_list:
        a_tag = job.find("a")
        if a_tag:
            title = a_tag.text.strip()
            link = a_tag["href"]
            if title not in seen_jobs:
                keywords = ["railway", "rrb", "iti", "technician", "alp", "ssc", "apprentice"]
                if any(kw in title.lower() for kw in keywords):
                    msg = f"🚨 *Nayi Government Job Update!*\n\n📌 *Post:* {title}\n🔗 *Link:* {link}"
                    send_telegram_message(msg)
                    save_seen_job(title)

if __name__ == "__main__":
    check_new_jobs()
  
