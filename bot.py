import os
import yt_dlp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8555710010:AAFBZD-4PpEvvrhkIP2M_m49rsTQITXIwiY"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

keyboard = ReplyKeyboardMarkup(
    [["🎵 Аудіо", "🎬 Відео"]],
    resize_keyboard=True
)

user_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n\nОбери формат:",
        reply_markup=keyboard
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🎵 Аудіо":
        user_mode[user_id] = "audio"
        await update.message.reply_text("🎧 Надішли посилання")
        return

    if text == "🎬 Відео":
        user_mode[user_id] = "video"
        await update.message.reply_text("🎥 Надішли посилання")
        return

    if "youtube.com" in text or "youtu.be" in text:
        if user_id not in user_mode:
            await update.message.reply_text("☝️ Спочатку обери формат.")
            return

        mode = user_mode[user_id]
        await update.message.reply_text("⏳ Завантажую...")

        try:
            if mode == "audio":
                ydl_opts = {
                    'format': 'bestaudio',
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                }
            else:
                ydl_opts = {
                    'format': 'mp4',
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text)
                filename = ydl.prepare_filename(info)
                if mode == "audio":
                    filename = filename.rsplit(".", 1)[0] + ".mp3"

            if mode == "audio":
                await update.message.reply_audio(open(filename, "rb"))
            else:
                await update.message.reply_video(open(filename, "rb"))

            os.remove(filename)

        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Бот запущений")
    app.run_polling()

if __name__ == "__main__":
    main()
from flask import Flask
import os
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

def start_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()
