"""
Edit this file to control what the bot watches for and how it reacts.
No coding needed beyond changing the values below.
"""

# ---------------------------------------------------------------------------
# 1. WHICH GROUP(S) TO WATCH
# ---------------------------------------------------------------------------
# Use the group's @username (e.g. "mycoolgroup") or its numeric id.
# Leave the list empty [] to watch EVERY group the account is in (not recommended).
WATCH_GROUPS = [
    "sousuozan",     # https://t.me/sousuozan
    "sobaidu666",    # https://t.me/sobaidu666
]

# ---------------------------------------------------------------------------
# 2. WHAT COUNTS AS SUSPICIOUS
# ---------------------------------------------------------------------------
# Plain keywords — matched anywhere in the message, case-insensitive.
# Grouped by category so you can delete whole sections you don't need.
KEYWORDS = [
    # --- Crypto / investment scams ---
    "free crypto",
    "airdrop",
    "double your",
    "double your money",
    "investment opportunity",
    "guaranteed profit",
    "guaranteed returns",
    "passive income",
    "trading signals",
    "pump and dump",
    "pump group",
    "mining rewards",
    "claim your reward",
    "claim your tokens",
    "elon musk giveaway",
    "usdt giveaway",
    "bitcoin giveaway",
    "10x returns",
    "100x gem",
    "forex trading",
    "binary options",

    # --- Recruitment / job scams ---
    "earn from home",
    "work from home",
    "earn $",
    "make money online",
    "part time job",
    "daily payout",
    "easy money",
    "hiring now",
    "join my team",

    # --- Contact / redirection bait ---
    "dm me",
    "dm me for",
    "pm me",
    "message me privately",
    "click here",
    "click the link",
    "check my bio",
    "check bio",
    "link in bio",
    "whatsapp me",
    "contact admin",

    # --- Suspicious links / invites ---
    "t.me/joinchat",
    "t.me/+",
    "bit.ly/",
    "tinyurl",
    "cutt.ly",

    # --- Adult / spam ---
    "hot singles",
    "onlyfans",
    "sex",
    "nude",
    "18+",

    # --- Chinese escort / adult-service spam ---
    "下水",
    "修车",
    "水汇",
    "吉隆坡",
    "美女",
    "大奶",
    "骚货",

    # --- Add your own group-specific spam words below ---

]

# Advanced regex patterns (optional). Leave [] if you don't need them.
# Example below flags messages containing any external link.
REGEX_PATTERNS = [
    # r"https?://(?!t\.me/yourgroup)\S+",   # any link that isn't your own group
]

# ---------------------------------------------------------------------------
# 3. THE WARNING MESSAGE (sent to the user's DM)
# ---------------------------------------------------------------------------
# {name} is replaced with the user's first name.
WARNING_MESSAGE = (
    "Hi {name}, this is an automated moderation notice from the group.\n\n"
    "Your recent message looked like spam or was flagged by our filters. "
    "Please avoid posting promotional links or scam-like content — "
    "repeated violations will lead to a ban.\n\n"
    "If this was a mistake, just ignore this message."
)

# ---------------------------------------------------------------------------
# 4. SAFETY LIMITS (keep these sane to avoid your account being flagged)
# ---------------------------------------------------------------------------
COOLDOWN_HOURS = 6        # don't warn the same person more than once per this many hours
MAX_DMS_PER_DAY = 30      # hard stop on total DMs per day across everyone
DELAY_BETWEEN_DMS = 4     # seconds to wait after each DM (looks more human)

# ---------------------------------------------------------------------------
# 5. OPTIONAL ENFORCEMENT (only works if the account is a group admin)
# ---------------------------------------------------------------------------
DELETE_MESSAGE = False    # True = delete the offending message
MUTE_USER = False         # True = mute the user in the group
MUTE_MINUTES = 60         # how long to mute for, if MUTE_USER is True
