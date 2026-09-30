"""Telegram userbot that mirrors a source channel into a target channel.

New posts are copied, replies stay threaded and edits are propagated. The mapping between
source and target message ids is kept in MySQL so replies and edits can find their copy.
"""

import logging
import os

import mysql.connector
from dotenv import load_dotenv
from hydrogram import Client, filters

load_dotenv()

SOURCE_CHAT_ID = int(os.environ["SOURCE_CHAT_ID"])
TARGET_CHAT_ID = int(os.environ["TARGET_CHAT_ID"])

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
}

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("userbot")

app = Client(
    os.environ.get("SESSION_NAME", "my_account"),
    api_id=int(os.environ["TG_API_ID"]),
    api_hash=os.environ["TG_API_HASH"],
)


def find_copy(source_id):
    """Return the id of the target-channel copy of a source message, or None."""
    db = mysql.connector.connect(**DB_CONFIG)
    try:
        cursor = db.cursor()
        cursor.execute("SELECT receive_id FROM tradingpost WHERE send_id = %s", (source_id,))
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        db.close()


def save_copy(source_id, copy_id):
    db = mysql.connector.connect(**DB_CONFIG)
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO tradingpost (send_id, receive_id) VALUES (%s, %s)", (source_id, copy_id))
        db.commit()
        cursor.close()
    finally:
        db.close()


@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def mirror_post(client, message):
    reply_to = None
    if message.reply_to_message_id is not None:
        reply_to = find_copy(message.reply_to_message_id)
        if reply_to is None:
            log.warning("Skipped reply %s: the message it answers was never mirrored", message.id)
            return

    copy = await client.copy_message(TARGET_CHAT_ID, message.chat.id, message.id, reply_to_message_id=reply_to)
    save_copy(message.id, copy.id)
    log.info("Mirrored post %s as %s", message.id, copy.id)


@app.on_edited_message(filters.chat(SOURCE_CHAT_ID))
async def mirror_edit(client, message):
    copy_id = find_copy(message.id)
    if copy_id is None:
        log.warning("Skipped edit of %s: no mirrored copy found", message.id)
        return

    if message.text is not None:
        await client.edit_message_text(
            TARGET_CHAT_ID, copy_id, message.text, entities=message.entities, disable_web_page_preview=True
        )
    else:
        # Media posts carry their text in the caption.
        await client.edit_message_caption(
            TARGET_CHAT_ID, copy_id, message.caption or "", caption_entities=message.caption_entities
        )
    log.info("Mirrored edit of %s", message.id)


if __name__ == "__main__":
    app.run()
