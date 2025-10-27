#python bot.py
from aiogram import Router, types
from aiogram.filters import Command
import storage

router = Router()


@router.message(Command("get_audio"))
async def cmd_get_audio(message: types.Message):
    try:
        song_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("Использование: /get_audio <ID песни>")
        return

    data = storage.load_songs()
    song = next((s for s in data["songs"] if s["id"] == song_id), None)

    if not song:
        await message.answer("Песня с таким ID не найдена.")
        return

    await message.answer_audio(song["audio_id"])


@router.message(Command("get_by_genre"))
async def cmd_get_by_genre(message: types.Message):
    try:
        genre = message.text.split(maxsplit=1)[1].lower()
    except IndexError:
        await message.answer("Использование: /get_by_genre <жанр>")
        return

    data = storage.load_songs()
    songs_in_genre = [s for s in data["songs"] if s["genre"].lower() == genre]

    if not songs_in_genre:
        await message.answer(f"Песни в жанре '{genre}' не найдены.")
        return

    songs_list = []
    for song in songs_in_genre:
        songs_list.append(f"{song['id']}: {song['title']}")

    response = f"Песни в жанре {genre}:\n" + "\n".join(songs_list)
    await message.answer(response)


@router.message(Command("get_text"))
async def cmd_get_text(message: types.Message):
    try:
        song_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("Использование: /get_text <ID песни>")
        return

    data = storage.load_songs()
    song = next((s for s in data["songs"] if s["id"] == song_id), None)

    if not song:
        await message.answer("Песня с таким ID не найдена.")
        return

    await message.answer(f"Текст песни '{song['title']}':\n\n{song['text']}")


@router.message(Command("search"))
async def cmd_search(message: types.Message):
    try:
        search_words = message.text.split()[1:]
    except IndexError:
        await message.answer("Использование: /search <слова через пробел>")
        return

    if not search_words:
        await message.answer("Укажите слова для поиска через пробел")
        return

    data = storage.load_songs()
    found_songs = []

    for song in data["songs"]:
        search_text = f"{song['title']} {song['text']}".lower()

        if all(word.lower() in search_text for word in search_words):
            found_songs.append(song)

    if not found_songs:
        await message.answer(
            f"Песни со словами '{' '.join(search_words)}' не найдены.\n"
            f"Попробуйте изменить запрос."
        )
        return

    songs_list = []
    for song in found_songs:
        preview = get_text_preview(song['text'], search_words)
        songs_list.append(f"{song['id']}: {song['title']} ({song['genre']})\n{preview}")

    response = f"Найдено песен: {len(found_songs)}\n\n" + "\n\n".join(songs_list)

    if len(response) > 4000:
        parts = [response[i:i + 4000] for i in range(0, len(response), 4000)]
        for part in parts:
            await message.answer(part)
    else:
        await message.answer(response)


def get_text_preview(text, search_words, context_lines=2):
    lines = text.split('\n')
    preview_lines = []

    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(word.lower() in line_lower for word in search_words):
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)

            for j in range(start, end):
                if lines[j] not in preview_lines:
                    preview_lines.append(lines[j])

    preview = "\n".join(preview_lines)
    if len(preview) > 40:
        preview = preview[:40]

    return preview if preview else "Отрывок не найден"