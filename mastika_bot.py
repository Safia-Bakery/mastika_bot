from telegram.constants import ParseMode
from sqlalchemy.orm import Session
import os
from telegram import ReplyKeyboardMarkup,Update,WebAppInfo,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,PicklePersistence

)
import json
import microser
import crud
from dotenv import load_dotenv
from translate import translation

load_dotenv()
manu_buttons = [['Оформить заказ🎂'],['Каталог тортов📒','Информацияℹ️'],['Регламент📃','Настройки⚙️']]
languages = [['uzbek','russian']]

from database import engine,session
#Base.metadata.create_all(bind=engine)
BOTTOKEN = os.environ.get('BOT_TOKEN')

SETTINGS,PHONENUMBER,VARIFICATION,FULLNAME,MANU,ORDER,INFORMATION,UPDATEFULLNAME,UPDATEPHONE,UPDATEPHONEVARIFIC= range(10)
persistence = PicklePersistence(filepath='hello.pickle')



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    query = crud.get_user(db=session,tel_id=update.message.from_user.id)
    if query:
        #await update.message.reply_text(translation[context.user_data['language']]['congrats'])
        await update.message.reply_text(translation[context.user_data['language']]['request_order'],reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    
    await update.message.reply_text("Здравствуйте!!")
    context.user_data['language'] = 'ru'
    reply_keyboard = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
    await update.message.reply_text(translation[context.user_data['language']]['greeting'])
    await update.message.reply_text(translation[context.user_data['language']]['request_phone'],
                                    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Поделиться контактом",resize_keyboard=True
        ))

    return PHONENUMBER
    #user= crud.get_user_tel_id(db=session,id=update.message.from_user.id)
    #user_data = requests.post(f"{BASE_URL}tg/login",json={'telegram_id':update.message.from_user.id})

    #if user:
    #    context.user_data['sphere_status']=user.sphere_status
    #    await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    #    return MANU
    #await update.message.reply_text(
    #    "Здравствуйте. Давайте сначала познакомимся ☺️\nКак Вас зовут? (в формате Ф.И.О)",
    #)

    #return LANGUAGE


#async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#    #if update.message.text=='uzbek':
#    #    context.user_data['language'] = 'uz'
#    #if update.message.text=='russian':
#    context.user_data['language'] = 'ru'
#    reply_keyboard = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
#    await update.message.reply_text(translation[context.user_data['language']]['greeting'])
#    await update.message.reply_text(translation[context.user_data['language']]['request_phone'],
#                                    reply_markup=ReplyKeyboardMarkup(
#            reply_keyboard, input_field_placeholder="Поделиться контактом",resize_keyboard=True
#        ))
#
#    return PHONENUMBER

