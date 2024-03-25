from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Your Telegram API ID and API hash
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')

# Directory to store message logs and media files
LOGS_DIRECTORY = 'logs/'
MEDIA_DIRECTORY = 'media/'

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(MEDIA_DIRECTORY, exist_ok=True)

# Initialize the Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    # Start the client
    await client.start()
    # Print logging start message
    print("Logging has started to logs/ and media/")
    # Run until Ctrl+C is pressed
    await client.run_until_disconnected()

# Function to handle incoming messages
@client.on(events.NewMessage)
async def handle_incoming(event):
    message = event.message
    sender_id = message.from_id
    chat_id = message.peer_id.user_id if message.is_private else message.chat_id
    
    log_filename = f"{LOGS_DIRECTORY}{chat_id}.txt"
    media_dir = f"{MEDIA_DIRECTORY}{chat_id}/"
    
    # Log the message
    with open(log_filename, "a") as file:
        if message.media:
            media = await message.download_media(file=media_dir)
            file.write(f"<{sender_id}>: {message.message} (Media saved to {media})\n")
        else:
            file.write(f"<{sender_id}>: {message.message}\n")

if __name__ == '__main__':
    client.loop.run_until_complete(main())
