import logging
import requests
import os
from dotenv import load_dotenv
import socket
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from orders import cancel_order, cancel_self_reg_order, cancel_return_order, cancel_replacement_order, \
    cancel_lending_order, cancel_ecom_order


load_dotenv()
# Вставьте сюда ваш токен
TELEGRAM_TOKEN = os.getenv('TG_BOT_TOKEN')

authorized_users_str = os.getenv('AUTHORIZED_USERS')
AUTHORIZED_USERS = list(map(int, authorized_users_str.split(',')))

def is_domain_reachable(domain):
    try:
        # Попытка разрешить доменное имя
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False


# Выбор домена в зависимости от доступности
if is_domain_reachable('rrpoms.pmru.local'):
    domain = 'rrpoms.pmru.local'
else:
    domain = 'SecurePortalPMRU.myizhora.com'

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f'Привет, {user_name}👋 \n'
        'Отправь мне номер заказа для отмены.')


def normalize_order_id(order_id: str) -> str:
    replacements = {
        'о': 'O', 'О': 'O',  # Кириллическая 'О' на латинскую 'O'
        'в': 'B', 'В': 'B',  # Кириллическая 'В' на латинскую 'B'
        ' ': '', '-': '-'
    }

    # Переводим кириллицу в латиницу и заменяем в order_id
    for cyrillic_char, latin_char in replacements.items():
        order_id = order_id.replace(cyrillic_char, latin_char)

    return order_id.upper()


async def handle_message(update: Update, context: CallbackContext) -> None:
    if update.message is None:
        return

    # Получаем текст сообщения от пользователя
    user_id = update.message.from_user.id

    # Проверка, что пользователь авторизован
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("У вас нет доступа к использованию этого бота.")
        return

    order_id = update.message.text.strip()
    order_id = normalize_order_id(order_id)

    # Проверяем префикс и вызываем соответствующую функцию для отмены заказа
    if order_id.startswith("OB-"):
        response = cancel_order(order_id)
    elif order_id.startswith("OQ-"):
        response = cancel_self_reg_order(order_id)
    elif order_id.startswith("FB-"):
        response = cancel_return_order(order_id)
    elif order_id.startswith("RB-"):
        response = cancel_replacement_order(order_id)
    elif order_id.startswith("LB-"):
        response = cancel_lending_order(order_id)
    elif order_id.startswith("OE-"):
        response = cancel_ecom_order(order_id)
    else:
        await update.message.reply_text(
            "Не удалось распознать номер заказа. Пожалуйста, укажите корректный номер заказа.")
        return

    # Сохранение истории заказа
    save_order_history(user_id, order_id, response.status_code, response.text)

    # Обработка ответа от функции отмены заказа
    if response.status_code == 200:
        await update.message.reply_text(text=f"<code>Добрый день! Заказ {order_id} успешно отменен.</code>",
                                        parse_mode='HTML')
    else:
        await update.message.reply_text(text=f"Ошибка при отмене заказа {order_id}:\n"
                                             f"Статус код: <b>{response.status_code} \n</b>"
                                             f"Текст ошибки: {response.text}",
                                        parse_mode='HTML')


# Функция для создания таблиц в SQLite
def create_tables():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_history (
            user_id INTEGER,
            order_id TEXT,
            status_code INTEGER,
            response_text TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Функция для сохранения истории заказов в SQLite
def save_order_history(user_id, order_id, status_code, response_text):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO order_history (user_id, order_id, status_code, response_text)
        VALUES (?, ?, ?, ?)
    ''', (user_id, order_id, status_code, response_text))
    conn.commit()
    conn.close()


def main() -> None:
    # Создаем таблицы
    create_tables()

    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.getLogger("telegram").setLevel(logging.DEBUG)

    # Запуск бота
    application.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()