from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot('5994486631:AAFyPqSDTC6ydxZSQRwxXVjKzBkyDiAsZCU')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

admin_id = 716532569
admin_id1 = 716532569
admin_id2 = 716532569
admin_id3 = 716532569

class UserConversation(StatesGroup):
    start = State()
    category = State()
    branch = State()
    object = State()
    number_phone_or_email = State()
    question = State()


@dp.message_handler(commands=['start'])
async def main(message):
    await UserConversation.start.set()
    await message.answer(f'Здравствуйте, пожалуйста, представьтесь! (Например: Иванов Иван)')


@dp.message_handler(state=UserConversation.start)
async def handle_start(message: types.Message, state: FSMContext):
    await state.update_data(firstname_lastname_info=message.text)
    await UserConversation.next()
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton('Проживание', callback_data='Проживание')
    button2 = types.InlineKeyboardButton('Питание', callback_data='Питание')
    button3 = types.InlineKeyboardButton('СИЗ', callback_data='СИЗ')
    markup.add(button1, button2, button3)
    await message.answer('Выберете категорию по которой у Вас вопрос:', reply_markup=markup)



@dp.callback_query_handler(state=UserConversation.category)
async def callback_category(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(user_category=call.data)
    await UserConversation.next()

    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Санкт-Петербургское УТТиСТ', callback_data='Санкт-Петербургское УТТиСТ')
    button2 = types.InlineKeyboardButton('Уренгойское УИРС', callback_data='Уренгойское УИРС')
    button3 = types.InlineKeyboardButton('Надымское УИРС', callback_data='Надымское УИРС')
    button4 = types.InlineKeyboardButton('Ноябрьское УИРС', callback_data='Ноябрьское УИРС')
    button5 = types.InlineKeyboardButton('Оренбургское УИРС', callback_data='Оренбургское УИРС')
    button6 = types.InlineKeyboardButton('Астраханское УИРС', callback_data='Астраханское УИРС')
    markup.add(button1, button2, button3, button4, button5, button6)
    await call.message.answer('Спасибо! Выберете Ваш филиал:', reply_markup=markup)
    await call.message.delete()  # Удаляем сообщение с кнопками категорий


@dp.callback_query_handler(state=UserConversation.branch)
async def callback_branch(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(user_branch=call.data)
    await UserConversation.next()
    await call.message.answer('Укажите производственный объект/проект/офис')
    await call.message.delete()  # Удаляем сообщение с кнопками категорий


@dp.message_handler(state=UserConversation.object)
async def handle_object(message: types.Message, state: FSMContext):
    await state.update_data(user_object=message.text)
    await UserConversation.next()
    await message.answer('Теперь задайте свой вопрос!')


@dp.message_handler(state=UserConversation.number_phone_or_email)
async def handle_number_phone(message: types.Message, state: FSMContext):
    await state.update_data(user_number_phone_or_email=message.text)
    await UserConversation.next()
    await message.answer('Пожалуйста, укажите Ваш контакт для обратной связи (email/телефон')

def get_admin_id(category: str) -> int:
    if category == 'Проживание':
        return admin_id1  # ID первого администратора
    elif category == 'Питание':
        return admin_id2  # ID второго администратора
    elif category == 'СИЗ':
        return admin_id3  # ID третьего администратора
    else:
        return admin_id  # ID администратора по умолчанию

@dp.message_handler(state=UserConversation.question)
async def handle_exit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_info = f'id Пользователя: {message.from_user.id}\n'
        user_info += f'Категория: {data["user_category"]}\n'
        user_info += f'Филиал: {data["user_branch"]}\n'
        user_info += f'Объект: {data["user_object"]}\n'
        user_info += f'ФИО заявителя: {data["firstname_lastname_info"]}\n'
        user_message = f'Обращение: {data["user_number_phone_or_email"]}\n'
        user_info += f'Контакты: {message.text}'

        admin_message = f'Новое сообщение от пользователя:\n\n{user_info}\n{user_message}'
        await bot.send_message(chat_id=get_admin_id(data["user_category"]), text=admin_message)

    await state.finish()
    await message.answer('Спасибо! Ваш вопрос был отправлен на рассмотрение!')



@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    await message.answer('Пожалуйста, используйте команду /start для начала диалога.')


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
