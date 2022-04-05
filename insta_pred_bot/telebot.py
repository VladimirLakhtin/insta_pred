from aiogram.utils import executor
from prediction_part.tokenizer import text_transform
from create_bot import dp
import handlers

async def on_startup(_):
    print('Бот подключился')

handlers.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)