from telegram import Update
from telegram.ext import ContextTypes

import bot.const as c
import bot.database as db
from bot.utils import logged_in, is_manager, events_list_full, not_group, \
    can_see_players
from bot.utils.event_handling.dashboard import create_dashboard_announce, \
    create_dashboard_admin


@not_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.message.from_user.id
    user = await db.get_user(tg_id=tg_id)
    if user is None:
        username = update.message.from_user.username
        if username is not None:
            await db.create_user(
                tg_id=tg_id, username=username,
                first_name=None, last_name=None
            )
            await update.message.reply_text("Добрый день")
        else:
            await update.message.reply_text(
                "Юзернейм не определен. Установите юзернейм в настройках пользователя, чтобы зарегистрироваться в боте"
            )
    else:
        await update.message.reply_text("Добрый день")


@not_group
@logged_in
async def my_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = await db.get_events(telegram_id=update.message.from_user.id)
    show_players = await can_see_players(update.message.from_user.id, context)
    await update.message.reply_text(  # apply_markdown(
        "\n\n".join([
            f"Вы записаны на следующие игры: ",
            *[event.other_event_info(show_players=show_players)
              for event in events]
        ])  # ), parse_mode="MarkdownV2"
    )


async def events_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events_text = await events_list_full(admin=False)
    await update.message.reply_text(events_text, parse_mode="html")


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
    await create_dashboard_announce(context=context)
    await create_dashboard_admin(context=context)


@not_group
@is_manager
async def show_event_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    normal = await db.get_event_count(at_least_one=True)
    zero = await db.get_event_count(at_least_one=False)
    message = "\n".join([
        "Количество посещений людей: ",
        *[f"@{username} - {count}" for username, count in normal],
        "", "Ни одного посещения:",
        *[f"@{username}" for username, count in zero],
        "", f"Удалить тех, кто не ходит - /{c.DELETE_ABSENT}"
    ])
    await update.message.reply_text(message)


@not_group
@is_manager
async def delete_absent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await db.delete_zero()
    await update.message.reply_text("Сделано")


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
