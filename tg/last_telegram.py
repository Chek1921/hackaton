from aiogram import types, executor, Dispatcher, Bot
import requests
import re
import ast
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import asyncio
from websockets import connect
import json
from aiogram.utils import exceptions as tg_exceptions
import websockets

from api import main_api
from handlers import states
from keyboards import beginBot, inputType, inlineChoice, emptyKeyboard, ratingReply


TOKEN = "6220388571:AAHYi2TR5B4-EPH1Jw_f6VINoJBJAK6JQrY"

auto_address = None
auto_state = 0

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

##########################

async def send_message_to_django(message):
    async with connect('wss://26.76.95.107:8000/wss') as websocket:
        data = {'message': message}
        await websocket.send(json.dumps(data))
        # response = await websocket.recv()
        # response_data = json.loads(response)
        # return response_data

async def receive_message(message):
    try:
        await bot.send_message(chat_id=message.chat.id, text=message)
    except tg_exceptions.ChatNotFound:
        print('Chat not found')

async def websocket_handler():
    async with websockets.connect('ws://26.76.95.107:8000/ws') as websocket:
        while True:
            message = await websocket.recv()
            await receive_message(message)


async def start_bot():
    await dp.start_polling()

async def start():
    await asyncio.gather(start_bot(), websocket_handler())



##########################

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await message.answer('Что вы хотите сделать?', reply_markup=beginBot)


@dp.message_handler(commands=['Создать'])
async def createReport(message: types.Message):
    await message.answer('Укажите адрес', reply_markup=inlineChoice)

@dp.callback_query_handler(text='auto')
async def autoAdress(callback : types.CallbackQuery):
    await callback.answer('OK')
    await callback.message.answer('Нажмите кнопку ниже', reply_markup=inputType)
    

@dp.callback_query_handler(text='manual')
async def autoAdress(callback : types.CallbackQuery):
    await callback.answer('OK')
    await callback.message.answer('Введите ваш адрес')
    await states.UserStates.adress_state.set()


@dp.message_handler(state=states.UserStates.adress_state)
async def addressManual(message: types.Message, state: FSMContext):
    global auto_state
    auto_state = 0
    async with state.proxy() as data:
        data['address'] = message.text
    print('BBBBBBBBBBBBBBB', message.text)
    
    await message.reply('Теперь опишите свою проблему:')
    await states.UserStates.next()


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    global auto_address
    global auto_state
    auto_state = 1
    lat = message.location.latitude
    lon = message.location.longitude
    reply = main_api.get_locations(lat, lon, message.from_user.id)
    print(type(reply))
    
    auto_address = main_api.rename_auto(reply)
    print('AAAAAAAAAAAAAAAAAAAA', auto_address)
    await message.answer(f'Ваш адрес: {auto_address}')
    await message.reply('Теперь опишите свою проблему:', reply_markup=emptyKeyboard)

    await states.UserStates.problem_state.set()


@dp.message_handler(state=states.UserStates.problem_state)
async def addressManual(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['report'] = message.text

    if auto_state == 1:
        main_api.post_data(auto_address, data['report'], message.chat.id)
        print('AUTOO')
    elif auto_state == 0:
        main_api.post_data(data['address'], data['report'], message.chat.id)
        print('MANUAL')

    await message.reply('Спасибо, ожидайте!', reply_markup=beginBot)
    await state.finish()

@dp.message_handler(commands=['Список_жалоб'])
async def createReport(message: types.Message):
    messages = main_api.get_data(message.from_user.id)
    for user_message in messages:
        await message.answer(user_message)

answers = dict()

@dp.callback_query_handler(Text(startswith='rate'))
async def createRating(callback : types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    id = callback.data.split('_')[2]
    answers = ast.literal_eval(open("answers.txt","r").read())
    if id not in answers:
        await callback.answer('Вы успешно поставили оценку')        
        answers[id] = res
        open("answers.txt","w").write(str(answers))
        main_api.post_rating(res, id)
    else:
        await callback.answer('Вы уже оценивали эту услугу', show_alert=True)
    print(answers)
    




if __name__ == '__main__':
    asyncio.run(start())