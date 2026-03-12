import requests
import time
from bs4 import BeautifulSoup

FACEBOOK_PAGE = "https://m.facebook.com/leizlann.francisco"
WEBHOOK_URL = "https://discord.com/api/webhooks/1481594202583466004/EqTx7cemODf2Lr3S0zh1nsljx2niKcwePX11mkg8huta5LRM-GreuENtQ5NfQpCW5tdY"

headers = {
    "User-Agent": "Mozilla/5.0"
}

last_post = None


def get_latest_post():
    r = requests.get(FACEBOOK_PAGE, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")

        if href and "/story.php" in href:
            post_url = "https://facebook.com" + href
            text = link.get_text().strip()

            return post_url, text

    return None, None


def send_to_discord(post_url, text):

    message = {
        "content": f"📢 **New Facebook Post**\n\n{text}\n\n{post_url}"
    }

    requests.post(WEBHOOK_URL, json=message)


while True:
    try:
        post_url, text = get_latest_post()

        if post_url and post_url != last_post:
            last_post = post_url
            send_to_discord(post_url, text)
            print("New post:", post_url)

        time.sleep(20)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)