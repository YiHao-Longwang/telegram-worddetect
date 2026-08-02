"""
Telegram spam-warning userbot.

Watches your group(s) for suspicious messages and privately DMs the sender
a warning, instead of calling them out publicly in the group.

Run with:  python warnbot.py
First run asks for a login code sent to your Telegram app.
"""

import asyncio
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import (
    UserPrivacyRestrictedError,
    UserIsBlockedError,
    FloodWaitError,
    PeerFloodError,
)
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

import config

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

if not all([API_ID, API_HASH, PHONE]):
    sys.exit("Missing API_ID / API_HASH / PHONE. Copy .env.example to .env and fill it in.")

client = TelegramClient("warnbot_session", int(API_ID), API_HASH)

# Compile matchers once
_keywords = [k.lower() for k in config.KEYWORDS]
_patterns = [re.compile(p, re.IGNORECASE) for p in config.REGEX_PATTERNS]

# Persisted state: who we warned and when, plus today's DM count
STATE_FILE = "warnbot_state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"warned": {}, "day": "", "sent_today": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


state = load_state()


def log(message: str):
    print(message, flush=True)


def _today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _reset_daily_counter():
    if state.get("day") != _today():
        state["day"] = _today()
        state["sent_today"] = 0


def is_suspicious(text: str) -> bool:
    matched, _ = match_suspicious(text)
    return matched


def match_suspicious(text: str):
    if not text:
        return False, ""
    lowered = text.lower()
    for keyword in _keywords:
        if keyword in lowered:
            return True, f"keyword={keyword!r}"
    for pattern in _patterns:
        if pattern.search(text):
            return True, f"regex={pattern.pattern!r}"
    return False, ""


def on_cooldown(user_id: int) -> bool:
    last = state["warned"].get(str(user_id))
    if not last:
        return False
    last_time = datetime.fromisoformat(last)
    return datetime.now(timezone.utc) - last_time < timedelta(hours=config.COOLDOWN_HOURS)


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------
# Build the chat filter for the event decorator
_chats = config.WATCH_GROUPS if config.WATCH_GROUPS else None


@client.on(events.NewMessage(chats=_chats))
async def handler(event):
    debug_skips = getattr(config, "DEBUG_LOG_SKIPS", False)
    log_all = getattr(config, "DEBUG_LOG_ALL_MESSAGES", False)

    # Ignore our own messages and non-user senders (channels, anon admins)
    if event.out:
        if debug_skips:
            log(f"[SKIP] own message in {event.chat_id}: {event.raw_text[:80]!r}")
        return

    if not event.sender_id:
        if debug_skips:
            log(f"[SKIP] no sender_id in {event.chat_id}: {event.raw_text[:80]!r}")
        return

    sender = await event.get_sender()
    if sender is None:
        if debug_skips:
            log(f"[SKIP] sender unavailable in {event.chat_id}: {event.raw_text[:80]!r}")
        return

    sender_is_bot = getattr(sender, "bot", False)
    matched, match_reason = match_suspicious(event.raw_text)

    if log_all:
        name = getattr(sender, "first_name", None) or getattr(sender, "title", None) or "unknown"
        log(
            f"[SEEN] chat_id={event.chat_id} sender_id={event.sender_id} "
            f"name={name!r} bot={sender_is_bot} matched={matched} text={event.raw_text[:120]!r}"
        )

    if sender_is_bot:
        if debug_skips and matched:
            name = getattr(sender, "first_name", None) or getattr(sender, "title", None) or "bot"
            log(
                f"[SKIP] bot sender matched {match_reason}: {name} ({sender.id}) "
                f"in {event.chat_id}: {event.raw_text[:80]!r}"
            )
        return

    if not matched:
        return

    name = getattr(sender, "first_name", None) or "there"
    uid = sender.id

    log(f"[FLAG] {name} ({uid}) in {event.chat_id} matched {match_reason}: {event.raw_text[:80]!r}")

    # --- Optional enforcement (needs admin rights) ---------------------------
    if config.DELETE_MESSAGE:
        try:
            await event.delete()
            log(f"       deleted message")
        except Exception as e:
            log(f"       could not delete: {e}")

    if config.MUTE_USER:
        try:
            until = datetime.now(timezone.utc) + timedelta(minutes=config.MUTE_MINUTES)
            rights = ChatBannedRights(until_date=until, send_messages=True)
            await client(EditBannedRequest(event.chat_id, uid, rights))
            log(f"       muted for {config.MUTE_MINUTES} min")
        except Exception as e:
            log(f"       could not mute: {e}")

    # --- The DM warning ------------------------------------------------------
    _reset_daily_counter()

    if on_cooldown(uid):
        log(f"       skip DM: on cooldown")
        return

    if state["sent_today"] >= config.MAX_DMS_PER_DAY:
        log(f"       skip DM: daily cap ({config.MAX_DMS_PER_DAY}) reached")
        return

    try:
        text = config.WARNING_MESSAGE.format(name=name)
        image = getattr(config, "WARNING_IMAGE", "")
        if image and os.path.exists(image):
            # Send the image with the warning as its caption
            await client.send_file(uid, image, caption=text, parse_mode="html")
        else:
            await client.send_message(uid, text, parse_mode="html")
        state["warned"][str(uid)] = datetime.now(timezone.utc).isoformat()
        state["sent_today"] += 1
        save_state(state)
        log(f"       DM sent ({state['sent_today']}/{config.MAX_DMS_PER_DAY} today)")
        await asyncio.sleep(config.DELAY_BETWEEN_DMS)

    except UserPrivacyRestrictedError:
        log(f"       DM blocked: user's privacy settings don't allow it")
    except UserIsBlockedError:
        log(f"       DM blocked: user has blocked this account")
    except PeerFloodError:
        log(f"       STOP: Telegram flagged this account for spam. Pausing.")
    except FloodWaitError as e:
        log(f"       flood wait: sleeping {e.seconds}s")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        log(f"       DM failed: {e}")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
async def main():
    await client.start(phone=PHONE)
    me = await client.get_me()
    log(f"Logged in as {me.first_name} (@{me.username}).")
    log(f"Watching: {config.WATCH_GROUPS or 'ALL groups'}")
    log(f"Listening for suspicious messages... DEBUG_LOG_SKIPS={getattr(config, 'DEBUG_LOG_SKIPS', False)}")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
