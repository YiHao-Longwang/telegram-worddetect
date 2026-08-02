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
    # --- Chinese escort / adult-service spam ---
    "下水",
    "修车",
    "水汇",
    "吉隆坡",
    "美女",
    "大奶",
    "骚货",

    # --- Add more Chinese spam words below ---

]

# Advanced regex patterns (optional). Leave [] if you don't need them.
# Example below flags messages containing any external link.
REGEX_PATTERNS = [
    # r"https?://(?!t\.me/yourgroup)\S+",   # any link that isn't your own group
]

# ---------------------------------------------------------------------------
# 2b. DEBUG LOGGING
# ---------------------------------------------------------------------------
# Turn these on only while testing. DEBUG_LOG_SKIPS explains why matching
# messages are ignored, such as when the sender is a bot.
DEBUG_LOG_SKIPS = True
DEBUG_LOG_ALL_MESSAGES = False

# ---------------------------------------------------------------------------
# 3. THE WARNING MESSAGE (sent to the user's DM)
# ---------------------------------------------------------------------------
# {name} is replaced with the user's first name.
WARNING_MESSAGE = (
    "💦 <b>吉隆坡 One SPA</b> 💦\n\n"
    "您好 {name}，看到你刚刚在群组里想找娱乐活动，推荐一家吉隆坡很受欢迎的下水店给你。\n\n"
    "环境舒适、各个国家来的美女都有 当然包括AV妹子🍑\n\n"
    "<b>想探索更多美女、价格和预约方式，可以点击下面的链接</b>\n"
    # 👇 EDIT THIS: change the URL and the label text between the tags
    "👉 <a href=\"https://t.me/kleznet168\">ONESPA高级水汇</a>"
)

# Optional image sent together with the warning (as the photo's caption).
# Put an image file in this folder and set its name here, e.g. "warning.jpg".
# Leave it as "" to send text only.
# NOTE: with an image, the text must be under ~1024 characters (yours is fine).
WARNING_IMAGE = "onespa.jpg"

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
