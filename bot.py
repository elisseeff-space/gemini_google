import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config_gemini import ConfigBox
from hdlr import hdlr_1, hdlr_2

# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=ConfigBox.config['ya_stt_bot'])#, parse_mode=ParseMode.MARKDOWN_V2)
    #bot = Bot(token=ConfigBox.config['GeminiElis_bot'], parse_mode=ParseMode.HTML)
    #bot = Bot(token=ConfigBox.config['GeminiElis_bot'], parse_mode=ParseMode.MARKDOWN_V2)
    # Диспетчер
    dp = Dispatcher()

    dp.include_routers(hdlr_2.router, hdlr_1.router)

    # Запускаем бота и пропускаем все накопленные входящие  
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)
    
if __name__ == "__main__":
    asyncio.run(main())