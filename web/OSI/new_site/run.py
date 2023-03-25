import asyncio
from consumers import ChatConsumer

asyncio.run(ChatConsumer.chat_message('testTEST'))