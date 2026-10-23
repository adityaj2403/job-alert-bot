import os
import requests

# GitHub Secrets se token aur chat id uthana
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram API Response:", response.text)
    except Exception as e:
        print("Error sending message:", e)

if __name__ == "__main__":
    print("Starting ITI Job Check script...")
    
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN or CHAT_ID is missing!")
    else:
        print("Bot tokens are present. Sending test notification...")
        send_telegram_message("🤖 ITI Job Alert Bot: Script successfully executed and connected!")
        
    print("Script finished execution.")
    
