
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

CARDS = [
    ("Hallo!", "سلام!"),
    ("Guten Morgen!", "صبح بخیر!"),
    ("Guten Tag!", "روز بخیر!"),
    ("Guten Abend!", "عصر بخیر!"),
    ("Gute Nacht!", "شب بخیر!"),
    ("Grüß dich!", "سلام! (غیررسمی)"),
    ("Wie geht's?", "حالت چطور است؟"),
    ("Wie geht es dir?", "حالت چطور است؟"),
    ("Wie geht es Ihnen?", "حال شما چطور است؟ (رسمی)"),
    ("Auf Wiedersehen!", "خداحافظ! (رسمی)"),
    ("Tschüs!", "فعلاً / خداحافظ!"),
    ("Bis bald!", "به‌زودی می‌بینمت!"),
    ("Servus!", "سلام / خداحافظ (منطقه‌ای)"),
    ("der Name", "نام"),
    ("der Vorname", "نام کوچک"),
    ("der Familienname", "نام خانوادگی"),
    ("die Frau", "خانم"),
    ("der Herr", "آقا"),
    ("Ich heiße ...", "اسم من ... است."),
    ("Ich bin ...", "من ... هستم."),
    ("Mein Name ist ...", "نام من ... است."),
    ("Das ist ...", "این ... است."),
    ("Wer bist du?", "تو چه کسی هستی؟"),
    ("Wie heißt du?", "اسمت چیست؟"),
    ("Wie heißen Sie?", "نام شما چیست؟ (رسمی)"),
    ("buchstabieren", "هجی کردن"),
    ("das Alphabet", "الفبا"),
    ("Wie bitte?", "ببخشید؟ / چی فرمودید؟"),
    ("die Herkunft", "خاستگاه / محل اصالت"),
    ("Woher?", "از کجا؟"),
]

def keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("نمایش معنی", callback_data="show"),
            InlineKeyboardButton("کارت بعدی ⏭", callback_data="next")
        ]
    ])

async def send_card(update, context, index):
    context.user_data["index"] = index
    word, meaning = CARDS[index]
    text = f"📚 Deutsch mit Majid Fardi\n\n"
    text += f"کارت {index + 1} از {len(CARDS)}\n\n"
    text += f"🇩🇪 {word}\n\n"
    text += "برای دیدن معنی دکمه را بزنید."
    await update.message.reply_text(text, reply_markup=keyboard())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_card(update, context, 0)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    index = context.user_data.get("index", 0)

    if query.data == "show":
        word, meaning = CARDS[index]
        await query.message.reply_text(
            f"🇩🇪 {word}\n🇮🇷 {meaning}",
            reply_markup=keyboard()
        )

    elif query.data == "next":
        index = (index + 1) % len(CARDS)
        context.user_data["index"] = index
        word, meaning = CARDS[index]
        await query.message.reply_text(
            f"📚 کارت {index + 1} از {len(CARDS)}\n\n🇩🇪 {word}",
            reply_markup=keyboard()
        )

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
