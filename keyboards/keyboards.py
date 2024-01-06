from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from lexicon.lexicon_ru import (menu_buttons_lexicon, lexicon_ru,
                                accept_buttons, buy_or_sell_buttons)
from services.trade_functions import get_crypto_prices


def menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=value)]
        for value in menu_buttons_lexicon.values()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def markets_keyboard():
    crypto_prices = get_crypto_prices()
    buttons = [
        [InlineKeyboardButton(text=line[0], callback_data=line[1])]
        for line in crypto_prices
    ]
    buttons.append([InlineKeyboardButton(text=lexicon_ru['back_to_menu'], callback_data=lexicon_ru['back_to_menu'])])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def buy_or_sell_keyboard():
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=value)]
        for value in buy_or_sell_buttons.values()
    ]
    buttons.append([InlineKeyboardButton(text=accept_buttons['back'], callback_data=accept_buttons['back'])])
    buttons.append([InlineKeyboardButton(text=lexicon_ru['back_to_menu'], callback_data=lexicon_ru['back_to_menu'])])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def accept_keyboard():
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=value)]
        for value in accept_buttons.values()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    buttons.append([InlineKeyboardButton(text=lexicon_ru['back_to_menu'], callback_data=lexicon_ru['back_to_menu'])])
    return keyboard


def back_to_menu_keyboard():
    buttons = [[InlineKeyboardButton(text=lexicon_ru['back_to_menu'], callback_data=lexicon_ru['back_to_menu'])]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def backs_keyboard():
    buttons = [
        [InlineKeyboardButton(text=accept_buttons['back'], callback_data=accept_buttons['back'])],
        [InlineKeyboardButton(text=lexicon_ru['back_to_menu'], callback_data=lexicon_ru['back_to_menu'])]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def user_brief_keyboard(user_brief):
    buttons = [
        [InlineKeyboardButton(text=f'{value} {key}', callback_data=f'briefcase:{key}')]
        for key, value in user_brief.items()
    ]
    buttons.append([InlineKeyboardButton(text=lexicon_ru['back_to_menu'], callback_data=lexicon_ru['back_to_menu'])])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

