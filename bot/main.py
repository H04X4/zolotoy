
import asyncio
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from config import TELEGRAM_TOKEN
from database import Database, ProductModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BotStates(StatesGroup):
    waiting_for_article = State()


class BotHandler:
    def __init__(self, bot: Bot, db: Database):
        self.bot = bot
        self.db = db

    async def cmd_start(self, message: Message, state: FSMContext) -> None:
        await message.answer(
            "<b>👋 Добро пожаловать в систему учета товаров!</b>\n\n"
            "Введите <b>артикул</b> товара, чтобы получить полную информацию.",
            parse_mode=ParseMode.HTML,
        )
        await state.set_state(BotStates.waiting_for_article)

    async def handle_article(self, message: Message, state: FSMContext) -> None:
       
        if not self.db.pool:
            await message.answer("❌ Ошибка подключения к базе данных. Попробуйте позже.")
            return

        article = message.text.strip()
        product: Optional[ProductModel] = await self.db.get_product_by_article(article)

        if not product:
            await message.answer("❌ Товар с таким артикулом не найден. Попробуйте снова.")
            return

        
        row_sum = product.cost_price * product.order_quantity

        
        caption = (
            f"<b>📦 Артикул:</b> {product.article}\n"
            f"<b>🖼 Изображение:</b> {'Есть' if product.image else 'Нет'}\n"
            f"<b>📊 Остаток:</b> {product.stock} шт.\n"
            f"<b>🏪 Наличие в магазинах:</b> {product.store_presence}\n"
            f"<b>💰 Себестоимость:</b> {product.cost_price:.2f} руб.\n"
            f"<b>🛒 Количество для заказа:</b> {product.order_quantity} шт.\n"
            f"<b>🧮 Сумма строки:</b> {row_sum:.2f} руб.\n"
            f"<b>📝 Комментарий:</b> {product.comment}"
        )

        try:
            if product.image:
                await message.answer_photo(
                    photo=product.image,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                )
            else:
                await message.answer(caption, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Ошибка отправки фото: {e}")
            await message.answer(caption, parse_mode=ParseMode.HTML)


async def main() -> None:
  
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    
    db = Database()
    await db.initialize()

    
    handler = BotHandler(bot, db)

    
    dp.message.register(handler.cmd_start, CommandStart())
    dp.message.register(handler.handle_article, BotStates.waiting_for_article)

    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
