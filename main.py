import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from instaloader import Instaloader, Profile

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class ProfileDownloader:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.ig = Instaloader()

    @staticmethod
    async def start(update: Update, context: CallbackContext):
        text1 = 'Insta Profile Downloader Started\n'
        text2 = 'This Bot Developed By Satya Ajay\n'
        text = text1 + text2
        await update.message.reply_text(text)

    @staticmethod
    async def help(update: Update, context: CallbackContext):
        text = 'I Am A Bot To Download Insta Profile Pictures\n'
        await update.message.reply_text(text)

    async def download_profile(self, update: Update, context: CallbackContext):
        query = update.message.text.strip()
        chat_id = update.message.chat_id
        await update.message.reply_text('Downloading...')

        try:
            user = Profile.from_username(self.ig.context, query)
            await context.bot.send_photo(chat_id, user.profile_pic_url)
        except Exception as e:
            logger.error(f"Error downloading profile: {e}")
            await update.message.reply_text('Error fetching profile. Make sure the username is correct.')

    @staticmethod
    async def error_handler(update: object, context: CallbackContext):
        logger.error(f"Update {update} caused error {context.error}")
        await context.bot.send_message(update.effective_chat.id, 'An error occurred, please try again!')

    def run_bot(self):
        app = Application.builder().token(self.api_token).build()
        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('help', self.help))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.download_profile))
        app.add_error_handler(self.error_handler)

        logger.info("Bot started!")
        app.run_polling()


if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")
    bot = ProfileDownloader(TOKEN)
    bot.run_bot()
