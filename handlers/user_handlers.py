from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.users import (create_profile, get_balance, shop,
                            get_brief_case, sell, get_user_statistics)
from lexicon.lexicon_ru import (lexicon_ru, menu_buttons_lexicon,
                                accept_buttons, buy_or_sell_buttons)
from keyboards.keyboards import (menu_keyboard, markets_keyboard, buy_or_sell_keyboard,
                                 accept_keyboard, back_to_menu_keyboard, backs_keyboard,
                                 user_brief_keyboard)
from FSMS.FSMS import MenuSG, BuySG, SellSG, BriefcaseSG
from services.trade_functions import get_crypto_price

router = Router()
states = []


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        text=lexicon_ru['help']
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(MenuSG.main_menu)
    await create_profile(user_id)
    await message.answer(
        text=lexicon_ru['main_menu'],
        reply_markup=menu_keyboard()
    )


@router.callback_query(F.data == lexicon_ru['back_to_menu'])
async def cmd_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(MenuSG.main_menu)
    await callback.message.edit_text(
        text=lexicon_ru['main_menu'],
        reply_markup=menu_keyboard()
    )


@router.callback_query(F.data == accept_buttons['back'])
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states[-1]['state'])
    await callback.message.edit_text(
        text=states[-1]['text'],
        reply_markup=states[-1]['reply_markup']
    )
    states.pop(-1)


@router.callback_query(MenuSG.main_menu, F.data == menu_buttons_lexicon['markets'])
async def cmd_markets(callback: CallbackQuery, state: FSMContext):
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': callback.message.reply_markup,
        'text': callback.message.text
    }
    states.append(prev_state)
    await state.set_state(MenuSG.choose_crypto)
    await state.update_data(prev_state={state: await state.get_state()})
    await callback.message.edit_text(
        text=lexicon_ru['crypto_names'],
        reply_markup=markets_keyboard()
    )


@router.callback_query(MenuSG.choose_crypto)
async def cmd_buy_crypto(callback: CallbackQuery, state: FSMContext):
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': callback.message.reply_markup,
        'text': callback.message.text
    }
    states.append(prev_state)
    data = callback.data.split(':')
    await state.update_data(crypto=data[1], price=float(data[-1]))
    await state.set_state(MenuSG.buy_or_sell)
    await callback.message.edit_text(
        text=lexicon_ru['buy_or_sell'],
        reply_markup=buy_or_sell_keyboard()
    )


@router.callback_query(MenuSG.buy_or_sell, F.data == buy_or_sell_buttons['buy'])
async def cmd_buy(callback: CallbackQuery, state: FSMContext):
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': callback.message.reply_markup,
        'text': callback.message.text
    }
    states.append(prev_state)
    await state.set_state(BuySG.buy_value)
    data = await state.get_data()
    crypto = data['crypto']
    balance = get_balance(callback.from_user.id)
    user_brief = get_brief_case(callback.from_user.id)
    await state.update_data(balance=balance, user_brief=user_brief)
    await callback.message.edit_text(
        text=lexicon_ru['buy_value'].format(balance, user_brief[crypto], crypto, crypto),
        reply_markup=backs_keyboard()
    )


@router.callback_query(MenuSG.buy_or_sell, F.data == buy_or_sell_buttons['sell'])
async def cmd_sell(callback: CallbackQuery, state: FSMContext):
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': callback.message.reply_markup,
        'text': callback.message.text
    }
    states.append(prev_state)
    await state.set_state(SellSG.sell_value)
    user_id = callback.from_user.id
    data = await state.get_data()
    crypto = data['crypto']
    balance = get_balance(user_id)
    user_brief = get_brief_case(user_id)
    await state.update_data(balance=balance, user_brief=user_brief)
    await callback.message.edit_text(
        text=lexicon_ru['sell_value'].format(balance, user_brief[crypto], crypto, crypto),
        reply_markup=backs_keyboard()
    )


