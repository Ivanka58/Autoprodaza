import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Данные из секретов
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
string_session = os.getenv('STRING_SESSION')
group_id = int(os.getenv('GROUP_ID'))
channel_id = int(os.getenv('CHANNEL_ID'))

client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def send_notification(event, forwarded_msg, sender):
    """Функция для отправки уведомления пользователю с твоим текстом"""
    username = f"@{sender.username}" if sender.username else sender.first_name
    
    # Ссылка на первый пост в канале
    channel_entity = await client.get_entity(channel_id)
    channel_username = channel_entity.username if channel_entity.username else f"c/{str(channel_id)[4:]}"
    msg_id = forwarded_msg[0].id if isinstance(forwarded_msg, list) else forwarded_msg.id
    msg_link = f"https://t.me/{channel_username}/{msg_id}"

    # Твой полный текст
    text = (
        f"Привет {username}!\n"
        f"Твое объявление [также было опубликовано]({msg_link}) в нашем канале @prodaja180!\n"
        f"Этот аккаунт — бот, не надо ему писать, он не ответит.\n"
        f"Если вы не согласны с публикацией объявления или у вас есть вопросы обратитесь к администратору @Ivanka58. Приятных торгов!"
    )
    
    try:
        await client.send_message(event.sender_id, text, link_preview=False)
    except:
        await event.reply(text, link_preview=False)

print("Бот запущен. Режим: Альбомы + Фильтры (Люди, Фото+Текст)...")

# 1. ОБРАБОТКА ОДИНОЧНЫХ СООБЩЕНИЙ
@client.on(events.NewMessage(chats=group_id, func=lambda e: e.grouped_id is None))
async def single_handler(event):
    sender = await event.get_sender()
    if sender and getattr(sender, 'bot', False): return # Игнор ботов
    
    # Обязательно фото И текст
    if event.photo and event.message.message:
        forwarded = await event.forward_to(channel_id)
        await send_notification(event, forwarded, sender)

# 2. ОБРАБОТКА АЛЬБОМОВ (ГРУПП ФОТО)
@client.on(events.Album(chats=group_id))
async def album_handler(event):
    sender = await event.get_sender()
    if sender and getattr(sender, 'bot', False): return # Игнор ботов

    # В альбоме текст обычно в первом сообщении
    if event.original_update.message.message or any(m.message for m in event.messages):
        # Пересылаем весь альбом целиком
        forwarded = await event.forward_to(channel_id)
        await send_notification(event, event.messages[0], sender)

client.start()
client.run_until_disconnected()
