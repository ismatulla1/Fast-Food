from aiogram.types import Message,CallbackQuery,ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State

from database import delete_food, get_users, update_food_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



from database import (is_admin,is_new_foods,
                      is_progress_foods,update_order,
                      add_food,get_foods)

from .buttons import register_kb
from .admin_button import (admin_munu_text,admin_menu,
                           order_button,menu_for_food,
                            new_order_food,progress_order_food,
                            menu_food_button,edit_text,update_food)

from aiogram import Router

admin_router = Router()



@admin_router.message(Command("admin"))
async def start_admin(message:Message):
    chat_id = message.from_user.id

    user = is_admin(chat_id)

    if user:
        if user[-1]:
           
           await message.answer(text=admin_munu_text,reply_markup=admin_menu)
        else:
            await message.answer("Siz admin emassiz!!! 🙃")
    else:

        await message.answer("Siz Ro'yhatdan o'tmagansiz, Ro'yhatdan o'ting: ",reply_markup=register_kb)


@admin_router.message(F.text =="🧾 Buyurtmalar")
async def show_order(message: Message):
    text="""📦 Buyurtmalar bo‘limi:\nKerakli turini tanlang 👇"""

    await message.answer(text=text,reply_markup=order_button)


@admin_router.message(F.text =="🆕 New")
async def new_order(message:Message):
    foods = is_new_foods()

    for i in foods:
        await message.answer(
                text=f"🍽 Taom: {i[1]}\n"
                     f"👤 Foydalanuvchi: {i[2]}\n"
                     f"📦 Miqdor: {i[3]} ta\n"
                     f"💵 Narx: {i[4]} so'm\n"
                     f"💵 Umumiy narx: {i[5]:,} so‘m\n"
                     f"🆕 New\n",
                     reply_markup=new_order_food(i[0])
            )



@admin_router.message(F.text =="⏳ In Progress")
async def progress_order(message:Message):
    foods = is_progress_foods()

    for i in foods:
        await message.answer(
                text=f"🍽 Taom: {i[1]}\n"
                     f"👤 Foydalanuvchi: {i[2]}\n"
                     f"📦 Miqdor: {i[3]} ta\n"
                     f"💵 Narx: {i[4]} so'm\n"
                     f"💵 Umumiy narx: {i[5]:,} so‘m\n"
                     f"🆕 In Progress\n",
                     reply_markup=progress_order_food(i[0])
            )


@admin_router.callback_query(F.data.startswith("new_cancel"))
async def cancel_order(call:CallbackQuery):
    order_id = int(call.data.split("_")[-1])
    update_order(order_id)
  
    

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.edit_text(text="success")



@admin_router.message(F.text=="🍱 Taomlar")
async def menu_foods(message:Message,state:FSMContext):
    await state.clear() 
    await message.answer(text=menu_for_food,reply_markup=menu_food_button)


class CreateFood(StatesGroup):
    name = State()
    desc = State()
    image = State()
    price = State()
    quantity = State()

# create 
@admin_router.message(F.text =="🆕 Create")
async def start_add_food(message:Message,state:FSMContext):
    await state.set_state(CreateFood.name)
    await message.answer("Taom nomini kiriting: ",reply_markup=ReplyKeyboardRemove())


@admin_router.message(CreateFood.name)
async def get_food_name(message:Message,state:FSMContext):
    await state.update_data(name =message.text)
    await state.set_state(CreateFood.desc)

    await message.answer("Taomga izoh qoldiring: ")


@admin_router.message(CreateFood.desc)
async def get_food_desc(message:Message,state:FSMContext):
    if len(message.text)<500:
        await state.update_data(desc =message.text)
        await state.set_state(CreateFood.image)

        await message.answer("Taom rasmini yuboring : ")
    else:
        await message.answer("Taomga izoh uzunligi bir oz ko'proq, qayta kiriting:  ")


@admin_router.message(CreateFood.image)
async def get_food_image(message:Message,state:FSMContext):
    try:
        image = message.photo[-1]

        file =  await message.bot.get_file(image.file_id)
        food = await state.get_data()
        food_name = food.get("name")
        

        file_path = f"images/{food_name}.jpg"

        await message.bot.download_file(file_path=file.file_path,destination=file_path)

        await state.update_data(image=file_path)
        await state.set_state(CreateFood.price)

        await message.answer("Taom narxini kiriting: ")
    except:

        await message.answer(f"Image yuklshda qandaydir muammo bor , qayta yuboring: ")


