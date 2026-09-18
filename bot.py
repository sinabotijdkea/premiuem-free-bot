
import os
import json
import logging
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# تنظیمات
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
SUPPORT = "m616281"

DATA_FILE = Path("data.json")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# سرویس‌ها
# =========================

PRODUCTS = {
    "v2ray": {
        "name": "🔥 کانفیگ ویتوری",
        "plans": [
            ("10 گیگ", 90),
            ("20 گیگ", 190),
            ("30 گیگ", 280),
            ("40 گیگ", 350),
            ("50 گیگ", 500),
        ],
    },
    "wireguard": {
        "name": "⚡ WireGuard",
        "plans": [
            ("5 گیگ", 60),
            ("10 گیگ", 120),
            ("15 گیگ", 180),
            ("20 گیگ", 250),
        ],
    },
    "dns": {
        "name": "🌐 DNS",
        "plans": [
            ("پلن DNS", 149),
        ],
    },
}


def load_data():
    if not DATA_FILE.exists():
        return {"users": [], "orders": []}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": [], "orders": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =========================
# منوی اصلی
# =========================

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛒 خرید سرویس", callback_data="products")
        ],
        [
            InlineKeyboardButton("📦 سفارش‌های من", callback_data="orders"),
            InlineKeyboardButton("💬 پشتیبانی", callback_data="support")
        ],
        [
            InlineKeyboardButton("ℹ️ درباره ربات", callback_data="about")
        ]
    ])


# =========================
# شروع ربات
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    data = load_data()

    if user.id not in data["users"]:
        data["users"].append(user.id)
        save_data(data)

    text = (
        f"سلام {user.first_name} 👋\n\n"
        "🌟 به Premium Free Bot خوش آمدید.\n\n"
        "از منوی زیر گزینه موردنظر خود را انتخاب کنید:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


# =========================
# نمایش سرویس‌ها
# =========================

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = []

    for key, product in PRODUCTS.items():
        buttons.append([
            InlineKeyboardButton(
                product["name"],
                callback_data=f"product:{key}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("🔙 برگشت", callback_data="home")
    ])

    await query.edit_message_text(
        "🛒 سرویس موردنظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# =========================
# نمایش پلن‌ها
# =========================

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    key = query.data.split(":")[1]

    if key not in PRODUCTS:
        return

    item = PRODUCTS[key]

    buttons = []

    for i, (plan, price) in enumerate(item["plans"]):
        buttons.append([
            InlineKeyboardButton(
                f"{plan} | {price} هزار تومان",
                callback_data=f"buy:{key}:{i}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("🔙 برگشت", callback_data="products")
    ])

    await query.edit_message_text(
        f"{item['name']}\n\n"
        "📋 پلن موردنظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# =========================
# ثبت سفارش
# =========================

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query
