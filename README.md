# Telegram Channel Mirror Userbot

A Telegram userbot, built with [Hydrogram](https://github.com/hydrogram/hydrogram), that mirrors one
channel into another in real time. I wrote it to copy trading signal posts into a free signals channel.

It's not a plain forward. A mirrored post looks like an original post in the target channel, and the
structure of the conversation is kept:

* New posts are copied over (text, media and formatting) without the "Forwarded from" header.
* Replies stay replies: each one is posted under the copy of the message it answered.
* Edits in the source channel are applied to the copy too, captions of media posts included.

## How it works

It runs as a user account, not a bot account, so it can read any channel you're a member of without admin
rights. When a post is mirrored, the id of the copy is saved in MySQL next to the id of the original. So
when a reply or an edit comes in later, the bot can look up which copy it belongs to. If a reply points
at a post that was never mirrored, it's skipped.

## Getting started

You need Python 3.9+, a MySQL database, and Telegram API credentials from
[my.telegram.org/apps](https://my.telegram.org/apps).

```bash
pip install -r requirements.txt
mysql -u <user> -p <database> < schema.sql
cp .env.example .env      # then fill in the values
python ubot.py
```

The first time you run it, Hydrogram asks for your phone number and the login code, then saves the
session to `my_account.session`. That file gives full access to the account, so keep it private. It's
already git-ignored.

## Configuration

Everything is read from environment variables, or from a `.env` file:

| Variable | What it is |
|---|---|
| `TG_API_ID`, `TG_API_HASH` | Telegram API credentials |
| `SESSION_NAME` | Session file name, `my_account` by default |
| `SOURCE_CHAT_ID` | Channel to mirror from (channel ids start with `-100`) |
| `TARGET_CHAT_ID` | Channel to post into; the account has to be allowed to post there |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | MySQL connection |

## Built with

Python, Hydrogram (MTProto) and MySQL.

## License

[MIT](LICENSE)

> A userbot automates a personal account. Telegram allows this through its API but comes down hard on
> spam, so only mirror content you're allowed to redistribute.
