from aiogram.fsm.state import State, StatesGroup

class AddNote(StatesGroup):
    day_ = State()
    time_ = State()
    avto = State()
    success = State()