from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters
import requests

bot_id = '5218966937:AAHt9C_IRO9B_LHhMZkfuC1zz9dVr72IAQ4'
moderation_chat_id = '-683299306'
group_chat_id = '-657618577'
test_sticket_id = 'CAADAgADOQADfyesDlKEqOOd72VKAg'
global last_message
global last_user_input_id
global last_user_input_full_name
last_message = ''
last_user_input_id = ''
last_user_input_full_name = ''

def start_analysis(text):
        bot_send_message(moderation_chat_id, text)
        bot_send_message(moderation_chat_id, default_evaluate_message())

def is_group(update: Update):
    if str(update.message.chat_id) == '-683299306' or str(update.message.chat_id) == '-657618577':
        return True
    
def is_admin_group(update: Update):
    if str(update.message.chat_id) == moderation_chat_id:
        return True

def bot_send_message(chat_id, text):    
    send_message_url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=html&text={2}'.format(bot_id, chat_id, text)
    request_get = requests.get(send_message_url)
    print('Status Code: ' + str(request_get.status_code))

def bot_send_sticker(chat_id, sticker_id):
    send_sticker_url = 'https://api.telegram.org/bot{0}/sendSticker?chat_id={1}&sticker={2}'.format(bot_id, chat_id, sticker_id)
    request_get = requests.get(send_sticker_url)
    print('Status Code: ' + str(request_get.status_code))

updater = Updater(bot_id, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá as mensagens serão colocadas para avaliação aqui.")
    bot_send_message(moderation_chat_id, 'Iniciando Execução')
    
def unknown_text(update: Update, context: CallbackContext):
    global last_message 
    global last_user_input_id
    global last_user_input_full_name
    if not (is_group(update)):
        update.message.reply_text('Sua mensagem será avaliada pela moderação, se aprovada, será postada em nosso grupo.')
        if (update.message.from_user.full_name != ''):
            text = '{0} Disse: \n\n {1}'.format('<a href="tg://user?id={0}">{1}</a>'
                                        .format(update.message.from_user.id, update.message.from_user.full_name), 
                                        update.message.text)
        else:
            text = '{0} Disse: \n\n {1}'.format('<a href="tg://user?id={0}">{1}</a>'
                                        .format(update.message.from_user.id, update.message.from_user.id), 
                                        update.message.text)
        
        last_message = text
        last_user_input_id = update.message.from_user.id
        last_user_input_full_name = update.message.from_user.full_name
        start_analysis(text)
    if is_admin_group(update):
        if str(update.message.text == 1):
            bot_send_message(group_chat_id, last_message)
        
    
def unknow_sticker(update: Update, context: CallbackContext):
    if not (is_group(update)):
        update.message.reply_text('Sua mensagem será avaliada pela moderação, se aprovada, será postada em nosso grupo.')
        if (update.message.from_user.full_name != ''):
            text = '{0} Postou:'.format('<a href="tg://user?id={0}">{1}</a>'
                                        .format(update.message.from_user.id, update.message.from_user.full_name), 
                                        )
        else:
            text = '{0} Postou:'.format('<a href="tg://user?id={0}">{1}</a>'
                                        .format(update.message.from_user.id, update.message.from_user.id), 
                                        )
        bot_send_message(moderation_chat_id, text)
        sticker_id = update.message.sticker.file_id
        bot_send_sticker(moderation_chat_id, sticker_id)
        bot_send_message(moderation_chat_id, default_evaluate_message())

def default_evaluate_message():
    result = '<b>Digite uma das opções:</b> \n <b>1</b> - Aprovar \n <b>2</b> - Banir \n <b>3</b> - Notificar Comportamento'
    return result

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.dispatcher.add_handler(MessageHandler(Filters.sticker, unknow_sticker))
    
updater.start_polling()