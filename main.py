import io
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pandas as pd

TOKEN = "6042534217:AAHYkViiDPlsQty3lTRrunT2rVc32IhV4Ak"
bot = Bot(token=TOKEN)  #экземпляр класса Bot. В качестве аргумента передается токен
dp = Dispatcher(bot)  #эземпляр класса класса Dispatcher (dp), который в качестве аргумента получит bot, принимает все апдейты и обрабатывает их

classes = {'1A' : '1DIbZMRdqKYi_WalPl5T9kESXmP0Wh2ZpAnuHdBe35-Y', '1B' : '1aaAovvR--ZuCIbDJ_MSYvBxiJBbeujEhoEnVYmqLJCo'}  #Создается словарь classes, где ключами являются классы, а значениями - идентификаторы таблиц 

def work_with_file(cllas):
    SHEET_ID = classes[cllas] #Получает идентификатор таблицы
    SHEET_NAME = '1'  #Получает имя листа
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'   #Формирует URL-адрес
    return url

def poisk_num_str(chel):
    num = table.index[table['Код'] == chel].tolist() # Поиск номера строки по заданному коду
    return num

def into_dict(num, colums):
    dict = {}
    for item in colums:
        for info in table[item][num]:
            dict[item] = info # Заполнение словаря значениями из таблицы
    return dict #возвращает словарь, содержащий информацию о ребенке


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    await message.answer('Вас приветствует чат-бот родителей в классе.\nВы можете посмотреть текущую успеваемость вашего ребёнка.')
    await message.answer('Введите класс ребёнка в формате:\n /class № класса')

@dp.message_handler(commands=['class'])
async def search_class(message: types.Message):
    cllas = message.get_args()
    url = work_with_file(cllas)
    global table
    table = pd.read_csv(url)
    await message.answer('Введите уникальный код в формате:\n/code код ребёнка')

@dp.message_handler(commands=['code'])
async def search_chel(message: types.Message):
    chel = message.get_args()
    num = poisk_num_str(chel)
    colum = table.columns
    dict = into_dict(num, colum)
    answer_message = ""
    for key in dict:
        answer_message += key + ': '+ dict[key] + '\n' # Формирование ответного сообщения с информацией о ребёнке
    await message.answer(answer_message)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)  #метод start_polling опрашивает сервер, проверяя на нём обновления. Если они есть, то они приходят в Telegram
