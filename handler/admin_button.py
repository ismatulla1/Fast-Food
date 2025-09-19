from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# === ASOSIY ADMIN MENYU ===
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧾 Buyurtmalar"),
            KeyboardButton(text="🍱 Taomlar")
        ],
        [
            KeyboardButton(text="👥 Foydalanuvchilar"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# === BUYURTMALAR TUGMALARI ===
order_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🆕 New")],
        [KeyboardButton(text="⏳ In Progress")],
        [KeyboardButton(text="✅ Finished")],
        [KeyboardButton(text="🔙 Back")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# === TAOMLAR MENYUSI ===
menu_food_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🆕 Create"),
            KeyboardButton(text="✏️ Update"),
        ],
        [
            KeyboardButton(text="❌ Delete"),
            KeyboardButton(text="📋 Read"),
        ],
        [
            KeyboardButton(text="🔙 Back"),
        ]
    ],
    resize_keyboard=True
)


# === INLINE BUTTONLAR ===
def new_order_food(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Cancel", callback_data=f"new_cancel_{order_id}"),
                InlineKeyboardButton(text="✅ In Progress", callback_data=f"new_send_{order_id}")
            ]
        ]
    )


def progress_order_food(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Cancel", callback_data=f"progress_cancel_{order_id}"),
                InlineKeyboardButton(text="🏁 Finished", callback_data=f"progress_send_{order_id}")
            ]
        ]
    )


def update_food(food_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📷 Rasmni o‘zgartirish", callback_data=f"edit_image_{food_id}"),
                InlineKeyboardButton(text="🍽 Nomini o‘zgartirish", callback_data=f"edit_name_{food_id}")
            ],
            [
                InlineKeyboardButton(text="💵 Narxni o‘zgartirish", callback_data=f"edit_price_{food_id}"),
                InlineKeyboardButton(text="📄 Tavsifni o‘zgartirish", callback_data=f"edit_desc_{food_id}")
            ],
            [
                InlineKeyboardButton(text="🛒 Miqdorini o‘zgartirish", callback_data=f"edit_quantity_{food_id}")
            ]
        ]
    )


# === TEXTLAR ===
admin_menu_text = """
✅ Siz muvaffaqiyatli Admin panelga kirdingiz!
Bu bo‘lim orqali siz quyidagi amallarni bajarishingiz mumkin:

🍔 Yangi taom qo‘shish
✏️ Taomlarni tahrirlash yoki o‘chirish
📊 Buyurtmalarni ko‘rish va boshqarish
👥 Foydalanuvchilarni kuzatish
"""

menu_for_food_text = """
🍱 Menyu boshqaruv bo‘limi:

🆕 Yangi taom qo‘shish (Create)
✏️ Taom ma’lumotlarini o‘zgartirish (Update)
❌ Taomni o‘chirish (Delete)
📋 Barcha taomlarni ko‘rish (Read)
🔙 Orqaga qaytish (Back)
"""

edit_food_text = """
🔧 Taomni tahrirlash bo‘limi:

📝 Nomi – taom nomini o‘zgartirish
💵 Narxi – taom narxini yangilash
🖼 Rasmi – yangi surat yuklash
📋 Tavsifi – taom tavsifini yangilash
🛒 Miqdorini – yangilash
"""
