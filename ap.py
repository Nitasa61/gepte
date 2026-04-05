import telebot
import subprocess
import os

# Data dari BotFather kamu
TOKEN = '8551014406:AAH_cYw276Hj6_GSbuwZ2f6pxuEfL0bF4DU'
# Masukkan ID Telegram kamu (angka) agar orang lain tidak bisa bajak VPS
ADMIN_ID = 6815885839 

bot = telebot.TeleBot(TOKEN)

def is_admin(message):
    return message.from_user.id == ADMIN_ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_admin(message):
        bot.reply_to(message, "✅ Bot Terhubung! Gunakan /cek untuk info server atau kirim perintah linux apapun.")
    else:
        bot.reply_to(message, "❌ Akses Ditolak.")

@bot.message_handler(commands=['cek'])
def check_server(message):
    if is_admin(message):
        # Mengambil info RAM dan Uptime
        ram = os.popen('free -m').read()
        uptime = os.popen('uptime -p').read()
        respon = f"ℹ️ **Info Server:**\n\n**Uptime:**\n`{uptime}`\n**RAM (MB):**\n`{ram}`"
        bot.reply_to(message, respon, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def execute_command(message):
    if is_admin(message):
        try:
            # Menjalankan perintah yang kamu ketik di Telegram langsung ke terminal VPS
            process = subprocess.Popen(message.text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            output = stdout if stdout else stderr
            if not output:
                output = "(Perintah dijalankan tanpa output)"
                
            # Limit karakter telegram (max 4096) agar tidak error jika output panjang
            bot.reply_to(message, f"📄 **Output:**\n`{output[:4000]}`", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"⚠️ **Error:**\n`{str(e)}`", parse_mode="Markdown")

print("Bot sedang berjalan...")
bot.polling()