@admin_router.message(CreateFood.price)
async def get_food_price(message:Message,state:FSMContext):
    try:
        if message.text.isdigit():
            price = message.text
            await state.update_data(price =price)
            await state.set_state(CreateFood.quantity)

            await message.answer("Taom miqdorini yuboring: ")
        else:
            await message.answer("Taom naxi raqam bo'lishi kerak , qayta kiriting:  ")
        
    except:
       await message.answer("Taom naxi yuborishda muammo bor , qayta kirting")


@admin_router.message(CreateFood.quantity)
async def get_food_quantity(message:Message,state:FSMContext):
    if message.text.isdigit():

        await state.update_data(quantity =message.text)
        data = await state.get_data()
        await state.clear()
        add_food(data)

        await message.answer("Taom muofaqiyatli saqlandi. ",reply_markup=menu_food_button)
    else:
         await message.answer("Taom miqdori raqam bo'lishi kerak , qayta kiriting:  ")



@admin_router.message(F.text =="✏️ Update")
async def  update_food_start(message:Message):

    await message.answer(text=edit_text)
    
    for i in get_foods():
        await message.answer(text=str(i[1]),reply_markup=update_food(i[0]))


# 🗑 Taom o‘chirish
@admin_router.message(F.text == "🗑 Delete")
async def delete_foods(message: Message):
    foods = get_foods()
    if foods:
        await message.answer("O‘chirmoqchi bo‘lgan taomni tanlang:")
        for food in foods:
            await message.answer(
                text=f"🍽 {food[1]} - {food[3]} so‘m",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(
                            text="❌ O‘chirish",
                            callback_data=f"delete_food_{food[0]}"
                        )]
                    ]
                )
            )
    else:
        await message.answer("Hozircha taomlar mavjud emas.")


@admin_router.callback_query(F.data.startswith("delete_food_"))
async def confirm_delete(call: CallbackQuery):
    food_id = int(call.data.split("_")[-1])
    delete_food(food_id)
    await call.message.edit_text("✅ Taom o‘chirildi.")


# 📋 Taomlar ro‘yxatini ko‘rish
@admin_router.message(F.text == "📋 List")
async def list_foods(message: Message):
    foods = get_foods()
    if foods:
        text = "🍱 Taomlar ro‘yxati:\n\n"
        for f in foods:
            text += f"ID: {f[0]} | 🍽 {f[1]} | 💵 {f[3]} so‘m | 📦 {f[4]} dona\n"
        await message.answer(text)
    else:
        await message.answer("Hozircha taomlar mavjud emas.")


# ✏️ Taom o‘zgartirish
class UpdateFood(StatesGroup):
    food_id = State()
    price = State()
    quantity = State()


@admin_router.callback_query(F.data.startswith("update_food_"))
async def start_update_food(call: CallbackQuery, state: FSMContext):
    food_id = int(call.data.split("_")[-1])
    await state.set_state(UpdateFood.food_id)
    await state.update_data(food_id=food_id)
    await call.message.answer("Yangi narxni kiriting:")


@admin_router.message(UpdateFood.food_id)
async def set_new_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=int(message.text))
        await state.set_state(UpdateFood.price)
        await message.answer("Yangi miqdorni kiriting:")
    else:
        await message.answer("Narx raqam bo‘lishi kerak.")


@admin_router.message(UpdateFood.price)
async def set_new_quantity(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(quantity=int(message.text))
        data = await state.get_data()
        update_food_data(data["food_id"], data["price"], data["quantity"])
        await state.clear()
        await message.answer("✅ Taom muvaffaqiyatli yangilandi.")
    else:
        await message.answer("Miqdor raqam bo‘lishi kerak.")


# 👥 Foydalanuvchilarni ko‘rish
@admin_router.message(F.text == "👥 Users")
async def list_users(message: Message):
    users = get_users()
    if users:
        text = "👥 Foydalanuvchilar ro‘yxati:\n\n"
        for u in users:
            text += f"ID: {u[0]} | 👤 {u[1]} | 📱 {u[2]}\n"
        await message.answer(text)
    else:
        await message.answer("Hozircha foydalanuvchilar mavjud emas.")









  




