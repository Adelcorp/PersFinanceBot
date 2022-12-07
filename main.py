# Сервер Telegram бота
import logging
import os

from aiogram import Bot, Dispatcher, types, executor

import expenses
from categories import Categories

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("5854560246:AAGOJ1oqkHHy-LizHS80OLeLc-hlTTGW-TE")

bot = Bot(token="5854560246:AAGOJ1oqkHHy-LizHS80OLeLc-hlTTGW-TE")
dp = Dispatcher(bot)

class NotCorrectMessage(Exception):
    pass

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Сегодняшние расходы: /today\n"
        "Расходы за текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories")


# Удаление трат
@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалено"
    await message.answer(answer_message)


# Отображение категорий
@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
    await message.answer(answer_message)


# Статистика за день
@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


# Статистика за месяц
@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


# Недавно добавленные расходы
@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходов ещё нет")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажмите "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


# Добавление новых расходов
@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены расходы {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
