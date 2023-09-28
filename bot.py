import os
import discord
from discord.ext import commands
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from decouple import config

# Baca token bot Telegram dari berkas .env
telegram_token = config('TELEGRAM_TOKEN')

# Inisialisasi bot Telegram
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

# Baca token bot Discord dari berkas .env
discord_token = config('DISCORD_TOKEN')

# Inisialisasi bot Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Mendapatkan ID saluran Discord pertama dari berkas .env
discord_channel_id_1 = int(config('DISCORD_CHANNEL_ID_1'))

# Mendapatkan ID saluran Discord kedua dari berkas .env
discord_channel_id_2 = int(config('DISCORD_CHANNEL_ID_2'))

# Fungsi untuk mengirim pesan dari Telegram ke Discord
def send_telegram_to_discord(update: Update, context: CallbackContext):
    message = update.message.text

    # Menentukan saluran Discord berdasarkan logika tertentu
    # Misalnya, saluran pertama jika pesan mengandung "channel1", saluran kedua jika mengandung "channel2", dll.
    if "channel1" in message:
        channel_id = discord_channel_id_1
    elif "channel2" in message:
        channel_id = discord_channel_id_2
    else:
        # Atur saluran default jika tidak ada kata kunci yang cocok
        channel_id = discord_channel_id_1

    # Mendapatkan objek saluran Discord
    discord_channel = bot.get_channel(channel_id)

    if discord_channel:
        asyncio.run_coroutine_threadsafe(discord_channel.send(message), bot.loop)

# Fungsi untuk mengirim pesan dari Discord ke Telegram
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    telegram_bot = updater.bot
    chat_id = YOUR_TELEGRAM_CHAT_ID  # Ganti dengan ID obrolan Telegram yang sesuai
    await telegram_bot.send_message(chat_id, message.content)

# Menambahkan handler pesan dari Telegram
telegram_message_handler = MessageHandler(Filters.text & ~Filters.command, send_telegram_to_discord)
dispatcher.add_handler(telegram_message_handler)

# Menambahkan handler perintah untuk mengirim pesan ke Discord
@bot.command()
async def send_to_discord(ctx, *, message: str):
    channel_id = discord_channel_id_1  # Default Discord channel
    if "channel1" in message:
        channel_id = discord_channel_id_1
    elif "channel2" in message:
        channel_id = discord_channel_id_2

    discord_channel = bot.get_channel(channel_id)

    if discord_channel:
        await discord_channel.send(message)
    else:
        await ctx.send("Saluran Discord tidak ditemukan.")

# Memulai bot Telegram
updater.start_polling()

# Memulai bot Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(discord_token)
