#python bot.py
from aiogram import Router, types
from aiogram.filters import Command
import storage

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для заучивания песен.\n"
        "Доступные команды:\n"
        "/add_song - добавить песню\n"
        "/list_songs - список песен\n"
        "/get_audio - вывод аудиофайла по ID\n"
        "/get_by_genre - вывод всех песен одного жанра\n"
        "/get_text - вывод текста песни\n"
        "/learn - режим построчного вывода текста\n"
        "/search - ищет песни, в которых есть все слова перечисленные после данной команды\n"
        "/cancel - отменить текущее действие"
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message):
    await message.answer("")


@router.message(Command("list_songs"))
async def cmd_list_songs(message: types.Message):
    data = storage.load_songs()
    if not data["songs"]:
        await message.answer("нет добавленных песен.")
        return

    songs_list = []
    for song in data["songs"]:
        songs_list.append(f"{song['id']}: {song['title']} ({song['genre']})")

    response = "Список песен:\n" + "\n".join(songs_list)
    await message.answer(response)