@router.message(BuySG.buy_value, F.text.isdigit())
async def cmd_buy_value(message: Message, state: FSMContext):
    buy_value = int(message.text)
    await state.update_data(buy_value=buy_value)
    data = await state.get_data()
    crypto = data['crypto']
    price = data['price']
    balance = data['balance']
    user_brief = data['user_brief']
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': backs_keyboard(),
        'text': lexicon_ru['sell_value'].format(balance, user_brief[crypto], crypto, crypto)
    }
    states.append(prev_state)
    await message.answer(
        text=lexicon_ru['buy_accept'].format(buy_value, crypto, buy_value * price),
        reply_markup=accept_keyboard()
    )
    await state.update_data(value=int(message.text))
    await state.set_state(BuySG.accept_buy)


@router.message(SellSG.sell_value, F.text.isdigit())
async def cmd_sell_value(message: Message, state: FSMContext):
    sell_value = int(message.text)
    await state.update_data(sell_value=sell_value)
    data = await state.get_data()
    crypto = data['crypto']
    price = data['price']
    balance = data['balance']
    user_brief = data['user_brief']
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': backs_keyboard(),
        'text': lexicon_ru['sell_value'].format(balance, user_brief[crypto], crypto, crypto)
    }
    states.append(prev_state)
    await message.answer(
        text=lexicon_ru['sell_accept'].format(sell_value, crypto, sell_value * price),
        reply_markup=accept_keyboard()
    )
    await state.set_state(SellSG.accept_sell)


@router.callback_query(BuySG.accept_buy)
async def cmd_accept_buy(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    buy_value = data['buy_value']
    price = data['price']
    crypto = data['crypto']
    result = await shop(callback.from_user.id, buy_value, price, crypto)
    if result:
        await callback.message.edit_text(
            text=lexicon_ru['successfully_buy'].format(buy_value, crypto),
            reply_markup=back_to_menu_keyboard()
        )
        await state.clear()
    else:
        await callback.message.edit_text(
            text=lexicon_ru['unsuccessfully_buy'],
            reply_markup=backs_keyboard()
        )


@router.callback_query(SellSG.accept_sell)
async def cmd_accept_sell(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sell_value = data['sell_value']
    price = data['price']
    crypto = data['crypto']
    result = await sell(callback.from_user.id, sell_value, price, crypto)
    if result:
        await callback.message.edit_text(
            text=lexicon_ru['successfully_sell'].format(sell_value, crypto),
            reply_markup=back_to_menu_keyboard()
        )
        await state.clear()
    else:
        await callback.message.edit_text(
            text=lexicon_ru['unsuccessfully_sell'],
            reply_markup=backs_keyboard()
        )


@router.callback_query(MenuSG.main_menu, F.data == menu_buttons_lexicon['briefcase'])
async def cmd_briefcase(callback: CallbackQuery, state: FSMContext):
    user_brief = get_brief_case(callback.from_user.id)
    await callback.message.edit_text(
        text=lexicon_ru['user_brief'],
        reply_markup=user_brief_keyboard(user_brief)
    )
    await state.set_state(BriefcaseSG.choose_crypto)


@router.callback_query(BriefcaseSG.choose_crypto)
async def cmd_briefcase_button(callback: CallbackQuery, state: FSMContext):
    prev_state = {
        'state': await state.get_state(),
        'reply_markup': callback.message.reply_markup,
        'text': callback.message.text
    }
    states.append(prev_state)
    crypto = callback.data.split(':')[-1]
    price = get_crypto_price(crypto)
    await state.update_data(crypto=crypto, price=price)
    await callback.message.edit_text(
        text=lexicon_ru['buy_or_sell'],
        reply_markup=buy_or_sell_keyboard()
    )
    await state.set_state(MenuSG.buy_or_sell)


@router.callback_query(MenuSG.main_menu, F.data == menu_buttons_lexicon['statistics'])
async def cmd_statistics(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = get_user_statistics(user_id)
    await callback.message.edit_text(
        text=lexicon_ru['user_statistics'].format(*data),
        reply_markup=back_to_menu_keyboard()
    )