async def phonenumber(update:Update,context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone_number'] = update.message.contact.phone_number.replace('+','')
    await update.message.reply_text(translation[context.user_data['language']]['varification'],reply_markup=ReplyKeyboardRemove())
    return VARIFICATION


async def varification(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['otp']=update.message.text
    await update.message.reply_text(translation[context.user_data['language']]['request_name'])
    return FULLNAME
async def fullname(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['full_name'] = update.message.text
    username = microser.generate_random_username(full_name=context.user_data['full_name'],phone_number=context.user_data['phone_number'])
    user = crud.create_user(db=session,
                     tel_id=update.message.from_user.id,
                     full_name=context.user_data['full_name'],
                     phone_number=context.user_data['phone_number'],
                     user_name=username)
    await update.message.reply_text(translation[context.user_data['language']]['congrats'])
    await update.message.reply_text(translation[context.user_data['language']]['request_order'],reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return MANU

async def manu(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'Оформить заказ🎂':
        user = crud.get_user(db=session,tel_id=update.message.from_user.id)
        await update.message.reply_text(
        f"Пожалуйста нажмите кнопку: Заказать🍰",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Заказать🍰",
                web_app=WebAppInfo(url=f"https://admin.cakes.safiabakery.uz/tg/order-type?token={microser.create_access_token(user.username)}",),
                
            ),resize_keyboard=True)
        )
        return ORDER
    elif update.message.text =='Каталог тортов📒':
        await update.message.reply_text(text="<a href='https://telegra.ph/Katalog-tortov-10-30'>Каталог тортов</a>",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True),parse_mode = ParseMode.HTML)
        #await update.message.reply_text('you chose Каталог тортов',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    
    elif update.message.text =='Регламент📃':
        #await update.message.reply_text(translation[context.user_data['language']]['reglament'])
        await update.message.reply_text(text="<a href='https://telegra.ph/Reglament-oformleniya-individualnyh-tortov-10-30'>Регламент</a>",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True),parse_mode = ParseMode.HTML)
        return MANU
    elif update.message.text =='Информацияℹ️':
        buttons = [['Связаться с специалистом','Оставить отзыв✍️','⬅️Назад']]
        await update.message.reply_text('Информация',reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
        return INFORMATION
    elif update.message.text =='Настройки⚙️':
        buttons = [['Изменить номер','Изменить Фио','⬅️Назад']]
        await update.message.reply_text('you chose settings',reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
        return SETTINGS
    else:
        await update.message.reply_text('thats wrong what you entered',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU



async def order(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_text(translation[context.user_data['language']]['congrats'])
    await update.message.reply_text(translation[context.user_data['language']]['request_order'],reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return MANU

async def information(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    entered_data = update.message.text
    if entered_data=='Связаться с специалистом':
        await update.message.reply_text('+998 97 113-40-40')
        await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    elif entered_data=='Оставить отзыв✍️':
        await update.message.reply_text(translation[context.user_data['language']]['comment'])
        await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    else:
        await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    

async def settings(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    data = update.message.text
    if data  =='Изменить Фио':
        await update.message.reply_text('please enter you full name',reply_markup=ReplyKeyboardRemove())
        return UPDATEFULLNAME
    elif data =='Изменить номер':
        reply_keyboard = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
        await update.message.reply_text(translation[context.user_data['language']]['request_phone'],
                                    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Поделиться контактом",resize_keyboard=True
        ))
        return UPDATEPHONE
    else:
        await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
        

async def updatefullname(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    data = update.message.text
    crud.updateuser(db=session,tel_id=update.message.from_user.id,phone_number=None,full_name=data)
    await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return MANU

async def updatephone(update:Update,context: ContextTypes.DEFAULT_TYPE) -> int:
    #context.user_data['updatephone'] = update.message.contact.phone_number.replace('+','')
    user_phone = update.message.contact.phone_number.replace('+','')
    if microser.phone_checker(user_phone):
        context.user_data['phone_number'] = update.message.contact.phone_number.replace('+','')
        await update.message.reply_text(translation[context.user_data['language']]['varification'],reply_markup=ReplyKeyboardRemove())
        return UPDATEPHONEVARIFIC
    else:
        reply_keyboard = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
        await update.message.reply_text(translation[context.user_data['language']]['request_phone'],
                                    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Поделиться контактом",resize_keyboard=True
        ))
        return UPDATEPHONE

async def updatephonevarific(update:Update,context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['otp']=update.message.text
    await update.message.reply_text('Manu',reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    crud.updateuser(db=session,tel_id=update.message.from_user.id,phone_number=context.user_data['phone_number'],full_name=None)
    return MANU

    
#--------------last section-------------
def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            #LANGUAGE: [MessageHandler(filters.TEXT,language)],
            PHONENUMBER:[MessageHandler(filters.CONTACT,phonenumber)],
            VARIFICATION:[MessageHandler(filters.TEXT,varification)],
            FULLNAME:[MessageHandler(filters.TEXT,fullname)],
            MANU:[MessageHandler(filters.TEXT,manu)],
            ORDER:[MessageHandler(filters.StatusUpdate.WEB_APP_DATA,order)],
            INFORMATION:[MessageHandler(filters.TEXT,information)],
            SETTINGS:[MessageHandler(filters.TEXT,settings)],
            UPDATEFULLNAME:[MessageHandler(filters.TEXT,updatefullname)],
            UPDATEPHONE:[MessageHandler(filters.CONTACT,updatephone)],
            UPDATEPHONEVARIFIC:[MessageHandler(filters.TEXT,updatephonevarific)],
        },
        fallbacks=[CommandHandler('start',start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,

        
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()