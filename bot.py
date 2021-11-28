import telebot
import config
import requests
import lxml
from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

flag1 = False
Inostranec = False
snils = ''
flag = ' '

@bot.message_handler(commands = ['start', 'help'])
def welcome(message):
    global Naprav
    global Budget
    global sp
    global silka
    global flag
    flag = ' '
    sp = []
    Naprav = Budget = silka = ' '
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
    bi = types.KeyboardButton("БИ")
    ib = types.KeyboardButton("ИБ")
    ist = types.InlineKeyboardButton("ИСТ")
    pi = types.KeyboardButton("ПИ")
    pm = types.KeyboardButton("ПМ")
    pmi = types.KeyboardButton("ПМИ")
    fiit = types.KeyboardButton("ФИИТ")
    markup_reply.add(bi, ib, ist, pi, pm, pmi, fiit)    
    if flag == ' ':
        bot.send_message(message.chat.id,"Привет, абитуриент! Ты уже подал заявление о приёме? Давай-ка глянем, какой у тебя рейтинг!")
        msg = bot.send_message(message.chat.id, "🔹 Бизнес-информатика (БИ)\n🔹 Информационная безопасность (ИБ)\n🔹 Информационные системы и технологии (ИСТ)\n🔹 Прикладная информатика (ПИ)\n🔹 Прикладная математика (ПМ)\n🔹 Прикладная математика и информатика (ПМИ)\n🔹 Фундаментальная информатика и информационные технологии (ФИИТ)\n\nВыбери по кнопке направление по которому ты хочешь узнать свой рейтинг.", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, get_info)
    elif flag == 'Ошибка':
        msg = bot.send_message(message.chat.id, "🔹 Бизнес-информатика (БИ)\n🔹 Информационная безопасность (ИБ)\n🔹 Информационные системы и технологии (ИСТ)\n🔹 Прикладная информатика (ПИ)\n🔹 Прикладная математика (ПМ)\n🔹 Прикладная математика и информатика (ПМИ)\n🔹 Фундаментальная информатика и информационные технологии (ФИИТ)\n\nВыбери по кнопке направление по которому ты хочешь узнать свой рейтинг.", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, get_info)    
        
def get_info(message):
    global Naprav
    global flag
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
    but_yes = types.KeyboardButton("Да")
    but_no = types.KeyboardButton("Нет")
    markup_reply.add(but_yes, but_no)    
    if message.text == "БИ":
        Naprav = "БИ"
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    elif message.text == "ИБ":
        Naprav = "ИБ"
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    elif message.text == "ИСТ":
        Naprav = "ИСТ"
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    elif message.text == "ПИ":
        Naprav = "ПИ"
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    elif message.text == "ПМ":
        Naprav = "ПМ"
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    elif message.text == "ПМИ":
        Naprav = "ПМИ"
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    elif message.text == "ФИИТ":
        Naprav = "ФИИТ"   
        msg = bot.send_message(message.chat.id, "Ты гражданин РФ?", parse_mode='html', reply_markup = markup_reply)
        bot.register_next_step_handler(msg, inostr)        
    else:
        msg = bot.send_message(message.chat.id, "Извините, направление по такому запросу отсутствует.", parse_mode='html')
        flag = 'Ошибка'
        bot.register_next_step_handler(msg, welcome)
               
def inostr(message):
    global Inostranec
    global Naprav
    global flag
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
    but_bud = types.KeyboardButton("Бюджет")
    but_vne = types.KeyboardButton("Внебюджет")
    markup_reply.add(but_bud, but_vne)    
    if message.text == "Нет":
        Inostranec = True
        if Naprav == "ИБ":
            msg = bot.send_message(message.chat.id, "Извините, направление по такому запросу отсутствует.", parse_mode='html')
            flag = 'Ошибка'
            bot.register_next_step_handler(msg, welcome)
        else:
            msg = bot.send_message(message.chat.id, "Введите свой id абитуриента или снилс", parse_mode='html')
            bot.register_next_step_handler(msg, proverka)
            
    elif message.text == "Да":
        Inostranec = False
        msg = bot.send_message(message.chat.id, "На какой тип обучения ты подавал заявление?", parse_mode='html', reply_markup = markup_reply)    
        bot.register_next_step_handler(msg, budget)
    else: 
        msg = bot.send_message(message.chat.id, "Неверно набранно!", parse_mode='html')
        flag = 'Ошибка'
        bot.register_next_step_handler(msg, welcome)

