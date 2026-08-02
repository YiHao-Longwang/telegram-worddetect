# Telegram spam-warning userbot

Watches your group for suspicious messages and **privately DMs the sender a warning**
instead of calling them out in the group.

## Setup (one time)

1. **Get API credentials**
   Go to https://my.telegram.org → *API development tools* → create an app.
   Copy the `api_id` and `api_hash`.

2. **Configure secrets**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and paste your `API_ID`, `API_HASH`, and `PHONE`.

3. **Install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set what to watch**
   Edit `config.py` — put your group's username in `WATCH_GROUPS`,
   adjust `KEYWORDS`, and edit the `WARNING_MESSAGE`.

## Run

```bash
python warnbot.py
```

First run sends a login code to your Telegram app — enter it once.
A `warnbot_session` file is created so you won't need to log in again.
Leave it running (a laptop that stays on, or a cheap VPS).

## Notes

- The account running this must **already be a member** of the group.
- Deleting/muting offenders (`config.py` section 5) only works if the account is a **group admin**.
- Built-in safety: per-user cooldown, daily DM cap, and delays — keep these reasonable
  so the account isn't flagged by Telegram's anti-spam system.
- If a user's privacy settings block DMs from non-contacts, the warning can't be
  delivered — the bot logs this and moves on.
