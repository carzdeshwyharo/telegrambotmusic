#python bot.py
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import storage

router = Router()


@router.message(Command("learn"))
async def cmd_learn(message: types.Message):
    try:
        song_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("Использование: /learn <ID песни>")
        return

    data = storage.load_songs()
    song = next((s for s in data["songs"] if s["id"] == song_id), None)

    if not song:
        await message.answer("Песня не найдена.")
        return

    lines = [line.strip() for line in song['text'].split('\n')]

    if not lines:
        await message.answer("У этой песни нет текста.")
        return

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="..........",
        callback_data=f"learn:{song_id}:1"
    ))

    await message.answer(
        f"Учим песню: {song['title']}\n\n"
        f"{lines[0]}",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("learn:"))
async def process_learn(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    song_id = int(parts[1])
    current_line = int(parts[2])

    data = storage.load_songs()
    song = next((s for s in data["songs"] if s["id"] == song_id), None)

    if not song:
        await callback.answer("Песня не найдена.")
        return

    lines = [line.strip() for line in song['text'].split('\n')]

    if current_line >= len(lines):
        await callback.message.edit_text(
            f"Конец песни\n"
            f"Для повторения используйте /learn {song_id}"
        )
        await callback.answer()
        return

    start_index = max(0, current_line - 2)
    end_index = current_line + 1

    lines_to_show = lines[start_index:end_index]

    message_text = f"{song['title']}\n\n" + "\n".join(lines_to_show)

    builder = InlineKeyboardBuilder()

    if current_line + 1 < len(lines):
        builder.add(types.InlineKeyboardButton(
            text="..........",
            callback_data=f"learn:{song_id}:{current_line + 1}"
        ))
    else:
        builder.add(types.InlineKeyboardButton(
            text="Завершить",
            callback_data=f"learn:{song_id}:{current_line + 1}"
        ))

    await callback.message.edit_text(
        message_text,
        reply_markup=builder.as_markup()
    )
    await callback.answer()