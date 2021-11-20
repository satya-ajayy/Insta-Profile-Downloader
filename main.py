import random
from telegram.ext import *
from traceback import format_exc, TracebackException
from instaloader import Instaloader, Profile


class ProfileDownloader:
    def __init__(self, API):
        print('Bot Started!')
        self.API = API

    @staticmethod
    def SampleReponses(text):
        user_msg = text.lower()
        if user_msg in ['hello', 'hola', 'hii', 'hi']:
            response = ['Hey! I can Download Insta Dp For You',
                        'Hello! Give Me Any User Name',
                        'Hey Hii! Give Me Any User Name'][random.randrange(3)]
            return response
        elif user_msg in ['who are you', 'who are you?']:
            response = ['I Am a Bot Designed By Ajay',
                        'I Am A Insta Profile Downloader Bot'][random.randrange(2)]
            return response
        elif user_msg in ['who designed you?', 'who is your creator?']:
            response = ['I Am Designed By Satya Ajay',
                        'Satya Ajay'][random.randrange(2)]
            return response
        elif user_msg in ['bye', 'byeee', 'see u', 'ttyl', 'tata']:
            response = ['Bye Have A Nyc Day Ahead', 'Take Care Byeee',
                        'See You Soon', 'Catch U Later Byeee',
                        'Nice Talking To You Bye'][random.randrange(5)]
            return response
        else:
            return -1

    def Handler(self, update, context):
        ig = Instaloader()
        query = update.message.text
        response = self.SampleReponses(query)
        if response == -1:
            msg = update.message.reply_text('Downloading...')
            chat_id = update.message.chat_id
            try:
                user = Profile.from_username(ig.context, query)
                context.bot.send_photo(chat_id, user.profile_pic_url)
            except TracebackException:
                print(format_exc())
                msg.edit_text('Try again 😕😕! Check the username correctly')
        else:
            update.message.reply_text(response)

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
            text3 = '(Send Some Usernames to Try)'
            text = text1 + text2 + text3
            update.message.reply_text(text)
        else:
            print(f'Update {update} caused Error {context.error}')

    @staticmethod
    def Error(update, context):
        update.message.reply_text('⚠ Unable To Fetch Data')
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
