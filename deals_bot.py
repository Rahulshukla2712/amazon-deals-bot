import time
import telebot
import requests
from bs4 import BeautifulSoup

# === CONFIGURATION ===
BOT_TOKEN = "8438763908:AAE_8sPvcjfAOIM4tinPY4H7KtR1GlYnuWQ"
CHANNEL_USERNAME = "-1003861409737" 
TRACKING_ID = "rahulshukla02-21"
INTERVAL = 900 # 15 ????

# (????????) ??? ?? Make.com ?? ????? ?? ??? ???, ?? ???? Webhook URL ???? ?????
WHATSAPP_WEBHOOK_URL = "YOUR_MAKE_WEBHOOK_URL_HERE" 

bot = telebot.TeleBot(BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_amazon_deals():
    print("Amazon se fresh deals dhoodh rahe hain...")
    url = "https://amazon.in"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return 
        soup = BeautifulSoup(response.content, "html.parser")
        deals = []
        items = soup.find_all("div", {"id": "gridItemRoot"}) or soup.find_all("div", {"class": "p13n-grid-content"})
        for item in items:
            try:
                title_tag = item.find("div", {"class": "_cDEE_p_zg-factsheet-title_395oF"}) or item.find("span")
                title = title_tag.text.strip() if title_tag else "Mega Discount Deal"
                link_tag = item.find("a", {"class": "a-link-normal"})
                if not link_tag or 'href' not in link_tag.attrs:
                    continue
                raw_link = link_tag['href']
                if not raw_link.startswith("http"):
                    raw_link = "https://amazon.in" + raw_link
                clean_url = raw_link.split("?")
                affiliate_link = f"{clean_url}?tag={TRACKING_ID}"
                deals.append({"title": title[:80] + "...", "link": affiliate_link})
            except Exception:
                continue
        return deals
    except Exception:
        return 

def send_to_whatsapp(message_text):
    if WHATSAPP_WEBHOOK_URL and "YOUR_MAKE" not in WHATSAPP_WEBHOOK_URL:
        try:
            requests.post(WHATSAPP_WEBHOOK_URL, json={"message": message_text}, timeout=10)
            print("-> Success: WhatsApp channel par deal bhej di gayi!")
        except Exception as e:
            print(f"WhatsApp par send nahi ho paya: {e}")

def start_bot():
    print("Telegram + WhatsApp Deals Bot active ho chuka hai...")
    
    welcome_msg = "?? *Amazon Deals Automation Engine Active!*\n\nNaye bot aur Chat ID ke sath connection 100% jud chuka hai."
    try:
        bot.send_message(CHANNEL_USERNAME, welcome_msg, parse_mode="Markdown")
        print("-> Success: Test message Telegram channel me post ho gaya hai!")
        send_to_whatsapp(welcome_msg)
    except Exception as token_e:
        print(f"-> Critical Error: {token_e}")
        return

    posted_links = set()
    while True:
        deals = get_amazon_deals()
        if deals:
            posted_any = False
            for deal in deals:
                if deal['link'] not in posted_links:
                    message = f"?? *TODAY'S BEST AMAZON DEAL* ??\n\n?? *{deal['title']}*\n\n?? *Buy Now:* {deal['link']}\n\n??????????????????\n?? Join our channel for more amazing loot offers!"
                    try:
                        # 1. ????????? ?? ????? ????
                        bot.send_message(CHANNEL_USERNAME, message, parse_mode="Markdown")
                        print(f"Telegram Posted: {deal['title']}")
                        
                        # 2. ??????? ?? ????? ????
                        send_to_whatsapp(message)
                        
                        posted_links.add(deal['link'])
                        posted_any = True
                        break 
                    except Exception as e:
                        print(f"Post nahi ho paya: {e}")
            if not posted_any:
                print("Koi nayi unique deal nahi mili.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    start_bot()
