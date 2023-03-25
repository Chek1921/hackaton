from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup 


class AdressStates(StatesGroup):
    auto_state = State()
    manual_state = State()


class UserStates(StatesGroup):
    adress_state = State()
    problem_state = State()
    third_state = State()
    fourth_state = State()



