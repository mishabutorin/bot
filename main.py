from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import db
import xml_generator as xg

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
    question = State()
    quit = State()


# Функция для отправки письма на почту с вложением XML-файла
def send_email_with_attachment(subject, attachment_path, photo_path):
    smtp_server = 'smtp.yandex.ru'  # Укажите адрес SMTP-сервера
    smtp_port = 587  # Укажите порт SMTP-сервера
    smtp_login = 'mushaspb@yandex.ru'  # Укажите адрес электронной почты отправителя
    smtp_password = ''  # Укажите пароль от электронной почты отправителя
    recipient = 'mushaspb@yandex.ru'  # Укажите адрес электронной почты получателя

    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = smtp_login
    msg['To'] = recipient
    msg['Subject'] = subject
    # msg.attach(MIMEText('plain'))

    # Добавление XML-файла в виде вложения
    with open(attachment_path, 'rb') as attachment_file:
        attachment = MIMEApplication(attachment_file.read(), _subtype='xml')
        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
        msg.attach(attachment)

    if photo_path:
        with open(photo_path, 'rb') as photo_file:
            photo_attachment = MIMEApplication(photo_file.read(), _subtype='jpg')
            photo_attachment.add_header('Content-Disposition', 'attachment', filename='photo.jpg')
            msg.attach(photo_attachment)

    # Отправка письма через SMTP-сервер
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_login, smtp_password)
        server.send_message(msg)


def get_admin_id(category: str) -> int:
    admin_mapping = {
        'Проживание': admin_id1,
        'Питание': admin_id2,
        'СИЗ': admin_id3
    }
    return admin_mapping.get(category, admin_id)


@dp.message_handler(commands=['start'])
async def start(message):
    await UserConversation.start.set()
    await message.answer(f'Пожалуйста, представьтесь! (Например: Иванов Иван)')


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

    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('УТТиСТ', callback_data='УТТиСТ')
    button2 = types.InlineKeyboardButton('Уренгойское УИРС', callback_data='Уренгойское УИРС')
    button3 = types.InlineKeyboardButton('Надымское УИРС', callback_data='Надымское УИРС')
    button4 = types.InlineKeyboardButton('Ноябрьское УИРС', callback_data='Ноябрьское УИРС')
    button5 = types.InlineKeyboardButton('Оренбургское УИРС', callback_data='Оренбургское УИРС')
    button6 = types.InlineKeyboardButton('Астраханское УИРС', callback_data='Астраханское УИРС')
    button7 = types.InlineKeyboardButton('Краснодарское УИРС', callback_data='Краснодарское УИРС')
    button8 = types.InlineKeyboardButton('Ямбургское УИРС', callback_data='Ямбургское УИРС')
    button9 = types.InlineKeyboardButton('Администрация СПб', callback_data='Администрация СПб')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
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
    await message.answer('Теперь задайте свой вопрос, при наличии прикрепите фото!')


@dp.message_handler(state=UserConversation.question, content_types=['text', 'photo'])
async def handle_question(message: types.Message, state: FSMContext):
    if message.caption and message.photo:  # если отправлены и текст и фото вместе
        # Получаем айди файла с фото и скачиваем
        photo_file = message.photo[-1].file_id
        photo = await bot.get_file(photo_file)
        photo_extension = photo.file_path.split('.')[-1]  # получаем расширение файла
        photo_path = f"photos/{photo_file}.{photo_extension}"
        await photo.download(destination_file=photo_path)
        await state.update_data(user_question=message.caption, photo=message.photo, photo_path=photo_path)
        await UserConversation.next()  # переходить к следующему шагу
        await message.answer('Пожалуйста, укажите Ваш контакт для обратной связи (email/телефон)')
    elif message.text:  # если сообщение - только текст, переходить к следующему шагу
        await state.update_data(user_question=message.text)
        await UserConversation.next()
        await message.answer('Пожалуйста, укажите Ваш контакт для обратной связи (email/телефон)')
    elif message.photo:  # если сообщение - только фото, сохранить фото и запросить вопрос
        # Получаем айди файла с фото и скачиваем
        photo_file = message.photo[-1].file_id
        photo = await bot.get_file(photo_file)
        photo_extension = photo.file_path.split('.')[-1]  # получаем расширение файла
        photo_path = f"photos/{photo_file}.{photo_extension}"
        await photo.download(destination_file=photo_path)
        await state.update_data(photo=message.photo, photo_path=photo_path)
        await message.answer('Пожалуйста, введите текст вопроса.')