def budget(message):
    global Budget
    global flag
    markup_inline1 = types.InlineKeyboardMarkup(row_width = 2)
    button = types.InlineKeyboardButton("Где находится номер снилса?", parse_mode='html', callback_data = "ok")
    markup_inline1.add(button)
    if message.text == "Бюджет":
        Budget = "Бюджет"
        msg = bot.send_message(message.chat.id, "Введите свой снилс", parse_mode='html', reply_markup = markup_inline1)
        bot.register_next_step_handler(msg, proverka)
    elif message.text == "Внебюджет":
        Budget = "Внебюджет"
        msg = bot.send_message(message.chat.id,"Введите свой снилс", parse_mode='html', reply_markup = markup_inline1)
        bot.register_next_step_handler(msg, proverka)
    else: 
        msg = bot.send_message(message.chat.id, "Неверно набранно! Для того, чтобы продолжить отправьте любой символ", parse_mode='html')
        flag = 'Ошибка'
        bot.register_next_step_handler(msg, welcome)        
                
def proverka(message):
    global Inostranec
    global Naprav
    global Budget
    global sp
    global silka
    global snils
    global flag
    if flag == 'репит':
        bot.send_message(message.chat.id, "Введите свой снилс ещё раз", parse_mode='html')
    snils = message.text
    if Inostranec == True:
        if Naprav == "БИ":
            silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1558&p_inst=0&p_category=2'         
        elif Naprav == "ИСТ":
            silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1556&p_inst=0&p_category=2'
        elif Naprav == "ПИ":
            silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1557&p_inst=0&p_category=2'
        elif Naprav == "ПМ":
            silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1790&p_inst=0&p_category=2'
        elif Naprav == "ПМИ":
            silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1553&p_inst=0&p_category=2'                
        elif Naprav == "ФИИТ":
            silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1554&p_inst=0&p_category=2'
        else: 
            bot.send_message(message.chat.id, "Извините, направление по такому запросу отсутствует", parse_mode='html')           
    else:
        if Budget == "Бюджет":
            if Naprav == "БИ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=203&p_inst=0&p_typeofstudy=1'         
            elif Naprav == "ИБ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=369&p_inst=0&p_typeofstudy=1'       
            elif Naprav == "ИСТ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=370&p_inst=0&p_typeofstudy=1'
            elif Naprav == "ПИ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=1084&p_inst=0&p_typeofstudy=1'
            elif Naprav == "ПМ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=559&p_inst=0&p_typeofstudy=1'
            elif Naprav == "ПМИ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=166&p_inst=0&p_typeofstudy=1'                
            elif Naprav == "ФИИТ":
                silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality=167&p_inst=0&p_typeofstudy=1'
            else: 
                bot.send_message(message.chat.id, "Извините, направление по такому запросу отсутствует! Для того, чтобы продолжить отправьте любой символ",  parse_mode='html')                 
        elif Budget == "Внебюджет":
                if Naprav == "БИ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=203&p_inst=0&p_category=2'         
                elif Naprav == "ИБ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=369&p_inst=0&p_category=2'       
                elif Naprav == "ИСТ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=370&p_inst=0&p_category=2'
                elif Naprav == "ПИ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=1084&p_inst=0&p_category=2'
                elif Naprav == "ПМ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=559&p_inst=0&p_category=2'
                elif Naprav == "ПМИ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=166&p_inst=0&p_category=2'                
                elif Naprav == "ФИИТ":
                    silka = 'https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=167&p_inst=0&p_category=2'
                else: 
                    msg = bot.send_message(message.chat.id, "Извините, направление по такому запросу отсутствует! Для того, чтобы продолжить отправьте любой символ", parse_mode='html')
                    flag = 'Ошибка'
                    bot.register_next_step_handler(msg, welcome)
                    
                    
    sp = parser(silka)
    print(sp)
    for i in range(0, len(sp)):
        if sp[i] == snils:
            bot.send_message(message.chat.id, "Ваше место в рейтинге: " + str(sp[i-1]) + "\n" + "Всего подали заявления: " + str(sp[-2]), parse_mode='html')  
            markup_inline2 = types.InlineKeyboardMarkup(row_width = 2)
            button1 = types.InlineKeyboardButton("Да", parse_mode='html', callback_data = "reg")
            button2 = types.InlineKeyboardButton("Нет", parse_mode='html', callback_data = "nereg")
            markup_inline2.add(button1, button2)    
            bot.send_message(message.chat.id, "Желаете остаться в системе?", parse_mode='html', reply_markup = markup_inline2)            
            break
    else: 
        msg = bot.send_message(message.chat.id, "Не удалось найти такого номера снилс или ID. Введите его еще раз", parse_mode='html')
        bot.register_next_step_handler(msg, proverka)
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global flag
    try:
        if call.message:
            if call.data == 'ok':
                bot.send_photo(call.message.chat.id, 'https://upload.wikimedia.org/wikipedia/commons/c/cd/СНИЛС.jpg')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите свой снилс", reply_markup=None)
            elif call.data == 'reg':
                flag = 'финал'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Желаете остаться в системе?", reply_markup=None)
                msg = bot.send_message(call.message.chat.id, "Отлично! Для того, чтобы продолжить отправьте любой символ", parse_mode='html')
                bot.register_next_step_handler(msg, final)
            elif call.data == 'nereg':
                bot.send_message(call.message.chat.id, "Ваc понял! Для того, чтобы заново запустить бота напишите /start или /help", parse_mode='html')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Желаете остаться в системе?", reply_markup=None)
    except Exception as e:
        print(repr(e))
