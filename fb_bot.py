import requests
import time
from bs4 import BeautifulSoup

# Facebook page URL (mobile version for easier scraping)
FACEBOOK_PAGE = "https://m.facebook.com/leizlann.francisco"

# Discord webhook URL (exposed)
WEBHOOK_URL = "https://discord.com/api/webhooks/1481594202583466004/EqTx7cemODf2Lr3S0zh1nsljx2niKcwePX11mkg8huta5LRM-GreuENtQ5NfQpCW5tdY"

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

last_post = None  # Tracks the last detected post


def get_latest_post():
    """Scrapes the Facebook page and returns the latest post URL and text."""
    try:
        r = requests.get(FACEBOOK_PAGE, headers=headers, timeout=10)
        r.raise_for_status()  # Raise error if request fails
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
    """Sends the post to Discord via webhook."""
    try:
        message = {
            "content": f"📢 **New Facebook Post**\n\n{text}\n\n{post_url}"
        }
        requests.post(WEBHOOK_URL, json=message, timeout=10)
    except requests.RequestException as e:
        print("Failed to send to Discord:", e)


# Main loop — runs indefinitely
while True:
    try:
        post_url, text = get_latest_post()

        if post_url and post_url != last_post:
            last_post = post_url
            send_to_discord(post_url, text)
            print("New post detected:", post_url)

        time.sleep(20)  # Check every 20 seconds

    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(60)  # Wait a minute if something unexpected happens
