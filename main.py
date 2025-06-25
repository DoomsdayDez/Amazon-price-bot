import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = "7894155410:AAFrrNR9yb-7CwVV3Zu4NqRNLUpQ3U1L7Es"

def get_amazon_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for sel in ['#priceblock_ourprice', '#priceblock_dealprice', '#priceblock_saleprice']:
            tag = soup.select_one(sel)
            if tag:
                return tag.text.strip()
        return "Price not found."
    except Exception as e:
        return f"Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /price <Amazon URL> to get the price.")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please include a valid Amazon URL.")
        return
    url = context.args[0]
    price = get_amazon_price(url)
    await update.message.reply_text(f"Price: {price}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
