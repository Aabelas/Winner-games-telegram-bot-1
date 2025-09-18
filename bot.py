        [InlineKeyboardButton("🎮 Play Games", callback_data="play")],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        ],
        [
            InlineKeyboardButton("🎁 Bonus", callback_data="bonus"),
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
            InlineKeyboardButton("Next ▶️", callback_data="page2"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def kb_page2() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📞 Support", callback_data="support")],
        [InlineKeyboardButton("🚀 About", callback_data="about")],
        [InlineKeyboardButton("◀️ Back", callback_data="main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def kb_back_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back to Menu", callback_data="main")]])

def kb_deposit_methods() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📱 Telebirr", callback_data="deposit_tb")],
        [InlineKeyboardButton("🏦 Bank Transfer", callback_data="deposit_bank")],
        [InlineKeyboardButton("💎 USDT (TRC20)", callback_data="deposit_crypto")],
        [InlineKeyboardButton("◀️ Back", callback_data="main")],
    ]
    return InlineKeyboardMarkup(keyboard)

# =========================
# Helpers
# =========================
async def edit_or_reply(update: Update, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None):
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        except Exception:
            await update.effective_chat.send_message(text, reply_markup=reply_markup)
    else:
        await update.effective_chat.send_message(text, reply_markup=reply_markup)

def username_of(update: Update) -> str:
    u = update.effective_user
    return u.username or u.first_name or "Player"

# =========================
# Command Handlers
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username)
    await update.message.reply_text(
        "🎉 Welcome to *Winner Games*!\n\nChoose an option below:",
        reply_markup=kb_main(),
        parse_mode="Markdown",
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *Help Menu*\n\n"
        "• 💰 Deposit: see payment options\n"
        "• 🎁 Bonus: claim your daily reward\n"
        "• 👤 Profile: view your balance\n",
        reply_markup=kb_main(),
        parse_mode="Markdown",
    )

# =========================
# Callback (Buttons)
# =========================
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    ensure_user(user.id, user.username)
    data = query.data

    # Paging
    if data == "main":
        await edit_or_reply(update, "🏠 Main Menu:", kb_main())
        return
    if data == "page2":
        await edit_or_reply(update, "📂 More Options:", kb_page2())
        return

    # Play Mini App
    if data == "play":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 Open Winner Game", web_app=WebAppInfo(url="https://legendary-bavarois-04204e.netlify.app/"))],
            [InlineKeyboardButton("◀️ Back", callback_data="main")]
        ])
        await edit_or_reply(update, "🎮 Click below to open the mini app:", keyboard)
        return

    # Profile
    if data == "profile":
        info = get_user(user.id)
        uname = info["username"] or username_of(update)
        bal = info["balance"]
        await edit_or_reply(update, f"👤 Username: @{uname}\n💰 Balance: {bal} coins", kb_back_main())
        return

    # Stats
    if data == "stats":
        await edit_or_reply(update, "📊 Stats\n• Games played: 0\n• Win rate: 0%\n• Highest win: 0", kb_back_main())
        return

    # Help
    if data == "help":
        await edit_or_reply(
            update,
            "ℹ️ Help\n\nFor support, choose *Support* on the next page or contact the admin.\nUse Bonus daily to get free coins.",
            kb_back_main(),
        )
        return

    # About
    if data == "about":
        await edit_or_reply(update, "🚀 About Winner Games\nA simple mini-games hub with rewards and fair play.", kb_back_main())
        return

    # Support
    if data == "support":
        await edit_or_reply(update, "📞 Support\nMessage our support team: @YourSupportUsername", kb_back_main())
        return

    # Deposit flow
    if data == "deposit":
        await edit_or_reply(update, "💰 Choose a deposit method:", kb_deposit_methods())
        return

    if data == "deposit_tb":
        await edit_or_reply(
            update,
            "📱 *Telebirr Deposit*\n"
            "1) Open Telebirr and send to: `09xx-xxx-xxx`\n"
            "2) Amount: minimum 50 ETB\n"
            "3) After payment, tap *I've Paid* and send the receipt to support.\n\n"
            "⚠️ Manual verification required.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Paid", callback_data="paid_tb")],
                [InlineKeyboardButton("◀️ Back", callback_data="deposit")],
            ]),
            )
        return

    if data == "deposit_bank":
        await edit_or_reply(
            update,
            "🏦 *Bank Transfer*\nBank: XYZ Bank\nAccount: 123456789\nName: Winner Games\n\nSend and then tap *I've Paid*.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Paid", callback_data="paid_bank")],
                [InlineKeyboardButton("◀️ Back", callback_data="deposit")],
            ]),
        )
        return

    if data == "deposit_crypto":
        await edit_or_reply(
            update,
            "💎 *USDT (TRC20)*\nAddress: `TRxxx…xxxx`\n\nSend and then tap *I've Paid*.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Paid", callback_data="paid_crypto")],
                [InlineKeyboardButton("◀️ Back", callback_data="deposit")],
            ]),
        )
        return

    if data in {"paid_tb", "paid_bank", "paid_crypto"}:
        await edit_or_reply(
            update,
            "✅ Thanks! Please send your payment receipt to support.\nOnce confirmed, coins will be added to your balance.",
            kb_back_main(),
        )
        return

    # Daily bonus
    if data == "bonus":
        info = get_user(user.id)
        today = date.today().isoformat()
        if info["last_bonus"] == today:
            await edit_or_reply(update, "🎁 You already claimed today's bonus. Come back tomorrow!", kb_back_main())
        else:
            reward = 5
            add_balance(user.id, reward)
            set_last_bonus_today(user.id)
            await edit_or_reply(update, f"🎉 Bonus claimed! +{reward} coins added to your balance.", kb_back_main())
        return

# =========================
# Handle Web App Data
# =========================
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.web_app_data:
        data = update.message.web_app_data.data
        data_dict = json.loads(data)
        action = data_dict.get("action")
        value = data_dict.get("value")

        user = update.effective_user
        ensure_user(user.id, user.username)

        if action == "play":
            await update.effective_chat.send_message(f"🎮 You played the game! Score: {value}")
        elif action == "deposit":
            add_balance(user.id, int(value))
            await update.effective_chat.send_message(
                f"💰 Deposit received: {value} coins! Your new balance: {get_user(user.id)['balance']}"
            )
        else:
            await update.effective_chat.send_message(f"Received action: {action} | Value: {value}")

# =========================
# Unknown commands
# =========================
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "❌ Sorry, I didn't understand that command. Please use the menu buttons.",
            reply_markup=kb_main(),
        )

# =========================
# Main entrypoint
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("🤖 Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
