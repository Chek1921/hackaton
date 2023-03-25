from aiogram import types, executor, Dispatcher, Bot
import requests
import re
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from api import main_api
from handlers import states
from keyboards import beginBot, inputType, inlineChoice, emptyKeyboard


TOKEN = "6220388571:AAHYi2TR5B4-EPH1Jw_f6VINoJBJAK6JQrY"

auto_address = None
auto_state = 0

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


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


@dp.message_handler(commands=['Список_ваших_жалоб'])
async def createReport(message: types.Message):
    await message.answer('Жалобы будут позже')



if __name__ == '__main__':
    executor.start_polling(dp)