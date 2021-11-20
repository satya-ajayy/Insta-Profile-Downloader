import random
from telegram.ext import *
from traceback import format_exc, TracebackException
from instaloader import Instaloader, Profile


class ProfileDownloader:
    def __init__(self, API):
        print('Bot Started!')
        self.API = API

    def Handler(self, update, context):
        ig = Instaloader()
        query = update.message.text
        update.message.reply_text('Downloading...')
        chat_id = update.message.chat_id
        try:
            user = Profile.from_username(ig.context, query)
            context.bot.send_photo(chat_id, user.profile_pic_url)
        except TracebackException:
            print(format_exc())

    @staticmethod
    def StartCommand(update, context):
        if not context.error:
            text1 = 'DP Downloader Bot Started\n\n'
            text2 = '(Bot Designer : R.Satya Ajay\n'
            text3 = 'Contact No : +91 86XXXXX607)'
            text = text1 + text2 + text3
            update.message.reply_text(text)
        else:
            print(f'Update {update} caused Error {context.error}')

    @staticmethod
    def HelpCommand(update, context):
        if not context.error:
            text1 = 'I Am A Bot To Download Profiles\n\n'
            text2 = 'You can control me by sending Insta Usernames'
            text3 = '(Send Some Usernames To Try)'
            text = text1 + text2 + text3
            update.message.reply_text(text)
        else:
            print(f'Update {update} caused Error {context.error}')

    @staticmethod
    def Error(update, context):
        update.message.reply_text('Try again 😕😕! Check the username correctly')
        print(f'Update {update} caused Error {context.error}')

    def RunBot(self):
        updater = Updater(self.API, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', self.StartCommand))
        dp.add_handler(CommandHandler('help', self.HelpCommand))
        dp.add_handler(MessageHandler(Filters.text, self.Handler))
        dp.add_error_handler(self.Error)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    Token = '2068225002:AAEy-VCaH_S4IeKz42Qtcqh_RBaOPQUyUMQ'
    mybot = ProfileDownloader(Token)
    mybot.RunBot()
