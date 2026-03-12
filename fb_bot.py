import requests
import time
from bs4 import BeautifulSoup
from flask import Flask
import threading

# ---------- CONFIG ----------
FACEBOOK_PAGE = "https://m.facebook.com/leizlann.francisco"
WEBHOOK_URL = "https://discord.com/api/webhooks/1481594202583466004/EqTx7cemODf2Lr3S0zh1nsljx2niKcwePX11mkg8huta5LRM-GreuENtQ5NfQpCW5tdY"
CHECK_INTERVAL = 20  # seconds between checks
# ----------------------------

headers = {"User-Agent": "Mozilla/5.0"}
last_post = None  # Tracks last detected post

# ---------- FLASK KEEP-ALIVE ----------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Run Flask server in a separate thread
threading.Thread(target=run_flask).start()
# --------------------------------------

def get_latest_post():
    """Scrape the Facebook page and return the latest post URL and text."""
    try:
        r = requests.get(FACEBOOK_PAGE, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print("Failed to fetch Facebook page:", e)
        return None, None

    soup = BeautifulSoup(r.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "/story.php" in href:
            post_url = "https://facebook.com" + href
            text = link.get_text().strip()
            return post_url, text

    return None, None

def send_to_discord(post_url, text):
    """Send a post to Discord via webhook."""
    try:
        message = {"content": f"📢 **New Facebook Post**\n\n{text}\n\n{post_url}"}
        requests.post(WEBHOOK_URL, json=message, timeout=10)
    except requests.RequestException as e:
        print("Failed to send to Discord:", e)

# ---------- MAIN LOOP ----------
while True:
    try:
        post_url, text = get_latest_post()
        if post_url and post_url != last_post:
            last_post = post_url
            send_to_discord(post_url, text)
            print("New post detected:", post_url)
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(60)
