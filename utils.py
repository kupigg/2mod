from faust.types import TableT

from constants import list_of_censored_words


async def check_user_is_blocked(blocked_user_table: TableT, sender_id: int, recipient_id: int) -> bool:
    if sender_id in blocked_user_table[recipient_id]:
        return True
    return False


async def filter_message(message: str):
    for censored_word in list_of_censored_words:
        index = message.find(censored_word)
        if index != -1:
            len_censored_word = len(censored_word)
            message = f"{message[:index]}{len_censored_word*'*'}{message[index+len_censored_word:]}"
    return message