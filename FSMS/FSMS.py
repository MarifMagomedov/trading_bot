from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage, Redis


# redis = Redis(host='localhost')
# storage = RedisStorage(redis=redis)
storage = MemoryStorage()


class MenuSG(StatesGroup):
    main_menu = State()
    choose_crypto = State()
    buy_or_sell = State()


class BuySG(StatesGroup):
    buy_value = State()
    accept_buy = State()


class SellSG(StatesGroup):
    sell_value = State()
    accept_sell = State()


class BriefcaseSG(StatesGroup):
    choose_crypto = State()