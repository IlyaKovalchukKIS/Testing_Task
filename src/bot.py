import json

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.pymongoAPI import func_sale

router = Router()


@router.message(CommandStart())
async def hello_message(message: Message):
    await message.answer(f"Hi {message.chat.username}")


@router.message()
async def pipeline(message: Message):
    data = json.loads(message.text)
    print(data)
    result = func_sale(
        dt_from=data["dt_from"], dt_upto=data["dt_upto"], group_type=data["group_type"]
    )
    await message.answer(f"{result}")
