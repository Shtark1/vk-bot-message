from vkbottle.bot import Bot, Message
from vkbottle import BaseStateGroup, CtxStorage
from cfg.config import bot_token, user_id, url_group
from backend.keyboard import BUTTON_TYPES
from backend.sending_messages import info, info_opros, opros_users
from database.database import Database


vk = Bot(bot_token)
bot = Bot(token=bot_token)
ctx = CtxStorage()
db = Database('database/database')


class SuperStates(BaseStateGroup):
    AWKWARD_STATE = 0
    ADD_POST = 1
    PUBLIK = 2
    OPROS = 3
    ACTION_PUBLIK = 4
    TEXT_PUBLIK = 5
    TEXT_OPROS = 6
    LOOK_ADD = 7


@bot.on.message(state=SuperStates.AWKWARD_STATE)
async def awkward_handler(message: Message):
    if message.text == "Добавить пост":
        await bot.state_dispenser.set(message.peer_id, SuperStates.ADD_POST)
        await message.answer(keyboard=BUTTON_TYPES["BTN_WHAT_POST"], message="Выбери какой тип поста ты хочешь добавить")

    elif message.text == "Посмотреть добавленные посты":

        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        all_added = db.viewing_post()
        print(all_added)
        for i in all_added:
            if i[3] == "Публикация":
                await message.answer(message=f"Ссылка на пост: {url_group}{i[0]}\nКол-во доставленных СМС: {i[1]}\nКол-во не полученных СМС: {i[2]}")
            else:
                await message.answer(message=f"Ссылка на опрос: {url_group}{i[0]}\nКол-во доставленных СМС: {i[1]}\nКол-во не полученных СМС: {i[2]}")

        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Это все посты которые ты добавлял\nПривет, Админ")

    else:
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Такой команды нет(")


# ====================================================================================
# ================================= ДОБАВЛЕНИЕ ПОСТА =================================
# ====================================================================================
@bot.on.message(state=SuperStates.ADD_POST)
async def awkward_handler(message: Message):
    if message.text == "Публикация":
        await bot.state_dispenser.set(message.peer_id, SuperStates.PUBLIK)
        await message.answer(keyboard=BUTTON_TYPES["BTN_OTMENA"], message="Введи номер записи:")

    elif message.text == "Опросник":
        await bot.state_dispenser.set(message.peer_id, SuperStates.OPROS)
        await message.answer(keyboard=BUTTON_TYPES["BTN_OTMENA"], message="Введите номер опросника:")

    elif message.text == "Отмена":
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")

    else:
        await bot.state_dispenser.set(message.peer_id, SuperStates.ADD_POST)
        await message.answer(keyboard=BUTTON_TYPES["BTN_WHAT_POST"], message="Такой команды нет(")


# ================================= ПУБЛИКАЦИЯ =================================
@bot.on.message(state=SuperStates.PUBLIK)
async def awkward_handler(message: Message):
    if message.text == "Отмена":
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")

    else:
        ctx.set("number_post", message.text)
        await bot.state_dispenser.set(message.peer_id, SuperStates.ACTION_PUBLIK)
        await message.answer(keyboard=BUTTON_TYPES["BTN_DEISTVIE"], message="Выбери действие которое должен сделать пользователь!")


@bot.on.message(state=SuperStates.ACTION_PUBLIK)
async def awkward_handler(message: Message):
    if message.text == "Отмена":
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")

    elif message.text == "Лайк" or message.text == "Комментарий" or message.text == "Репост" or message.text == "Всё вместе":
        ctx.set("action_vid", message.text)
        await bot.state_dispenser.set(message.peer_id, SuperStates.TEXT_PUBLIK)
        await message.answer(keyboard=BUTTON_TYPES["BTN_OTMENA"], message="Напишите текст который будут получать пользователи")

    else:
        await bot.state_dispenser.set(message.peer_id, SuperStates.ACTION_PUBLIK)
        await message.answer(keyboard=BUTTON_TYPES["BTN_DEISTVIE"], message="Такой команды нет(")


@bot.on.message(state=SuperStates.TEXT_PUBLIK)
async def awkward_handler(message: Message):
    if message.text == "Отмена":
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")

    else:
        id_post = ctx.get("number_post")
        vid = ctx.get("action_vid")
        id_user_send = info(id_post, vid)
        if id_user_send == "Ошибка":
            await message.answer(message=f"Такого поста нет(")

        else:
            i=0
            i2=0
            for a in id_user_send:
                try:
                    await bot.api.messages.send(peer_id=a, random_id=0, message=message.text)
                    i+=1
                except:
                    i2+=1
                    print(a, "Ему нельзя отправить соообщение")
            await message.answer(message=f"Пост был добавлен!!!")
            db.add_post(id_post, i, i2, "Публикация")

        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")


# ================================= Опросник =================================
@bot.on.message(state=SuperStates.OPROS)
async def awkward_handler(message: Message):
    if message.text == "Отмена":
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")

    else:
        number_now = ctx.get("number_now")
        if number_now is None:
            ctx.set("number_now", 1)
            text_opr = info_opros(message.text)
            ctx.set("pool_id", message.text)
            ctx.set("all_info_opros", text_opr)

        number_now = ctx.get("number_now")
        text_opr = ctx.get("all_info_opros")

        if text_opr[0][0] != "Ошибка":
            number_of_options = len(text_opr[0])

            if number_now <= number_of_options:
                await bot.state_dispenser.set(message.peer_id, SuperStates.OPROS)
                await message.answer(keyboard=BUTTON_TYPES["BTN_OTMENA"], message=f"Введи текст для ответа на:\n{text_opr[0][number_now - 1]}")

                if number_now != 1:
                    id_users = opros_users(ctx.get("pool_id"), text_opr[1][number_now-2])
                    i = 0
                    i2 = 0
                    for a in id_users:
                        try:
                            i+=1
                            await bot.api.messages.send(peer_id=a, random_id=0, message=message.text)
                        except:
                            i2+=1
                            print(a, "Ему нельзя отправить соообщение")
                    db.add_post(ctx.get("pool_id"), i, i2, "Опросник")
                ctx.set("number_now", number_now+1)

            else:
                await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Все текста были отправлены!\nПривет, Админ")
                await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)

        else:
            await bot.state_dispenser.set(message.peer_id, SuperStates.OPROS)
            await message.answer(keyboard=BUTTON_TYPES["BTN_OTMENA"], message="Такого опросника нет(\nПопробуйте снова ввести номер опросника:")


# ====================================================================================
# =================================  НАЧАЛО ОБЩЕНИЯ  =================================
# ====================================================================================
@bot.on.message(text=["Начать", "Привет", "a"])
async def die_handler(message: Message):
    if message.from_id in user_id:
        await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
        await message.answer(keyboard=BUTTON_TYPES["BTN_ADMIN_START"], message="Привет, Админ")

    else:
        users_info = await bot.api.users.get(message.from_id)
        await message.answer("Привет, {}".format(users_info[0].first_name))


@bot.on.message()
async def die_handler(message: Message):
    if message.from_id in user_id:
        users_info = await bot.api.users.get(message.from_id)
        await message.answer('Для входа в админку, напиши мне "Начать", "Привет" или "a"'.format(users_info[0].first_name))


def start():
    bot.run_forever()
