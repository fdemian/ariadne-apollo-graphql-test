import asyncio

async def chat_generator(obj, info):
    for i in range(5):
        await asyncio.sleep(1)
        yield { 'text': 'A text' }


def chat_resolver(chat, info):
    return chat
