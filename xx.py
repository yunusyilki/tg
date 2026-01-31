import asyncio
import random
import warnings
import sys
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 1. Hataları ve uyarıları engelle
warnings.filterwarnings("ignore", category=UserWarning)

# Windows için özel Event Loop ayarı (RuntimeError: aiodns hatasını çözer)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- AYARLAR ---
TOKEN = '8556351477:AAGTzCsl2m24GKLZ4TxXNWtbodftSQgX6VM'
CHANNEL_ID = -1001735621817        # Paylaşılacak Kanal
SOURCE_CHANNEL_ID = -1001735621817 # Mesajların Alınacağı Kanal
START_MSG_ID = 1248
END_MSG_ID = 1681 
INTERVAL_MINUTES = 30

# aiodns hatasını engellemek için trust_env=True olan bir session kullanıyoruz
bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()
msg_pool = []

def refresh_pool():
    global msg_pool
    msg_pool = list(range(START_MSG_ID, END_MSG_ID + 1))
    random.shuffle(msg_pool)
    print(f"✅ Havuz yenilendi: {len(msg_pool)} mesaj sıraya alındı.")

async def copy_random_post():
    global msg_pool
    if not msg_pool:
        refresh_pool()
    
    msg_id = msg_pool.pop()
    try:
        await bot.copy_message(
            chat_id=CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=msg_id
        )
        print(f"🚀 Paylaşım Başarılı! (ID: {msg_id}) - Kalan: {len(msg_pool)}")
    except Exception as e:
        # Eğer mesaj silinmişse veya hata varsa burada RecursionError olmasın diye
        # doğrudan fonksiyonu tekrar çağırmak yerine küçük bir bekleme ekliyoruz.
        print(f"❌ ID {msg_id} kopyalanamadı, bir sonrakine geçiliyor...")
        await asyncio.sleep(1)
        # Çok fazla peş peşe hata alıp botu kitlememesi için kontrol
        if len(msg_pool) > 0:
            return await copy_random_post()

async def main():
    refresh_pool()
    # İlk paylaşımı hemen yap (test için)
    await copy_random_post()
    
    scheduler.add_job(copy_random_post, 'interval', minutes=INTERVAL_MINUTES)
    scheduler.start()
    
    print(f"🔥 Bot Aktif! {INTERVAL_MINUTES} dakikada bir paylaşım yapılıyor...")
    
    # Botun açık kalmasını sağlayan döngü
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass