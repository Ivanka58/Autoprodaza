import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Данные из секретов
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
string_session = os.getenv('STRING_SESSION')
group_id = int(os.getenv('GROUP_ID'))
channel_id = int(os.getenv('CHANNEL_ID'))

client = TelegramClient(StringSession(string_session), api_id, api_hash)

print("Бот запущен и готов к работе...")

@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    try:
        # 1. Пересылаем в канал
        forwarded = await event.forward_to(channel_id)
        
        # Получаем юзернейм или имя
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else sender.first_name
        
        # Ссылка на пост в канале (если канал публичный)
        # Если канал частный, ссылка не будет работать для всех, но мы её создаем
        channel_entity = await client.get_entity(channel_id)
        channel_username = channel_entity.username if channel_entity.username else f"c/{str(channel_id)[4:]}"
        msg_link = f"https://t.me/{channel_username}/{forwarded.id}"

        # 2. Формируем текст уведомления
        notification_text = (
            f"Привет {username}!\n"
            f"Твое объявление [также было опубликовано]({msg_link}) в нашем канале @prodaja180!\n\n"
            f"Этот аккаунт — бот, не надо ему писать, он не ответит.\n"
            f"Если вы не согласны с публикацией или у вас есть вопросы, обратитесь к администратору @Ivanka58.\n"
            f"Приятных торгов!"
        )

        # 3. Пытаемся отправить в ЛС, если нет - отвечаем в группе
        try:
            await client.send_message(event.sender_id, notification_text, link_preview=False)
            print(f"Уведомление отправлено в ЛС пользователю {username}")
        except:
            await event.reply(notification_text, link_preview=False)
            print(f"ЛС закрыто, ответил в группе пользователю {username}")

    except Exception as e:
        print(f"Ошибка системы: {e}")

client.start()
client.run_until_disconnected()
