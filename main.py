import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import wikipedia

# Wikipedia kutubxonasiga ulanish
wikipedia.set_lang("uz") # Maqola tilini sozlash, masalan "uz" uchun o'zbek, "en" uchun ingliz tili
wikipedia.set_rate_limiting(True) # soatda faqat qancha so'roq yuborilishi mumkinligini belgilaydi.

# Logging konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# /search buyrug'iga javob qaytarish
def search(update: Update, context: CallbackContext):
    query = update.message.text
    try:
        result = wikipedia.summary(query)
        update.message.reply_text(result)
    except wikipedia.exceptions.PageError:
        update.message.reply_text("Maqola topilmadi.")
    except wikipedia.exceptions.DisambiguationError as e:
        update.message.reply_text("Boshqa maqolalar topildi, iltimos, qidirilayotgan mavzuni aniqroq kiritish uchun qidiruv so'zini batafsilroq yozing.")
    except Exception as e:
        update.message.reply_text("Ma'lumotlar olishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

# /start buyrug'iga javob qaytarish
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Assalomu alaykum! Wikipedia botiga xush kelibsiz. Maqolani topish uchun kerakli so'zni botga yuboring.")

def main():
    """Start the bot."""
    # Telegram Bot tokenini yuklab olish
    updater = Updater("6854701223:AAEGihOzIfg0dwv6JbxOg7Tqzo-2DbQKhaw")

    # Buyruqlarni qayta ishlash uchun dispetcherni yaratish
    dispatcher = updater.dispatcher

    # Buyruqlar bilan qanday ishlovchilarni bog'lash
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, search))
    dispatcher.add_handler(MessageHandler(Filters.all, start))

    # Botni ishga tushirish
    updater.start_polling()

    # Botni ishlashini to'xtatish
if __name__=='__main__':
    main()