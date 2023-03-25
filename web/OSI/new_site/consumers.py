from channels.consumer import AsyncConsumer
from .models import *
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import exceptions as tg_exceptions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "6220388571:AAHYi2TR5B4-EPH1Jw_f6VINoJBJAK6JQrY"

bot = Bot(TOKEN)
dp = Dispatcher(bot)


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']
        chat_id = text_data_json['chat_id']
        rate = text_data_json['rate']
        id = text_data_json['id']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': id,
                'message': message,
                'chat_id': chat_id,
                'rate': rate
            }
        )

    async def chat_message(self, event):
        message = event['message']
        chat_id = event['chat_id']
        rate = event['rate']
        id = event['id']
        rate1 = InlineKeyboardButton(text='1/5', callback_data=f'rate_1_{id}')
        rate2 = InlineKeyboardButton(text='2/5', callback_data=f'rate_2_{id}')
        rate3 = InlineKeyboardButton(text='3/5', callback_data=f'rate_3_{id}')
        rate4 = InlineKeyboardButton(text='4/5', callback_data=f'rate_4_{id}')
        rate5 = InlineKeyboardButton(text='5/5', callback_data=f'rate_5_{id}')
        ratingReply = InlineKeyboardMarkup().row(rate1, rate2, rate3, rate4, rate5)
        try:
            if rate == True:
                await bot.send_message(chat_id=chat_id, text=f'{message} \n Спасибо за обращение!', reply_markup=ratingReply)
            else: 
                await bot.send_message(chat_id=chat_id, text=f'{message}')
        except tg_exceptions.ChatNotFound:
            print('Chat not found')