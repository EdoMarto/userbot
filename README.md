# Telegram Channel Mirror Userbot

A Telegram userbot, built with [Hydrogram](https://github.com/hydrogram/hydrogram), that mirrors one
channel into another in real time. It was built to mirror trading-signal posts into a free signals
channel.

Unlike a plain forward, a mirrored post looks like an original post in the target channel, and the
conversation structure is preserved:

- **New posts** are copied (text, media and formatting) without the "Forwarded from" header.
- **Replies** are posted as replies to the matching copy, so threads stay intact.
- **Edits** in the source channel are applied to the copy, including captions of media posts.

## How it works

```
source channel ──► on_message ──────► copy_message ──► target channel
       │                                   │
       │                                   ▼
       └──────► on_edited_message ──► MySQL: source id → copy id ──► edit copy
```

The bot runs as a user account, not a bot account, so it can read channels the user is a member of
without admin rights. Each copy's id is stored in MySQL next to the source id. When a reply or an edit
arrives, the bot looks up the copy it belongs to. Replies to posts that were never mirrored are skipped.

## Getting started

Requirements: Python 3.9+, a MySQL database, and Telegram API credentials from
[my.telegram.org/apps](https://my.telegram.org/apps).

```bash
pip install -r requirements.txt
mysql -u <user> -p <database> < schema.sql
cp .env.example .env      # then fill in the values
python ubot.py
```

On the first run Hydrogram asks for your phone number and the login code, then saves the session to
`my_account.session`. The session gives full access to the account: keep it private (it is
git-ignored).

## Configuration

All settings are read from environment variables, or from a `.env` file:

| Variable | Description |
|---|---|
| `TG_API_ID`, `TG_API_HASH` | Telegram API credentials |
| `SESSION_NAME` | Session file name, `my_account` by default |
| `SOURCE_CHAT_ID` | Channel to mirror from (channel ids start with `-100`) |
| `TARGET_CHAT_ID` | Channel to post into; the account must be allowed to post there |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | MySQL connection |

## Tech stack

Python · Hydrogram (MTProto) · MySQL

## License

[MIT](LICENSE)

> Userbots automate a personal account, which Telegram allows through its API but restricts against spam.
> Mirror only content you are allowed to redistribute.
