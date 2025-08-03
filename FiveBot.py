import os
from dotenv import load_dotenv
import ptbot
from pytimeparse import parse

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
bot = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def start_countdown(chat_id, seconds):
    message_id = bot.send_message(chat_id, f"Осталось: {seconds} секунд\n{render_progressbar(seconds, 0)}")
    bot.create_countdown(
        seconds,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total=seconds
    )
    bot.create_timer(seconds, notify, chat_id=chat_id)


def handle_message(chat_id, text):
    seconds = parse(text)
    if seconds is None:
        bot.send_message(chat_id, "5s")
        return
    start_countdown(chat_id, seconds)


def notify_progress(secs_left, chat_id, message_id, total):
    progress = total - secs_left
    progressbar = render_progressbar(total, progress)
    bot.update_message(chat_id, message_id, f"Осталось: {secs_left} секунд\n{progressbar}")


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло") 


def main():
    bot.reply_on_message(handle_message)
    bot.run_bot()


if __name__ == '__main__':
    main()