import traceback

from telegram import Update
from telegram.ext import ContextTypes

import bot.const as c
import bot.database as db
from bot.utils import logged_in, is_manager, action_button, send_to_announces, \
    events_list_full, send_to_admin
from bot.utils.auth import not_group
from bot.utils.mailing import create_dashboard


@not_group
@logged_in
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await db.get_user(tg_id=update.message.from_user.id)
    await update.message.reply_text(
        f"Добрый день, {user.first_name}, {c.SIGN_UP_TEXT}"
    )


@not_group
@logged_in
async def my_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = await db.get_events(username=update.message.from_user.username)
    await update.message.reply_text(  # apply_markdown(
        "\n\n".join([
            f"Вы записаны на следующие игры: ",
            *[event.other_event_info() for event in events]
        ])  # ), parse_mode="MarkdownV2"
    )


async def events_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events_text = await events_list_full(admin=False)
    print(events_text)
    try:
        await update.message.reply_text(events_text, parse_mode="html")

    except Exception as E:
        traceback.print_exc()


async def games_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = await db.get_games(linked=True)
    await update.message.reply_text(
        "\n".join([
            f"Список наших игр\: ",
            *[game_link for game_link, game_id in games]
        ]), parse_mode="MarkdownV2", disable_web_page_preview=True
    )


@not_group
@is_manager
async def send_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_dashboard(context=context)


async def help_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.chat_id)
    user_commands = [
        f"/{c.START_REGISTRATION} - регистрация",
        f"/{c.GAME_LIST} - список игр",
        f"/{c.EVENTS} - список ближайших игр",
        f"/{c.SIGN_UP} - записаться на игру",
        f"/{c.CREATE_GAME} - создать игру",
        f"/{c.MY_GAMES} - мои игры",
        f"/{c.LEAVE} - покинуть игру",
        f"/help - справка",
    ]
    admin_commands = [
        f'\n{"-" * 10}Админ{"-" * 10}',
        f"/{c.DASHBOARD} - отправить в чат ближайшие игры",
    ]
    if await db.user_is_manager(tg_id=update.message.from_user.id):
        user_commands.extend(admin_commands)

    await update.message.reply_text("\n".join(user_commands))
