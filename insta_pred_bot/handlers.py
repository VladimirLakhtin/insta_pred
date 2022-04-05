from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import bot
import keyboards
from prediction_part.make_pred import get_pred
import instaloader.exceptions as insta_exception


class FSMUser_name(StatesGroup):
    user_name = State()


async def command_start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет! \nЯ могу сказать, является ли конкретный Инстаграм-аккаунт бизнес-аккаунтом\n\nВыбери действие', reply_markup=keyboards.kb_main)


async def command_help(message : types.Message):
    await bot.send_message(message.from_user.id, '''Данный бот использует ML модель, которая получает на вход рускоязычный Instargam-аккаунт и относит его к одной из 2 групп:\n
    \U0001F4B0Business-аккаунты - аккаунты, деятельность которых направлена на достижение коммерческих целей посредством продажи и/или рекламы товаров/услуг, в частности направленных на других пользователей Instargam\n
    \U0001F3C4Life-аккаунты - аккаунты, деятельность которых направлена на демонстрацию исключительно личной жизни конкретного человека. Главной задачей не является достижение коммерческих целей\n
    Разработчик: <b>@apelsin_lvl</b>''',parse_mode='html', reply_markup=keyboards.kb_main)


async def get1pred(message: types.Message):
    await FSMUser_name.user_name.set()
    await bot.send_message(message.from_user.id, 'Введи ник пользователя:')


async def get_user_name(message: types.Message, state: FSMContext):
    
    try:
        y = get_pred(message['text'])
    except insta_exception.ProfileNotExistsException:
        await bot.send_message(message.from_user.id, 'Аккаунта с таким именем не существует\U0001F937 Попробуй еще раз', reply_markup=keyboards.kb_main)
    except insta_exception.LoginRequiredException:
        await bot.send_message(message.from_user.id, 'Аккаунта с таким именем не существует\U0001F937 Попробуй еще раз', reply_markup=keyboards.kb_main)

    await FSMUser_name.next()
    mess = message['text']
    y = 'Business_account' + '\U0001F4B0' if y == 1 else 'Life_account' + '\U0001F3C4'
    await bot.send_message(message.from_user.id, f'Думаю, <b>{mess}</b> - это <b>{y}</b>', parse_mode='html', reply_markup=keyboards.kb_main)



async def other_message(message: types.Message):
    if message['text'].lower() == 'инфо':
        await bot.send_message(message.from_user.id, '''Данный бот использует ML модель, которая получает на вход рускоязычный Instargam-аккаунт и относит его к одной из 2 групп:\n
    \U0001F4B0Business-аккаунты - аккаунты, деятельность которых направлена на достижение коммерческих целей посредством продажи и/или рекламы товаров/услуг, в частности направленных на других пользователей Instargam\n
    \U0001F3C4Life-аккаунты - аккаунты, деятельность которых направлена на демонстрацию исключительно личной жизни конкретного человека. Главной задачей не является достижение коммерческих целей\n
    Разработчик: <b>@apelsin_lvl</b>''', parse_mode='html', reply_markup=keyboards.kb_main)
    else:
        await bot.send_message(message.from_user.id, 'Я не понимаю, тебе следует выбрать действие ниже \U0001F447', reply_markup=keyboards.kb_main)



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])  
    dp.register_message_handler(get1pred, lambda message: 'предскажи аккаунт' in message.text.lower(), state=None)
    dp.register_message_handler(get_user_name, state=FSMUser_name.user_name)
    dp.register_message_handler(other_message) 
