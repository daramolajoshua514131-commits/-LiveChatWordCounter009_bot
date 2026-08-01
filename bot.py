import os
import re
from collections import Counter
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def analyze_text(text: str) -> str:
    # Character counts
    char_count = len(text)
    char_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))

    # Word count
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)

    # Sentence & Paragraph count
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = len(sentences)

    paragraphs = [p for p in text.split('\n') if p.strip()]
    paragraph_count = len(paragraphs)

    # Estimated Reading Time (~200 words per minute)
    reading_time_min = round(word_count / 200, 1)

    # Top Keywords for SEO
    lower_words = [w.lower() for w in words if len(w) > 3]
    top_keywords = Counter(lower_words).most_common(3)
    keyword_str = ", ".join([f"'{k}': {v}" for k, v in top_keywords]) if top_keywords else "None"

    return (
        f"📊 **Text Analysis Summary**\n"
        f"───────\n"
        f"📝 **Words:** `{word_count}`\n"
        f"🔤 **Characters (total):** `{char_count}`\n"
        f"🔤 **Characters (no spaces):** `{char_no_spaces}`\n"
        f"📄 **Sentences:** `{sentence_count}`\n"
        f"📑 **Paragraphs:** `{paragraph_count}`\n"
        f"⏱️ **Est. Reading Time:** `{reading_time_min} min`\n"
        f"🔑 **Top Keywords:** `{keyword_str}`"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Welcome to Content Count Bot!**\n\n"
        "Send or paste any text below, and I'll analyze word count, character count, "
        "sentences, paragraphs, and top keywords instantly."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    stats = analyze_text(user_text)
    await update.message.reply_text(stats, parse_mode="Markdown")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set.")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
