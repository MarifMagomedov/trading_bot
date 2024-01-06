import sqlite3 as sq
import json


users = sq.connect('users.db')
cur = users.cursor()
currencies = {
        'BTC': 0,
        'ETH': 0,
        'USDT': 0,
        'BNB': 0,
        'SOL': 0,
        'ADA': 0,
        'AVAX': 0,
        'USDC': 0,
        'XRP': 0,
        'STETH': 0
    }


async def db_start():
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, balance INTEGER, briefcase TEXT, 
        number_of_transactions INTEGER, buys INTEGER, sells INTEGER, changing_the_balance INTEGER)'''
    )
    users.commit()


async def create_profile(user_id):
    user = cur.execute(
        'SELECT 1 FROM users WHERE user_id == "{}"'.format(user_id)
    ).fetchone()
    if not user:
        cur.execute(
            '''INSERT INTO users(user_id, balance, briefcase, 
            number_of_transactions, buys, sells, changing_the_balance) VALUES(?, ?, ?, ?, ?, ?, ?)''',
            (user_id, 696969, json.dumps(currencies), 0, 0, 0, 0)
        )
        users.commit()


def get_balance(user_id):
    data = cur.execute(
        'SELECT balance FROM users WHERE user_id = "{}"'.format(user_id)
    ).fetchone()
    return data[0]


def get_brief_case(user_id):
    user_brief = json.loads(cur.execute(
        'SELECT briefcase FROM users WHERE user_id == "{}"'.format(user_id)
    ).fetchone()[0])
    return user_brief


def get_number_of_transactions(user_id):
    number_of_transactions = cur.execute(
        'SELECT number_of_transactions FROM users WHERE user_id == "{}"'.format(user_id)
    ).fetchone()[0]
    return number_of_transactions


def get_buys(user_id):
    user_buys = cur.execute(
        'SELECT buys FROM users WHERE user_id == "{}"'.format(user_id)
    ).fetchone()[0]
    return user_buys


def get_sells(user_id):
    user_sells = cur.execute(
        'SELECT sells FROM users WHERE user_id == "{}"'.format(user_id)
    ).fetchone()[0]
    return user_sells


def get_changing_the_balance(user_id):
    user_changing_the_balance = cur.execute(
        'SELECT changing_the_balance FROM users WHERE user_id == "{}"'.format(user_id)
    ).fetchone()[0]
    return user_changing_the_balance


async def shop(user_id, buy_value, price, crypto):
    user_balance = get_balance(user_id)
    user_brief = get_brief_case(user_id)
    user_number_of_transactions = get_number_of_transactions(user_id)
    user_buys = get_buys(user_id)
    user_changing_the_balance = get_changing_the_balance(user_id)
    if 0 <= buy_value * price <= user_balance:
        user_balance -= (buy_value * price)
        user_brief[crypto] += buy_value
        user_number_of_transactions += 1
        user_buys += 1
        user_changing_the_balance = round(user_changing_the_balance - (buy_value * price), 2)
        cur.execute(
            '''UPDATE users SET balance = ?, briefcase = ?, 
            number_of_transactions = ?, buys = ?, changing_the_balance = ? WHERE user_id == ?''',
            (user_balance, json.dumps(user_brief),
             user_number_of_transactions, user_buys, user_changing_the_balance, user_id)
        )
        users.commit()
        return True
    else:
        return False


async def sell(user_id, sell_value, price, crypto):
    user_balance = get_balance(user_id)
    user_brief = get_brief_case(user_id)
    user_number_of_transactions = get_number_of_transactions(user_id)
    user_sells = get_sells(user_id)
    user_changing_the_balance = get_changing_the_balance(user_id)
    if 0 <= sell_value <= user_brief[crypto]:
        user_brief[crypto] -= sell_value
        user_balance += (price * sell_value)
        user_number_of_transactions += 1
        user_sells += 1
        user_changing_the_balance = round(user_changing_the_balance + (sell_value * price), 2)
        cur.execute(
            '''UPDATE users SET balance = ?, briefcase = ?, 
            number_of_transactions = ?, sells = ?, changing_the_balance = ? WHERE user_id == ?''',
            (user_balance, json.dumps(user_brief),
             user_number_of_transactions, user_sells, user_changing_the_balance, user_id)
        )
        users.commit()
        return True
    else:
        return False


def get_user_statistics(user_id):
    user_balance = get_balance(user_id)
    user_number_of_transactions = get_number_of_transactions(user_id)
    user_sells = get_sells(user_id)
    user_buys = get_buys(user_id)
    user_changing_the_balance = get_changing_the_balance(user_id)
    if user_changing_the_balance > 0:
        user_changing_the_balance = f'+{user_changing_the_balance}'
    return user_balance, user_changing_the_balance, user_number_of_transactions, user_buys, user_sells
