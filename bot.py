import os
import logging
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# -------- Gemini --------
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyBzkG1sbFrh_cDMn-nvMxwHr7G-VngYHE0"
genai.configure(api_key=GEMINI_API_KEY)

# Model Gemini terbaru yang stabil
GEMINI_MODEL = "gemini-2.5-flash"

async def ask_gemini(prompt: str) -> str:
    """Panggil Gemini API untuk jawab pertanyaan."""
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: genai.GenerativeModel(GEMINI_MODEL).generate_content(prompt)
        )
        return response.text.strip()
    except Exception as e:
        logging.error("Gemini error: %s", e)
        return "⚠️ Maaf, terjadi kesalahan saat memproses jawaban AI."
# ------------------------

# ---------- Configuration ----------
TOKEN = os.getenv("TELEGRAM_TOKEN") or "8303623186:AAHRpYMpF29blS-2GuNiCZAbuhYRgjy5K-c"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Static content ----------
FAKULTAS_INFO = {
    "Fakultas Teknik": ["Teknik Informatika", "Teknik Elektro", "Teknik Sipil"],
    "Fakultas Ekonomi": ["Manajemen", "Akuntansi"],
    "Fakultas Ilmu Komputer": ["Sistem Informasi", "Teknologi Informasi"]
}

BEASISWA_INFO = [
    "Beasiswa Prestasi: potongan UKT untuk mahasiswa berprestasi akademik.",
    "Beasiswa Keluarga Tidak Mampu: bantuan selektif berdasarkan verifikasi dokumen.",
    "Beasiswa Mitra Industri: beasiswa kerja sama dengan perusahaan."
]

ALUR_PENDAFTARAN = [
    "1. Kunjungi situs resmi pendaftaran: https://binadarma.ac.id/pendaftaran",
    "2. Isi formulir online & unggah dokumen (ijazah, KTP, pas foto).",
    "3. Lakukan pembayaran biaya pendaftaran (jika ada).",
    "4. Ikuti seleksi/tes (jika program memerlukan).",
    "5. Pengumuman & konfirmasi pendaftaran."
]
# -----------------------------------

# ---------- Command Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo 👋 Selamat datang di Chatbot Promosi Kampus Bina Darma!\n"
        "Ketik /menu untuk melihat pilihan, atau tulis pertanyaan (mis. 'apa jurusan Teknik Informatika?')."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/menu - Menu interaktif\n"
        "/info - Info singkat kampus\n"
        "/fakultas - Daftar fakultas & jurusan\n"
        "/beasiswa - Info beasiswa\n"
        "/alur - Alur pendaftaran\n"
        "/kontak - Kontak kampus\n"
        "/event - Event terbaru\n\n"
        "Atau ketik pertanyaan langsung (contoh: 'jadwal pendaftaran kapan?')."
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Universitas Bina Darma, Palembang.\nWebsite: https://binadarma.ac.id\nInstagram: @binadarma_official"
    )

async def fakultas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_lines = ["📚 *Daftar Fakultas & Jurusan*"]
    for fac, prodi in FAKULTAS_INFO.items():
        text_lines.append(f"\n{fac}:")
        for p in prodi:
            text_lines.append(f" - {p}")
    await update.message.reply_text("\n".join(text_lines))

async def beasiswa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎓 *Info Beasiswa:*\n" + "\n".join(BEASISWA_INFO))

async def alur_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 *Alur Pendaftaran:*\n" + "\n".join(ALUR_PENDAFTARAN))

async def daftar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Pendaftaran mahasiswa baru melalui:\nhttps://binadarma.ac.id/pendaftaran"
    )

async def event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 Info event kampus terbaru: cek Instagram resmi @binadarma_official atau situs kampus."
    )

async def kontak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Alamat: Jl. Jenderal Ahmad Yani No.12, Palembang\n"
        "☎️ (0711) 515581\n"
        "🌐 https://binadarma.ac.id"
    )
# -------------------------------------

# ---------- Menu + Buttons ----------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Daftar", callback_data="daftar")],
        [InlineKeyboardButton("📚 Fakultas", callback_data="fakultas")],
        [InlineKeyboardButton("🎓 Beasiswa", callback_data="beasiswa")],
        [InlineKeyboardButton("📝 Alur", callback_data="alur")],
        [InlineKeyboardButton("📍 Kontak", callback_data="kontak")],
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Silakan pilih menu:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "fakultas":
        text_lines = ["📚 Daftar Fakultas & Jurusan:"]
        for fac, prodi in FAKULTAS_INFO.items():
            text_lines.append(f"\n{fac}:")
            for p in prodi:
                text_lines.append(f" - {p}")
        await query.edit_message_text("\n".join(text_lines))
    elif query.data == "beasiswa":
        await query.edit_message_text("🎓 Beasiswa:\n" + "\n".join(BEASISWA_INFO))
    elif query.data == "alur":
        await query.edit_message_text("📝 Alur Pendaftaran:\n" + "\n".join(ALUR_PENDAFTARAN))
    elif query.data == "daftar":
        await query.edit_message_text("📝 Daftar di: https://binadarma.ac.id/pendaftaran")
    elif query.data == "kontak":
        await query.edit_message_text("📍 Jl. Jenderal Ahmad Yani No.12, Palembang\n☎️ (0711) 515581")
    elif query.data == "info":
        await query.edit_message_text("🎓 Universitas Bina Darma\nWebsite: https://binadarma.ac.id")
    else:
        await query.edit_message_text("⚠️ Menu tidak dikenali.")
# -------------------------------------

# ---------- Free-text (AI) ----------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    if user_text.startswith("/"):
        return

    low = user_text.lower()
    if "fakultas" in low or "jurusan" in low:
        await fakultas_command(update, context)
        return
    if "beasiswa" in low:
        await beasiswa_command(update, context)
        return
    if "pendaftaran" in low or "daftar" in low:
        await alur_command(update, context)
        return

    prompt = f"Tolong jawab pertanyaan tentang Universitas Bina Darma secara singkat, ramah, dan jelas: \"{user_text}\""
    answer = await ask_gemini(prompt)
    await update.message.reply_text(answer)
# -------------------------------------

# ---------- Main ----------
def main():
    if not TOKEN or TOKEN.startswith("MASUKKAN"):
        print("❌ ERROR: Token Telegram belum diisi.")
        return

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("fakultas", fakultas_command))
    app.add_handler(CommandHandler("beasiswa", beasiswa_command))
    app.add_handler(CommandHandler("alur", alur_command))
    app.add_handler(CommandHandler("daftar", daftar_command))
    app.add_handler(CommandHandler("event", event_command))
    app.add_handler(CommandHandler("kontak", kontak_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Free text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 Bot Promosi Bina Darma berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
