import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)


TOKEN = '7737621617:AAHQrH9O1dflwHPbssD26Q8gwJxMPG14zng'
# Структура данных

serials = {
    'Убийства в…': {
        'description': '''Сериал погружает зрителя в атмосферу тихой провинциальной жизни, где за фасадом обыденности скрываются темные тайны.
С каждым новым эпизодом раскрываются все новые подробности загадочных убийств, которые потрясают местное сообщество.
Зрители станут свидетелями запутанных расследований, в которых переплетаются личные драмы,давние обиды и криминальные интриги.''',
        'link': 'https://www.ivi.ru/watch/ubijstva-v',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\71jI5iY+1yL.jpg'  
    },
    'Кости': {
        'description': '''Этот сериал приглашает зрителей окунуться в мир судебной медицины. Команда опытных специалистов, во главе с блестящим антропологом, занимается расследованием самых загадочных и сложных преступлений.
С помощью научных методов они восстанавливают картину произошедшего, анализируя мельчайшие детали и улики.
Сериал сочетает в себе элементы детектива, триллера и научной фантастики, предлагая зрителям захватывающие расследования и неожиданные повороты сюжета.''',
        'link': 'https://www.kinopoisk.ru/series/243595/?utm_referrer=yandex.ru',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\pyYP1DWZkZA.jpg'
    },
     'Доктор Харроу': {
        'description': '''Драма, посвященная работе судмедэксперта, который сталкивается с самыми загадочными и трагическими случаями.
Доктор Харроу - блестящий ученый, но его личная жизнь далека от идеала.
В каждом эпизоде он проводит вскрытия, анализирует улики и пытается понять причины смерти, сталкиваясь с моральными дилеммами и человеческими трагедиями. Сериал поднимает глубокие вопросы о жизни и смерти, о добре и зле, и о том, какую цену приходится платить за правду.''',
        'link': 'https://www.kinopoisk.ru/series/1112955/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\102410.jpg'
    },
     'Касл': {
        'description': '''Касл - это увлекательное сочетание детективной истории и романтической комедии.
Писатель Ричард Касл, в поисках вдохновения, оказывается вовлеченным в расследование реальных убийств вместе с опытным детективом Кейт Беккет. Их нестандартный подход и остроумные диалоги делают этот сериал легким и приятным для просмотра.''',
        'link': 'https://www.kinopoisk.ru/series/409640/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\212973.jpg'
    },
     'Менталист': {
        'description': '''Менталист - это захватывающий детективный сериал, в центре которого находится Патрик Джейн, человек с феноменальной памятью и способностью к наблюдению.
После трагической гибели своей семьи, он посвящает свою жизнь поимке серийного убийцы, известного как Крвавый Джейн сотрудничает с Калифорнийским Бюро Расследований, используя свои экстрасенсорные способности для раскрытия сложных преступлений.''',
        'link': 'https://www.kinopoisk.ru/series/412344/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\4029f59b7450a2ea7603d4824894eea3.jpg'
    },
    'Охотники за разумом': {
        'description': '''Охотники за  - это психологический триллер, основанный на реальных событиях.
Сериал рассказывает о работе агентов ФБР, которые разрабатывают новые методы профилирования серийных убийц.
Они пытаются проникнуть в сознание преступников,чтобы понять их мотивы и предотвратить новые преступления.''',
        'link': 'https://www.kinopoisk.ru/series/958500/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\RnBX3FKLG8U.jpg'
    }, 
}

