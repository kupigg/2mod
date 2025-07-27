import faust

from faust.types import TopicT

from constants import chat_messages
from utils import check_user_is_blocked, filter_message


app = faust.App(
    "simple-faust-app",
    broker="localhost:19092"
)

blocked_user_table = app.Table(
    "blocked_user_table",
    partitions=1,
    default=list
)


class Message(faust.Record):
    sender_id: int
    recipient_id: int
    message: str


class BlockUser(faust.Record):
    user_who_blocked: int
    blocked_user: int


messages_topic = app.topic("messages", value_type=Message)
filtered_messages_topic = app.topic("filtered-topic", key_type=str, value_type=Message)
blocked_users_topic = app.topic("blocked-user-topic", key_type=str, value_type=BlockUser)


@app.agent(messages_topic)
async def process_message(stream):
    async for message in stream:
        is_blocked = await check_user_is_blocked(blocked_user_table, message.sender_id, message.recipient_id)
        if not is_blocked:
            filtered_message = await filter_message(message.message)
            await filtered_messages_topic.send(value=Message(sender_id=message.sender_id, recipient_id=message.recipient_id, message=filtered_message))
            continue


@app.agent(blocked_users_topic)
async def process_block_users(stream):
    async for message in stream:
        block_users_log = blocked_user_table.get(message.user_who_blocked) or []
        block_users_log.append(message.blocked_user)
        blocked_user_table[message.user_who_blocked] = block_users_log


@app.task
async def send_test_messages():
    for message in chat_messages:
        message_obj = Message(**message)
        await messages_topic.send(value=message_obj)


@app.task
async def send_test_blocked_user():
    await blocked_users_topic.send(value=BlockUser(user_who_blocked=101, blocked_user=202))
    await blocked_users_topic.send(value=BlockUser(user_who_blocked=101, blocked_user=404))


@app.task
async def send_test_messages2():
    for message in chat_messages:
        message_obj = Message(**message)
        await messages_topic.send(value=message_obj)