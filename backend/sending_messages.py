import collections
import vk_api
from cfg.config import bot_group_id, user_token


def info(id_post, vid):
    vk = vk_api.VkApi(token=user_token)
    api = vk.get_api()

    try:
        id_users = []
        if vid == "Лайк" or vid == "Всё вместе":
            id_users_all = api.likes.getList(type="post", owner_id=bot_group_id, item_id=id_post)["items"]
            for a in id_users_all:
                id_users.append(a)

        if vid == "Комментарий" or vid == "Всё вместе":
            id_users_all_info = api.wall.getComments(owner_id=bot_group_id, post_id=1)["items"]
            for a in id_users_all_info:
                id_users.append(a["from_id"])

        if vid == "Репост" or vid == "Всё вместе":
            id_users_all_info = api.wall.getReposts(owner_id=bot_group_id, post_id=1)["items"]
            for a in id_users_all_info:
                id_users.append(a["from_id"])

        if vid == "Всё вместе":
            id_users = [item for item, count in collections.Counter(id_users).items() if count == 3]

    except:
        id_users = "Ошибка"

    return id_users


def info_opros(number_opros):
    text = []
    id_opros = []

    try:
        vk = vk_api.VkApi(token=user_token)
        api = vk.get_api()

        info_opr = api.polls.getById(owner_id=bot_group_id, poll_id=number_opros)["answers"]
        for a in info_opr:
            text.append(a["text"])
            id_opros.append(a["id"])
    except:
        text.append("Ошибка")

    return text, id_opros


def opros_users(number_opros, id_opros):
    id_users = []
    try:
        vk = vk_api.VkApi(token=user_token)
        api = vk.get_api()

        users_opros = api.polls.getVoters(owner_id=bot_group_id, poll_id=number_opros, answer_ids=id_opros)
        for a in users_opros[0]["users"]["items"]:
            id_users.append(a)

    except:
        id_users.append("Ошибка")

    return id_users
