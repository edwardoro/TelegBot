
from dispatcher import dp
from db import BotDB
from aiogram import  executor, types

BotDB = BotDB('teleBot.db')


@dp.message_handler(commands=('start'), commands_prefix='/!')
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    await message.answer("Welcome!😁\nI'm your ArchiveBot🤓\nYou can save everything here👀")

    @dp.message_handler(commands=('save', 's'), commands_prefix='/!')
    async def start(message: types.Message):
        @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
        async def download_doc(message: types.Message):
            # Скачивание в каталог с ботом с созданием подкаталогов по типу файла
            await message.document.download(destination_dir="/Users/MrSas/Documents")
            await message.answer("Document saved🥳")

        # Типы содержимого тоже можно указывать по-разному.
        @dp.message_handler(content_types=["photo"])
        async def download_photo(message: types.Message):
            # Убедитесь, что каталог /tmp/somedir существует!
            await message.photo[-1].download(destination_dir="/Users/MrSas/Documents")
            await message.answer("Photo saved🥳")

        @dp.message_handler(commands=('text'), commands_prefix='/!')
        async def start(message: types.Message):
            cmd_variants = ('/text', '!text')

            text = message.text
            for i in cmd_variants:
                text = text.replace(i, '').strip()
            BotDB.add_record(message.from_user.id, text)
            await message.answer("Text saved😋")
        await message.answer("Send🥺")
    @dp.message_handler(commands=('download','d'), commands_prefix='/!')
    async def start(message: types.Message):
        @dp.message_handler(commands=('photo_up', 'ph'),commands_prefix='/!' )
        async def upload_ph(message: types.Message):
            await message.answer_document(open("/Users/MrSas/Documents/photos/file_6.jpg", "rb"))



    @dp.message_handler(commands=("history", "h"), commands_prefix="/!")
    async def start(message: types.Message):
        cmd_variants = ('/history', '/h', '!history', '!h')
        within_als = {
            "day": ('today', 'day', 'сегодня', 'день'),
            "month": ('month', 'месяц'),
            "year": ('year', 'год'),
        }

        cmd = message.text
        for r in cmd_variants:
            cmd = cmd.replace(r, '').strip()

        within = 'day'
        if (len(cmd)):
            for k in within_als:
                for als in within_als[k]:
                    if (als == cmd):
                        within = k

        records = BotDB.get_records(message.from_user.id, within)
        await message.answer(records)

    # @dp.message_handler(commands=['img'])
    # def ext_photo(message):
    #     # откроем БД и по ID пользователя извлечём данные base64
    #     conn = sq.connect("myBot.db.db")
    #     img = conn.execute('SELECT files FROM records WHERE user_id = ?', (message.chat.id,)).fetchone()
    #     if img is None:
    #         conn.close()
    #         return None
    #     else:
    #         conn.close()
    #
    #         # сохраним base64 в картинку и отправим пользователю
    #         with open("Users/MrSas/Documents/photos", "wb") as fh:
    #             fh.write(base64.decodebytes(img[0]))
    #             dp.send_photo(message.chat.id, open("Users/MrSas/Documents/photos", "rb"))

@dp.message_handler(commands=('help'), commands_prefix='/!')
async def start(message: types.Message):
    await message.answer(
        'Commands:\n /start - start bot,\n /help - all commands,\n /save - save files, \n /history - output '
        'files and files date,\n /photo - saved or upload photo,\n /document - saved or upload documents,\n /text - saved text,\n /download - bot send files')








if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
