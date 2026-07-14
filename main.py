import json
import os
from flask import Flask, request, jsonify
import vk_api
from vk_api.utils import get_random_id

# --- КОНФИГУРАЦИЯ ---
# Замените на свои значения или используйте переменные окружения
TOKEN = os.environ.get("VK_TOKEN", "vk1.a.vu5xFY-QoQA9zpAcz1cIQcXtU0tf1Ehlc6VQ7hU3jKimx9yJ1BnDTa5C1A8iucygVezZYgNSfMDvqYfg_-XJPc0HxS51gtAZSfoLKVqTq9O45udNPl2xnXrzBF2NLu5tsghAIm0JngqMiO56PldVZ2xSPdaAjk6UhocMSc4Qc7s-I_oa3wwpwNhFa6uG3r-575eitYfFanHRv2g2aOen2g")`
CONFIRM_STRING = os.environ.get("CONFIRM_STRING", "401c9e27")  # Вставьте сюда строку из настроек Callback API

app = Flask(__name__)

# Авторизация VK
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# Хранилище выбранных пользователем товаров
user_choice = {}

def make_keyboard(buttons_rows, one_time=True):
    """Генерирует JSON-клавиатуру."""
    keyboard = {
        "one_time": one_time,
        "buttons": buttons_rows
    }
    return json.dumps(keyboard, ensure_ascii=False)

def send_message(peer_id, message_text, keyboard_json=None):
    """Безопасная отправка сообщения"""
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
    """Обрабатывает входящее сообщение"""
    text = text.strip().lower()

    # --- ГЛАВНОЕ МЕНЮ ---
    if text in ["начать", "старт", "start", "главная", "главное меню"]:
        kb_rows = [
            [
                {"action": {"type": "text", "label": "🛍 Магазин"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "ℹ️ Помощь"}, "color": "secondary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "👋 Добро пожаловать в тестовый магазин!\n"
            "Выберите действие:",
            kb_json
        )

    # --- МАГАЗИН (СПИСОК ТОВАРОВ) ---
    elif text in ["🛍 магазин", "магазин", "товары", "каталог"]:
        kb_rows = [
            [
                {"action": {"type": "text", "label": "🚀 Премиум - 100₽"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "⚡ Ускорение - 50₽"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "🎨 Стикерпак - 30₽"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "🛍 Наш магазин:\n\n"
            "Выберите товар для покупки:",
            kb_json
        )

    # --- ВЫБОР ПРЕМИУМ ---
    elif text == "🚀 премиум - 100₽":
        user_choice[user_id] = {
            "name": "Премиум",
            "price": 100,
            "desc": "30 дней премиум доступа"
        }
        kb_rows = [
            [
                {
                    "action": {
                        "type": "open_link",
                        "link": "https://vk.com",
                        "label": "💳 Оплатить 100₽"
                    },
                    "color": "positive"
                }
            ],
            [
                {"action": {"type": "text", "label": "🛍 Другие товары"}, "color": "secondary"}
            ],
            [
                {"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "✅ Вы выбрали: Премиум\n"
            "💰 Цена: 100₽\n"
            "📝 30 дней премиум доступа\n\n"
            "Нажмите кнопку оплаты для тестового платежа:",
            kb_json
        )


    elif text == "⚡ ускорение - 50₽":
        user_choice[user_id] = {
            "name": "Ускорение",
            "price": 50,
            "desc": "7 дней ускорения"
        }
        kb_rows = [
            [
                {
                    "action": {
                        "type": "open_link",
                        "link": "https://vk.com",
                        "label": "💳 Оплатить 50₽"
                    },
                    "color": "positive"
                }
            ],
            [
                {"action": {"type": "text", "label": "🛍 Другие товары"}, "color": "secondary"}
            ],
            [
                {"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "✅ Вы выбрали: Ускорение\n"
            "💰 Цена: 50₽\n"
            "📝 7 дней ускорения\n\n"
            "Нажмите кнопку оплаты для тестового платежа:",
            kb_json
        )

    # --- ВЫБОР СТИКЕРПАК ---
    elif text == "🎨 стикерпак - 30₽":
        user_choice[user_id] = {
            "name": "Стикерпак",
            "price": 30,
            "desc": "Эксклюзивные стикеры"
        }
        kb_rows = [
            [
                {
                    "action": {
                        "type": "open_link",
                        "link": "https://vk.com",
                        "label": "💳 Оплатить 30₽"
                    },
                    "color": "positive"
                }
            ],
            [
                {"action": {"type": "text", "label": "🛍 Другие товары"}, "color": "secondary"}
            ],
            [
                {"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "✅ Вы выбрали: Стикерпак\n"
            "💰 Цена: 30₽\n"
            "📝 Эксклюзивные стикеры\n\n"
            "Нажмите кнопку оплаты для тестового платежа:",
            kb_json
        )

    # --- ДРУГИЕ ТОВАРЫ (возврат к магазину) ---
    elif text == "🛍 другие товары":
        kb_rows = [
            [
                {"action": {"type": "text", "label": "🚀 Премиум - 100₽"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "⚡ Ускорение - 50₽"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "🎨 Стикерпак - 30₽"}, "color": "primary"}
            ],
            [
                {"action": {"type": "text", "label": "🏠 Главное меню"}, "color": "secondary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "🛍 Наш магазин:\n\n"
            "Выберите товар для покупки:",
            kb_json
        )

    # --- ПОМОЩЬ ---
    elif text in ["ℹ️ помощь", "помощь", "help", "ℹ️ помощь"]:
        send_message(
            peer_id,
            "ℹ️ Помощь\n\n"
            "Это тестовый бот для обучения работе с VK Pay.\n\n"
            "Как сделать тестовый платеж:\n"
            "1. Нажмите 'Магазин'\n"
            "2. Выберите товар\n"
            "3. Нажмите 'Оплатить'\n"
            "4. В появившемся окне подтвердите\n\n"
            "Все платежи тестовые - деньги не списываются!"
        )

    # --- НЕИЗВЕСТНЫЕ СООБЩЕНИЯ ---
    else:
        kb_rows = [
            [
                {"action": {"type": "text", "label": "Начать"}, "color": "primary"}
            ]
        ]
        kb_json = make_keyboard(kb_rows, one_time=True)
        send_message(
            peer_id,
            "❌ Я вас не понимаю.\n"
            "Используйте кнопку 'Начать' для навигации:",
            kb_json
        )


@app.route('/', methods=['POST'])
def main():
    """Обработчик входящих запросов от CallbackAPI ВК"""
    data = request.get_json()

    # Проверка на строку подтверждения (первый запрос от ВК)
    if data.get('type') == 'confirmation':
        return CONFIRM_STRING, 200

    # Обработка нового сообщения
    if data.get('type') == 'message_new':
        message = data['object']['message']
        peer_id = message['peer_id']
        user_id = message['from_id']
        text = message.get('text', '')

        handle_message(peer_id, user_id, text)

        return 'ok', 200

    return 'ok', 200

@app.route('/', methods=['GET'])
def home():
    """Проверка что сервер работает"""
    return "Бот работает!", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)