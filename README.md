# Telegram Message Logger

This Python script allows you to log incoming and outgoing messages from your Telegram account to text files. It differentiates messages using user IDs and saves media files to a separate directory while adding references to them in the log files. You can view the logs at http://127.0.0.1:5000. Here the logs are in HTML, with media embeds.

## Getting Started

### Prerequisites

Before running the script, you need to install the following dependencies:

- Python 3
- Telethon library (`pip install telethon`)
- Python-dotenv library (`pip install python-dotenv`)
- Flask library (`pip install flask`)

### Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/H0NEYCUT/telegram-message-logger.git
   ```

2. Create a `.env` file in the project directory and add your Telegram API ID and API hash in the following format:

   ```env
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   ```

3. Run the script:

   ```bash
   python3 logger.py
   ```

4. The script will start logging incoming and outgoing messages to the `logs/` directory and save media files to the `media/` directory.
   There's a webUI running at http://127.0.0.1:5000. 

## Configuration

- `logger.py`: The main Python script for logging messages.
- `.env`: Configuration file to store your Telegram API ID and API hash.

## Demo

You can watch the demo of the logger here:


https://github.com/H0NEYCUT/Telegram-Message-Logger/assets/73757972/f3cecbba-ee57-4243-a840-e5a58fd4fa4c


## Contributing

Contributions are welcome! If you find any bugs or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
