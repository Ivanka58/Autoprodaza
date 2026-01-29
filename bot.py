import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Берем данные из секретов GitHub
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
string_session = os.getenv('STRING_SESSION')
group_id = int(os.getenv('GROUP_ID'))
channel_id = int(os.getenv('CHANNEL_ID'))

client = TelegramClient(StringSession(string_session), api_id, api_hash)

print("Бот запущен...")

@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    try:
        # 1. Пересылаем сообщение в канал
        await event.forward_to(channel_id)
        
        # 2. Отвечаем пользователю в личку (или в группе)
        notification_text = (
            f"🌐 Привет, [{event.sender.first_name}]!\\n\\n"
        f"Ваше объявление ({forwarded_mag.link}) успешно опубликовано в нашем канале: @prodaja180\\n"
        f"Этот аккаунт - бот, писать ему не надо, он не ответит.\\n"
        f"Если вы не согласны с публикацией, или у вас есть какие-либо вопросы, свяжитесь с администратором @ivanka58.\\n"
        f"Приятных торгов!"
        )
        await event.reply(notification_text)
        print(f"Обработано сообщение от {event.sender_id}")
    except Exception as e:
        print(f"Ошибка: {e}")

client.start()
client.run_until_disconnected()
