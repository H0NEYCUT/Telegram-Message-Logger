from flask import Flask, send_from_directory, render_template
from markupsafe import Markup
from threading import Thread
from telethon import TelegramClient, events
from dotenv import load_dotenv
from datetime import datetime
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

# Initialize Flask
app = Flask(__name__, template_folder='.')

# Dictionary to store the number of media files for each chat
media_counts = {}

@app.route('/')
def index():
    files = os.listdir(LOGS_DIRECTORY)
    return render_template('index.html', files=files)

@app.route('/logs/<path:path>')
def send_log(path):
    with open(os.path.join(LOGS_DIRECTORY, path), 'r') as f:
        content = Markup(f.read())
    return render_template('log.html', content=content)

@app.route('/media/<path:path>')
def send_media(path):
    return send_from_directory(MEDIA_DIRECTORY, path)

def run_flask():
    app.run(port=5000) # To open the logger up to public, change this line to the following: app.run(host='0.0.0.0', port=5000)

# Start Flask in a new thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

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
        # Format the message's datetime
        message_time = message.date.astimezone().strftime('%Y-%m-%d %H:%M:%S')

        if message.media:
            # Increment the media count for this chat
            media_counts[chat_id] = media_counts.get(chat_id, 0) + 1
            
            # Use the media count as the filename
            media_filename = f"{media_counts[chat_id]}{message.file.ext}"
            media = await message.download_media(file=os.path.join(media_dir, media_filename))
            
            media_path = os.path.join('/', MEDIA_DIRECTORY, str(chat_id), media_filename)
            
            # Check the file extension to determine whether to use an <img> or <video> tag
            if media_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.svg', '.ico')):
                file.write(f"<p><b><u>{message_time} {sender_id}</u></b>: {message.message} <img src='{media_path}' alt='Media' style='max-width: 250px; max-height: 250px;'> <a href='{media_path}' target='_blank'>[Direct link]</a></p>\n")
            elif media_filename.lower().endswith(('.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.3gp', '.3g2', '.m4v', '.mpg', '.mpeg', '.m2v', '.m4v', '.f4v', '.f4p', '.f4a', '.f4b', '.mp4v', '.flv', '.vob')):
                file.write(f"<p><b><u>{message_time} {sender_id}</u></b>: {message.message} <video src='{media_path}' controls style='max-width: 500px; max-height: 500px;'></video> <a href='{media_path}' target='_blank'>[Direct link]</a></p>\n")
        else:
            file.write(f"<p><b><u>{message_time} {sender_id}</u></b>: {message.message}</p>\n")

if __name__ == '__main__':
    client.loop.run_until_complete(main())