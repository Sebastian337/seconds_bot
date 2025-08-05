from decouple import config
import ptbot
from pytimeparse import parse


TG_TOKEN = config('TG_TOKEN')
TG_CHAT_ID = config('TG_CHAT_ID')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def handle_message(bot, chat_id, text):
    seconds = parse(text)
    if seconds is None:
        bot.send_message(chat_id, "5s")
    message_id = bot.send_message(chat_id, f"Таймер запущен на {seconds} секунд\n{render_progressbar(seconds, 0)}")
    bot.create_countdown(
        seconds,
        lambda secs_left: notify_progress(bot, secs_left, chat_id, message_id, seconds)
    )
    
    bot.create_timer(
        seconds,
        lambda: notify(bot, chat_id)
    )


def notify_progress(bot, secs_left, chat_id, message_id, total):
    progress = total - secs_left
    progressbar = render_progressbar(total, progress)
    bot.update_message(chat_id, message_id, f"Осталось: {secs_left} секунд\n{progressbar}")


def notify(bot, chat_id):
    bot.send_message(chat_id, "Время вышло")


def main():
    bot = ptbot.Bot(config('TG_TOKEN'))
    bot.reply_on_message(lambda chat_id, text: handle_message(bot, chat_id, text))
    bot.run_bot()


if __name__ == '__main__':
    main()
