from vkbottle import Keyboard, KeyboardButtonColor, Text


admin_start = (
    Keyboard(one_time=False, inline=True)
    .add(Text("Добавить пост"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Посмотреть добавленные посты"))
).get_json()

what_post = (
    Keyboard(one_time=False, inline=True)
    .add(Text("Публикация"))
    .add(Text("Опросник"))
    .row()
    .add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)
).get_json()

otmena = (
    Keyboard(one_time=False, inline=True)
    .add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)
).get_json()

deistvie = (
    Keyboard(one_time=False, inline=True)
    .add(Text("Лайк"))
    .add(Text("Комментарий"))
    .add(Text("Репост"))
    .add(Text("Всё вместе"))
    .row()
    .add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)
).get_json()

BUTTON_TYPES = {
    "BTN_ADMIN_START": admin_start,
    "BTN_WHAT_POST": what_post,
    "BTN_OTMENA": otmena,
    "BTN_DEISTVIE": deistvie,
}



