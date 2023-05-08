import sys
import time
import telepot

import alsaaudio as aa

m = aa.Mixer()

status = 0

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    global status
    print('Got command: %s' % command)

    if command == '/time':
        bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command.lower() == 'on' or command.lower() == 'увага' or command.lower() == 'старт':
        if status == 1:
            bot.sendMessage(chat_id, "Уже і так ввімкнено!!")
        else:
            status = 1
            bot.sendMessage(chat_id, "УВАГА, ВВІМКНЕНО!")
            m.setvolume(100)
    elif command.lower() == 'off' or command.lower() == 'стоп':
        if status == 0:
            bot.sendMessage(chat_id, "Уже і так НЕ ввімкнена!")
        else:
            status = 0
            bot.sendMessage(chat_id, "ЗУПИНЕНО!")
            m.setvolume(0)
    elif command.lower() == '/status' or command.lower() == 'статус' or command.lower() == 'стан':
        if status == 1:
            msssg = "Поточний статус: увімкнено"
        elif status == 0:
            msssg = "Поточний статус: вимкнено"
        else:
            msssg = "Невідома команда, спробуйте знову"
        bot.sendMessage(chat_id, msssg)    
    else:
        bot.sendMessage(chat_id, "Невідома команда, спробуйте знову") 

bot = telepot.Bot('520****API****')
bot.message_loop(handle)
print('I am listening...')

while 1:
    try:
        time.sleep(10)
    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        exit()
    
    except:
        print('Other error or exception occured!')
