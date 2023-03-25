from channels.consumer import AsyncConsumer
import json

class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        print(text_data)
        print(text_data['text'])
        json_str = text_data['text']
        json_dict = json.loads(json_str)
        result = json.dumps(json_dict, ensure_ascii=False)
        print(type(result))
        if text_data['text'] == 'Hello from Js client':
            await self.send({
                "type": "websocket.send",
                "text": "Hello from Django socket"
            })
        else:
            await self.send({
                "type": "websocket.send",
                "text": "HI"
            })

    async def websocket_disconnect(self, event):
        pass