import time, datetime
import telepot
import vlc

siren = "Air_raid_siren.mp3"
p = vlc.MediaPlayer(siren)

status = 0
p.stop()

now = datetime.datetime.now()
on_words = ['старт', '+', 'on','ввімкнути',"увімкнути"]
off_words = ['стоп','-','вимкнути','off','of']
check_words = ['/status', '/status', 'стан', 'check', 'чек']


def get_admins():
    adm_file = open('adm_siren.txt', 'r')
    admins = adm_file.read()
    adm_file.close()
    return admins.split('*')

def get_users():
    usr_file = open('usr_siren.txt', 'r')
    users = usr_file.read()
    usr_file.close()
    return users.split('*')

def check_admin(id_):
    try:
        return len(id_) == 9 and id_.isdigit()
    except:
        return False


def handle(msg):
    global check_words
    global status
    
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print('Got command: %s' % command, chat_id)
    command = command.replace(' ','').lower()    

    try:
        if command == '/start':
                if str(chat_id) not in get_users():
                    print(get_users())
                    usr_file = open('usr_siren.txt', 'a+')
                    usr_file.writelines(f"*{chat_id}")
                    usr_file.close()
                    bot.sendMessage(1000000, f"{chat_id} is new user!")   #1000000 - telegram id of admin
                    bot.sendMessage(chat_id, "Зверніться до адміністратора для доступу.")
                else:
                    bot.sendMessage(chat_id, "Готово до роботи.")
        elif str(chat_id) in get_admins():
            if 'addadmin' in command:
                if check_admin(command.replace('addadmin','')):
                    if command.replace('addadmin','') not in get_admins():
                        adm_file = open('adm_siren.txt', 'a+')
                        adm_file.writelines(f"*{command.replace('addadmin','')}")
                        adm_file.close()
                    bot.sendMessage(chat_id, "Done.") 
                    bot.sendMessage(569830287, f"Admins: {get_admins()}")
                    bot.sendMessage(int(command.replace('addadmin','')), "Готово до роботи.") 
                else:
                    bot.sendMessage(chat_id, "Невідома команда, спробуйте знову")
            elif 'deladmin' in command and '1000000' not in command:
                with open('adm_siren.txt', 'r') as file :
                    filedata = file.read()
                # Replace the target string
                filedata = filedata.replace(command.replace('deladmin',''), '')
                # Write the file out again
                with open('adm_siren.txt', 'w') as file:
                    file.write(filedata) 
                bot.sendMessage(569830287, f"Admins: {get_admins()}")
            elif command == 'adminlist':
                bot.sendMessage(1000000, f"Admins: {get_admins()}")
            elif command in on_words:
                if status == 1:
                    bot.sendMessage(chat_id, "🔴Уже і так ВВІМКНЕНО!🔴")
                else:    
                    bot.sendMessage(chat_id, "🔴УВАГА, ВВІМКНЕНО!🔴")
                    p.play()
                status = 1
                bot.sendMessage(1000000, f"Turned ON by {chat_id}")        
            elif command in off_words:
                if status == 0:
                    bot.sendMessage(chat_id, "🟢Уже і так НЕ ввімкнена!🟢")
                else:
                    p.stop()
                    bot.sendMessage(chat_id, "🟢ЗУПИНЕНО!🟢")
                status = 0
                bot.sendMessage(1000000, f"Turned OFF by {chat_id}")
            elif command in check_words:
                if status == 1:
                    msssg = "🔴Поточний статус: УВІМКНЕНО🔴"
                elif status == 0:
                    msssg = "🟢Поточний статус: вимкнено🟢"
                else:
                    msssg = "Невідома команда, спробуйте знову"
                bot.sendMessage(chat_id, f"{msssg}")    
            else:
                bot.sendMessage(chat_id, "Невідома команда, спробуйте знову") 
        else:
                bot.sendMessage(chat_id, "Невідома команда, спробуйте знову") 
    except Exception as e:
        bot.sendMessage(1000000, f"Crytical error. MSG: {command}. id: {chat_id} . Error: {e}")
        print(e)
bot = telepot.Bot('5112***:AAF***')  #API
bot.message_loop(handle)
print(f'I am listening...')

while 1:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print('\n Program interrupted')
        p.stop()
        exit()
    except:
        print('Other error or exception occured!')
        p.stop()


