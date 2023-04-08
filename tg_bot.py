import logging
from telegram.ext import Application
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from datetime import datetime
#from config impoprt BOT_TOKEN


proxy_url = "socks5://user:pass@host:port"

app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()

BOT_TOKEN = '5484392012:AAEX3XR-isqaEcO-gLaEVPIUPmWRrvMW4a0'
# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/site', '/time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("open", open_keyboard))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("equation", equation))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


async def equation(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text("You said: " + user_says)


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Off",
        reply_markup=ReplyKeyboardRemove()
    )


async def open_keyboard(update, context):
    await update.message.reply_text(
        "On",
        reply_markup=markup
    )


async def help(update, context):
    await update.message.reply_text(
        "Мои функции:"
        "/equation - решаю уравнения(пример записи"
        "/text_from_p - сканирую текст с картинки и отправляю вам"
        "/close - закрыть функциональнок меню"
        "/open - открыть функциональнок меню")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def time(update, context):
    now = datetime.now()
    current_datetime = now.strftime("%D-%H:%M:%S")
    await update.message.reply_text(
        current_datetime
    )


async def start(update, context):
    await update.message.reply_text(
        "Привет! Я твой новый бот-помощник в обучении. Чтобы узнать больше пропиши команду: /help",
        reply_markup=markup
    )


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