books = {
    '«Убийство на улице Морг»': {
        'description': '''Автор: Эдгар Аллан По
Это произведение, которое часто называют первым в истории детективом, погружает нас
в атмосферу таинственного Парижа XIX века. Когда в маленькой комнатке обнаруживают два изуродованных тела, на помощь вызывают гениального детектива Огюста Дюпена.
Его логические рассуждения и нестандартный подход к расследованию позволяют ему раскрыть загадку, которая кажется неразрешимой для других. Роман полон неожиданных
поворотов и создает неповторимую атмосферу загадочности.''',
        'link': 'https://www.litres.ru/book/edgar-po/ubiystvo-na-ulice-morg-17099631/chitat-onlayn/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\kniga_ubiystvo_na_ulitse_morg_po_e.a_1603696109_1.jpg'
    },
    '«Десять негритят»': {
        'description': '''Автор:Агата Кристи
Классический детектив королевы криминального жанра. Десять совершенно незнакомых
людей оказываются на отдаленном острове, куда их пригласил таинственный хозяин. Один за другим они начинают погибать, и каждый раз звучит строчка из детской считалки.
Кто же убийца и почему он выбирает именно этих людей? Интригующий сюжет и неожиданная
развязка делают эту книгу одной из самых популярных в серии о знаменитом детективе Эркюле Пуаро.''',
        'link':'https://www.litres.ru/book/agata-kristi/desyat-negrityat-22174330/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\nx44gs0k5nhrl49dg10jsg643zmmaq7d.jpg'
    },
    '«Мальтийский сокол»': {
        'description': '''Автор: Дэшил Хэммет
Жесткий нуарный роман, который погружает читателя в мрачный мир частных детективов гангстеров.
Сэмюэль Спейд, циничный и опытный детектив, оказывается втянут в опасную игру, связанную с поиском таинственной статуэтки.
Предательство, насилие и любовь переплетаются в этом захватывающем детективе, который стал классикой жанра.''',
        'link': 'https://www.livelib.ru/book/1000477895-maltijskij-sokol-deshil-hemmet',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\IMG_E7150-1000x1000.jpg'
    },
    '«Талантливый мистер Рипли»': {
        'description': '''Автор: Патриция Хайсмит
Психологический триллер, который заставляет задуматься о природе человеческой зависти и жажды власти.
Том Рипли, молодой американец, одержим богатым и успешным англичанином Дикки Гринлифом.
Ради достижения своей цели он готов на все, даже на убийство.
Роман раскрывает темные стороны человеческой души и оставляет глубокое впечатление. ''',
        'link': 'https://www.litres.ru/book/patriciya-haysmit/talantlivyy-mister-ripli-19405295/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\7084778141.jpg'
    },
    '«Смерть - дело одинокое»': {
        'description': '''Автор: Рэй Брэдбери
Философский детектив, который выходит за рамки традиционного жанра.
Стареющий писатель приезжает в маленький городок, где начинает расследовать серию загадочных смертей.
Постепенно он погружается в атмосферу таинственности и одиночества, которая царит в этом месте.
Роман затрагивает глубокие философские вопросы о смысле жизни,старости и смерти. ''',
        'link': 'https://www.litres.ru/book/rey-bredberi/smert-delo-odinokoe-121568/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\6729908819.jpg'
    },
   '«Тайна отца Брауна»': {
        'description': '''Автор: Гилберт Кийт Честертон
Серия рассказов о католическом священнике, который обладает удивительной способностью распутывать самые запутанные дела.
Отец Браун, с его мягкими манерами и глубокими знаниями человеческой природы, часто оказывается единственным, кто может
раскрыть правду о произошедшем преступлении.
Его расследования полны юмора, а его методы совершенно нетрадиционны. ''',
        'link': 'https://www.litres.ru/book/gilbert-chesterton/tayna-otca-brauna-25457443/',
        'photo': 'C:\\Users\\Пользователь\\Pictures\\Screenshots\\6007884870.jpg'
    }, 
    
}

biographies = {
    'Эйлин Кэрол Уорнос': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Эйлин Кэрол Уорнос .pdf'  
    },
    'Юрий Цюман': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Юрий Цюман .pdf'
    },
    'Александр Чайка ': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Александр Чайка .pdf'
    },
    'Джеффри Дамер ': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Джеффри Дамер .pdf'
    },
    'Джон Кристи': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Джон Кристи.pdf'
    },
    'Ладислав Гоер': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Ладислав Гоер .pdf'
    },
     'Тед Банди': {
        'pdf': 'C:\\Users\\Пользователь\\Desktop\\python1\\project\\Тед Банди .pdf'
    },

}

# Обработчики команд и кнопок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Сериалы/Фильмы", callback_data='category_serials')],
        [InlineKeyboardButton("Книги", callback_data='category_books')],
        [InlineKeyboardButton("Биографии", callback_data='category_biographies')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == 'category_serials':
            keyboard = [
                [InlineKeyboardButton(title, callback_data=f'serial_{title}')]
                for title in serials.keys()  # исправлено с books.keys()
            ]
            keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
            await query.edit_message_text('Выберите сериал:', reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'category_books':
            keyboard = [
                [InlineKeyboardButton(title, callback_data=f'book_{title}')]
                for title in books.keys()
            ]
            keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
            await query.edit_message_text('Выберите книгу:', reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == 'category_biographies':
            keyboard = [
                [InlineKeyboardButton(title, callback_data=f'bio_{title}')]
                for title in biographies.keys()  # исправлено с books.keys()
            ]
            keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
            await query.edit_message_text('Выберите биографию:', reply_markup=InlineKeyboardMarkup(keyboard))

        elif data.startswith('serial_'):
            title = data[len('serial_'):]
            item = serials.get(title)
            if item:
                caption = f"{title}\n\n{item['description']}\n\nСсылка для просмотра:\n{item['link']}"
                await query.message.delete()
                with open(item['photo'], 'rb') as photo_file:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo_file, caption=caption)
            else:
                await query.edit_message_text('Сериал не найден.')

        elif data.startswith('book_'):
            title = data[len('book_'):]
            item = books.get(title)
            if item:
                caption = f"{title}\n\n{item['description']}\n\nСсылка для чтения:\n{item['link']}"
                await query.message.delete()
                with open(item['photo'], 'rb') as photo_file:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo_file, caption=caption)
            else:
                await query.edit_message_text('Книга не найдена.')

        elif data.startswith('bio_'):
            title = data[len('bio_'):]
            bio = biographies.get(title)
            if bio:
                await query.edit_message_text(f'{title}')
                with open(bio['pdf'], 'rb') as doc_file:
                    await context.bot.send_document(chat_id=query.message.chat_id, document=doc_file)
            else:
                await query.edit_message_text('Биография не найдена.')
        elif data == 'back':
            keyboard = [
                [InlineKeyboardButton("Сериалы/Фильмы", callback_data='category_serials')],
                [InlineKeyboardButton("Книги", callback_data='category_books')],
                [InlineKeyboardButton("Биографии", callback_data='category_biographies')],
            ]
            await query.edit_message_text('Выберите категорию:', reply_markup=InlineKeyboardMarkup(keyboard))

    except Exception as e:
        logging.error(f"Ошибка в button_handler: {e}")
        await query.edit_message_text("Произошла ошибка, попробуйте еще раз.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == '__main__':
    main()
