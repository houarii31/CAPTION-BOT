import os
import io
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import google.generativeai as genai
from PIL import Image

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ذاكرة بسيطة فالراس، كل مستخدم واللغة ديالو
user_lang = {}

LANGS = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "ar": "🇩🇿 دارجة / عربية",
}


def lang_instruction(lang: str) -> str:
    if lang == "fr":
        return "Réponds uniquement en français."
    if lang == "ar":
        return "جاوب بالدارجة الجزائرية البسيطة أو العربية الفصحى السهلة."
    return "Answer only in English."


def build_prompt(lang: str, topic: str | None = None) -> str:
    instruction = lang_instruction(lang)
    prompt = (
        f"{instruction}\n"
        "أنت خبير فصناعة محتوى السوشيال ميديا (فيسبوك وتيكتوك).\n"
        "اكتب:\n"
        "1) كابشن جذاب وقصير (سطرين لـ 3) مناسب للمنشور، فيه إيموجي مناسبة.\n"
        "2) 10 هاشتاقات مرتبطة بالمحتوى: خليط بين هاشتاقات مشهورة وهاشتاقات دقيقة (niche).\n\n"
        "الفورمات ديال الجواب بالضبط:\n"
        "Caption:\n<النص هنا>\n\nHashtags:\n<الهاشتاقات مفصولة بمسافة>"
    )
    if topic:
        prompt += f"\n\nالموضوع أو الكلمة لي عطاني المستخدم: {topic}"
    return prompt


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(v, callback_data=k)] for k, v in LANGS.items()]
    await update.message.reply_text(
        "أهلا! 👋 اختار اللغة ديال الكابشن والهاشتاقات:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_lang[query.from_user.id] = query.data
    await query.edit_message_text(
        f"تم! ✅ اللغة: {LANGS[query.data]}\n\n"
        "دابا:\n"
        "📸 صيفط تصويرة → نعطيك كابشن + هاشتاقات\n"
        "✍️ كتب كلمة أو موضوع → نعطيك كابشن + هاشتاقات\n\n"
        "باش تبدل اللغة فأي وقت، كتب /start"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "fr")
    await update.message.chat.send_action("typing")

    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    image = Image.open(io.BytesIO(bytes(photo_bytes)))

    prompt = build_prompt(lang)
    try:
        response = model.generate_content([prompt, image])
        text = response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        text = "⚠️ صرا مشكل تقني، عاود المحاولة من بعد شوية."

    await update.message.reply_text(text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "fr")
    topic = update.message.text
    await update.message.chat.send_action("typing")

    prompt = build_prompt(lang, topic)
    try:
        response = model.generate_content(prompt)
        text = response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        text = "⚠️ صرا مشكل تقني، عاود المحاولة من بعد شوية."

    await update.message.reply_text(text)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_lang))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logging.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
