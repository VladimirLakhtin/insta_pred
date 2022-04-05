from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5200980757:AAG4yNGnlgvDNiRoHeXU9P-4qEFC3GDHFQ8')
dp = Dispatcher(bot, storage=storage)