@dp.message_handler()
async def handle_answer_only(message: types.Message, state: FSMContext):
    await state.update_data(user_question=message.text)
    await UserConversation.next()


@dp.message_handler(state=UserConversation.quit)
async def handle_exit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = f'id Пользователя: {message.from_user.id}\n'
        user_category = f'Категория: {data["user_category"]}\n'
        user_branch = f'Филиал: {data["user_branch"]}\n'
        user_object = f'Объект: {data["user_object"]}\n'
        user_firstname_lastname = f'ФИО заявителя: {data["firstname_lastname_info"]}\n'
        user_question = f'Обращение: {data.get("user_question", "")}\n'
        user_number_phone_or_email = f'Контакты: {message.text}'

        db.add_message(user_id=message.from_user.id, user_category=user_category, user_object=user_object,
                       user_branch=user_branch,
                       firstname_lastname_info=user_firstname_lastname,
                       user_number_phone_or_email=user_number_phone_or_email, user_question=user_question)

        admin_message = f'Новое сообщение от пользователя:\n\n{user_id}{user_category}{user_branch}{user_object}' \
                        f'{user_firstname_lastname}{user_number_phone_or_email}\n{user_question} '

        if "photo" in data:
            # Если фотография была предоставлена, отправляем ее вместе с текстовым сообщением
            photo_path = data["photo_path"]
            photo_caption = "Фотография к сообщению"
            with open(photo_path, "rb") as photo_file:
                await bot.send_photo(chat_id=get_admin_id(data["user_category"]),
                                     photo=photo_file,
                                     caption=photo_caption)
            await bot.send_message(chat_id=get_admin_id(data["user_category"]), text=admin_message)
        else:
            await bot.send_message(chat_id=get_admin_id(data["user_category"]), text=admin_message)

    xg.generate_xml(user_id, user_category, user_object, user_branch, user_firstname_lastname,
                    user_number_phone_or_email,
                    user_question)

    # Отправка сообщения на почту с вложением XML-файла
    email_subject = 'Новое сообщение от пользователя'
    xml_attachment_path = 'user_data.xml'  # Укажите путь к XML-файлу
    photo_path = data.get("photo_path")
    send_email_with_attachment(email_subject, xml_attachment_path, photo_path)

    await state.finish()
    await message.answer('Спасибо! Ваш вопрос был отправлен на рассмотрение!')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    await message.answer('Пожалуйста, используйте команду /start для начала диалога.')


@dp.errors_handler(exception=Exception)
async def handle_errors(update, exception):
    # Обработчик ошибок и исключений
    print(f"Ошибка обработки обновления:\n{update}\n{exception}")

    # Если возникло исключение smtplib.SMTPAuthenticationError, то скорее всего проблема с аутентификацией
    if isinstance(exception, smtplib.SMTPAuthenticationError):
        print("Ошибка аутентификации. Проверьте правильность адреса электронной почты и пароля отправителя.")
    # Если возникло исключение FileNotFoundError, то скорее всего указан неправильный путь к файлу вложения или фотографии
    elif isinstance(exception, FileNotFoundError):
        print("Файл не найден. Проверьте правильность пути к файлу вложения или фотографии.")
    # Если возникло исключение smtplib.SMTPException, то скорее всего есть проблемы с SMTP-сервером
    elif isinstance(exception, smtplib.SMTPException):
        print("Ошибка SMTP-сервера. Проверьте настройки SMTP и подключение к серверу.")
    # Если возникло другое исключение, то вывести общее сообщение об ошибке
    else:
        print("Произошла ошибка при отправке электронной почты.")

    return True


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
