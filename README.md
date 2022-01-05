# Darts stats bot

This is a Telegram bot used to keep track of your darts score history.

## Usage

Make sure you have Python 3.6 or higher and pip on your machine.

Create your own telegram bot and get the token from bot father. Then create a `.env` file with the following content:

```
BOT_TOKEN=<your-bot-token-from-bot-father>
SECRET=<secret-string-for-authenticating>
DATABASE_URL=<database-url>
FIGURE_FILE=<filename-for-matplotlib-figure>
```

Then create a virtual environment, activate it and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Before starting the bot, initialize the database

```bash
python3 src/db.py
```

After that start the bot with the command

```bash
python3 src/index.py
```

## Testing

Set a `.env.test` file with the following content.

```
DATABASE_URL=<test-database-url>
```

and run tests with

```bash
ENV=TRUE pytest bot
```

The bot itself is not tested.
