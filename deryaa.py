import asyncio
import warnings
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# 1. Windows için DNS ve Event Loop yaması (Hatanın çözümü burada)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Pydantic uyarılarını gizle
warnings.filterwarnings("ignore", category=UserWarning)

# --- AYARLAR ---
TOKEN = '8558975814:AAE8l1kVRGp5mFPAEebr_8fzD3SW1EjjaF0'
ADMIN_ID = 7368199274  # Kendi Telegram ID'ni buraya yaz

request_counter = 0
bot = Bot(token=TOKEN)
dp = Dispatcher()

# KATILMA İSTEĞİ GELDİĞİNDE
@dp.chat_join_request()
async def welcome_request(update: ChatJoinRequest):
    global request_counter
    request_counter += 1
    
    text = (
        "Merhaba Canım En Güzel Orospuların İfşalarının Bulunduğu\n"
        "Çılgın Kanallara Katılmak İster misin?\n\n"
        "İşte En İyi Türk İfşa Kanalları\n"
        "👇👇👇👇👇👇👇👇👇👇👇👇👇"
    )
    
    # Buton linklerini kendine göre güncelle
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="TÜRK İFŞA İZLE  🔥", url="https://t.me/+BiOfsdHHKGAzMGNk")],
        [InlineKeyboardButton(text="ONLYFANS İFŞA  🔞", url="https://t.me/+JNpGJ10xTkVjM2E0")],
        [InlineKeyboardButton(text="ENSEST İFŞA VİDEOLARI 💦", url="https://t.me/+HH2ALPSN9KUzNGVk")]
    ])

    try:
        await bot.send_message(chat_id=update.from_user.id, text=text, reply_markup=keyboard)
    except:
        # Kullanıcı botu engellediyse hata vermemesi için
        pass

# İSTATİSTİK KOMUTU
@dp.message(Command("stat"))
async def show_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            f"📊 **BOT: SELİN**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"✅ Bugün Gelen İstek Sayısı: {request_counter}"
        )

async def main():
    print("Selin Botu Başlatılıyor... (Windows Mode)")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot kapatıldı.")