def final(message):   
    global sp
    global silka
    global flag
    if flag == 'финал':
        markup_reply45 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        rezultat = types.KeyboardButton("Узнать рейтинг!")
        markup_reply45.add(rezultat)
        msg = bot.send_message(message.chat.id, "Вы успешно зарегестрировались!", parse_mode='html', reply_markup = markup_reply45)
        bot.register_next_step_handler(msg, sad)
    
def sad(message):
    if message.text == "Узнать рейтинг!":
        sp = parser(silka)
        print(sp)
        for i in range(0, len(sp)):
            if sp[i] == snils:
                msg = bot.send_message(message.chat.id, "Ваше место в рейтинге: " + str(sp[i-1]) + "\n" + "Всего подали заявления: " + str(sp[-2]), parse_mode='html')
                bot.register_next_step_handler(msg, sad)
    else:
        msg =bot.send_message(message.chat.id, "Для того, чтобы заново запустить бота напишите /start или /help", parse_mode='html')
        bot.register_next_step_handler(msg, welcome)
def parser(silka):
    url = silka
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find()
    spisok = soup.get_text()
    spisok = spisok.split('\n')
    b = []
    for i in spisok:
        if i == '' or i == '\xa0' or i == '0' or i == 'ВНУ, ВНУ' or i == 'участвует в конкурсе' or i == 'нет' or i == 'да' or i == 'ЕГЭ, ЕГЭ' or i == 'ЕГЭ, ЕГЭ, ЕГЭ' or i == 'зачислен' or i == 'не сданы один или несколько экзаменов (внутренние испытания)' or i == 'ВНУ, ВНУ, ВНУ':
            pass
        else: b.append(i)
    for ind in range(0, len(b)):
        if b[ind] == "1":
            w = ind     
    spisok = []
    for i in range(w, len(b)):
        spisok.append(b[i])
    while len(spisok[-1]) == 1 or len(spisok[-1]) == 2 or len(spisok[-1]) == 3:
        spisok.pop(-1)
    return spisok
    
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()