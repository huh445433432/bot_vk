import json
import os
from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id

# --- КОНФИГУРАЦИЯ ---
TOKEN = os.environ.get("VK_TOKEN")
CONFIRM_STRING = os.environ.get("CONFIRM_STRING")

if not TOKEN:
    raise RuntimeError("Не задан VK_TOKEN в переменных окружения")
if not CONFIRM_STRING:
    raise RuntimeError("Не задан CONFIRM_STRING в переменных окружения")

app = Flask(__name__)

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

user_choice = {}

def make_keyboard(buttons_rows, one_time=True):
    keyboard = {
        "one_time": one_time,
        "buttons": buttons_rows
    }
    return json.dumps(keyboard, ensure_ascii=False)

def send_message(peer_id, message_text, keyboard_json=None):
    try:
        vk.messages.send(
            peer_id=peer_id,
            message=message_text,
            keyboard=keyboard_json,
            random_id=get_random_id()
        )
    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка VK API: {e}")

def handle_message(peer_id, user_id, text):
    text = text.strip().lower()

    if text in ["начать", "старт", "start", "главная", "главное меню"]:
        kb_rows = [
            [{"action": {"type": "text", "label": "🛍 Магазин"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "ℹ️ Помощь"}, "color": "secondary"}]
        ]
        send_message(
            peer_id,
            "👋 Добро пожаловать в тестовый магазин!\nВыберите действие:",
            make_keyboard(kb_rows, one_time=True)
        )

    elif text in ["магазин", "товары", "каталог", "🛍 магазин"]:
        kb_rows = [
            [{"action": {"type": "text", "label": "🚀 Премиум - 100₽"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "⚡ Ускорение - 50₽"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🎨 Стикерпак - 30₽"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}]
        ]
        send_message(
            peer_id,
            "🛍 Наш магазин:\nВыберите товар для покупки:",
            make_keyboard(kb_rows, one_time=True)
        )

    elif text == "🚀 премиум - 100₽":
        user_choice[user_id] = {"name": "Премиум", "price": 100, "desc": "30 дней премиум доступа"}
        kb_rows = [
            [{
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com",
                    "label": "💳 Оплатить 100₽"
                },
                "color": "positive"
            }],
            [{"action": {"type": "text", "label": "🛍 Другие товары"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}]
        ]
        send_message(
            peer_id,
            "✅ Вы выбрали: Премиум\n💰 Цена: 100₽\n📝 30 дней премиум доступа\nНажмите кнопку оплаты:",
            make_keyboard(kb_rows, one_time=True)
        )

    elif text == "⚡ ускорение - 50₽":
        user_choice[user_id] = {"name": "Ускорение", "price": 50, "desc": "7 дней ускорения"}
        kb_rows = [
            [{
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com",
                    "label": "💳 Оплатить 50₽"
                },
                "color": "positive"
            }],
            [{"action": {"type": "text", "label": "🛍 Другие товары"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}]
        ]
        send_message(
            peer_id,
            "✅ Вы выбрали: Ускорение\n💰 Цена: 50₽\n📝 7 дней ускорения\nНажмите кнопку оплаты:",
            make_keyboard(kb_rows, one_time=True)
        )

    elif text == "🎨 стикерпак - 30₽":
        user_choice[user_id] = {"name": "Стикерпак", "price": 30, "desc": "Эксклюзивные стикеры"}
        kb_rows = [
            [{
                "action": {"type": "open_link",
                    "link": "https://vk.com",
                    "label": "💳 Оплатить 30₽"
                },
                "color": "positive"
            }],
            [{"action": {"type": "text", "label": "🛍 Другие товары"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}]
        ]
        send_message(
            peer_id,
            "✅ Вы выбрали: Стикерпак\n💰 Цена: 30₽\n📝 Эксклюзивные стикеры\nНажмите кнопку оплаты:",
            make_keyboard(kb_rows, one_time=True)
        )

    elif text == "🛍 другие товары":
        kb_rows = [
            [{"action": {"type": "text", "label": "🚀 Премиум - 100₽"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "⚡ Ускорение - 50₽"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🎨 Стикерпак - 30₽"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}]
        ]
        send_message(
            peer_id,
            "🛍 Наш магазин:\nВыберите товар для покупки:",
            make_keyboard(kb_rows, one_time=True)
        )

    elif text in ["помощь", "help", "ℹ️ помощь"]:
        send_message(
            peer_id,
            "ℹ️ Помощь\nЭто тестовый бот для обучения работе с VK Pay.\n"
            "Как сделать тестовый платёж:\n1. Нажмите 'Магазин'\n2. Выберите товар\n3. Нажмите 'Оплатить'\n4. В появившемся окне подтвердите\nВсе платежи тестовые - деньги не списываются!"
        )

    else:
        kb_rows = [[{"action": {"type": "text", "label": "Начать"}, "color": "primary"}]]
        send_message(
            peer_id,
            "❌ Я вас не понимаю.\nИспользуйте кнопку 'Начать' для навигации:",
            make_keyboard(kb_rows, one_time=True)
        )

@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    if not data:
        return 'ok', 200

    # Подтверждение Callback API
    if data.get('type') == 'confirmation':
        return CONFIRM_STRING, 200

    # Обработка нового сообщения
    if data.get('type') == 'message_new':
        message = data.get('object', {}).get('message', {})
        peer_id = message.get('peer_id')
        user_id = message.get('from_id')
        text = message.get('text', '')

        if peer_id and user_id:
            handle_message(peer_id, user_id, text)

        return 'ok', 200

    return 'ok', 200

@app.route('/', methods=['GET'])
def home():
    return "Бот работает!", 200
