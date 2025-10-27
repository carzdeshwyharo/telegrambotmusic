#python bot.py
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import storage

router = Router()


class AddSong(StatesGroup):
    waiting_for_audio = State()
    waiting_for_genre = State()
    waiting_for_title = State()
    waiting_for_text = State()


@router.message(Command("add_song"))
async def cmd_add_song(message: types.Message, state: FSMContext):
    await message.answer(
        "Добавить новую песню!\n"
        "Отправь аудиофайл с песней"
    )
    await state.set_state(AddSong.waiting_for_audio)


@router.message(AddSong.waiting_for_audio, F.audio)
async def process_audio(message: types.Message, state: FSMContext):
    audio_id = message.audio.file_id
    await state.update_data(audio_id=audio_id)
    await message.answer("отправь жанр этой песни")
    await state.set_state(AddSong.waiting_for_genre)


@router.message(AddSong.waiting_for_genre, F.text)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("отправь название песни")
    await state.set_state(AddSong.waiting_for_title)


@router.message(AddSong.waiting_for_title, F.text)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("отправь текст песни")
    await state.set_state(AddSong.waiting_for_text)


@router.message(AddSong.waiting_for_text, F.text)
async def process_text(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    song_data = {
        "audio_id": user_data['audio_id'],
        "genre": user_data['genre'],
        "title": user_data['title'],
        "text": message.text
    }

    song_id = storage.add_song(song_data)

    await message.answer(f"Песня добавлена! ID: {song_id}")
    await state.clear()