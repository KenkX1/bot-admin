import requests
import telebot
from telebot import types
import json

token = "7116003817:AAGqDAV8Ph_7keIni1ofhOSkiKOStQaHV_o"

# Работа с графиком:
#
# 1. Выбрать тип работ.
# 2. Указать дату.
# 3. После выбора даты показать список часов, доступных для работы, пример:
# 08.00 - 09.00
# 13.00 - 14.00
# 14.00 - 15.00
# 17.00 - 18.00
# 3 продолжение: и просим пользователя указать время начала работ (пишем часы или выбираем)
# 4. Просим указать время окончания работ (пишем часы или выбираем).
#
# 3 и 4: если вдруг пишет пользователь часы, надо проверить а доступно ли время или нет.
#
# 5. Выбираем ответственного за работу.

#1.После выбора даты дать выбор действия изменение или добавление
#2.в случае изменнения дополнительно спрашиваем, что нужно изменить

bot = telebot.TeleBot(token)

access_key = 'a205a92c-c6c2-4486-b4e6-d7e301c5e4b4'
headers = {
    'X-Yandex-Weather-Key': access_key
}
response = requests.get('https://api.weather.yandex.ru/v2/forecast?lat=57.9194&lon=59.965', headers=headers)
pogod = response.json()
times = ["8","9","10","11","12","13","14","15","16","17","18","19","20","21"]
zan_time = []
cvobod_time = ''
cvobod_time1 = []
cvobod_time2 = []

active_day = None
active_nach_time = None
active_kon_time = None

name = []
start_temp = []
end_temp = []
worker = []
post = []
tg = []
wr1 = []
data = []
worker1 = []
datt = []
workkk = []
workerr = []
workerr1 = []
fallout = []
nach_rabot = []
kon_rabot = []
vid_rabot_graf = []
vse_rabot_graf = []
worker11 = []
data_izm1 = []
vse = []
def add_works():
    global name
    global start_temp
    global end_temp
    global data
    global fallout
    file = open("work-types.json", 'r', encoding="utf-8")
    if len(file.readlines()) == 0:
        data = []
    else:
        file.seek(0)
        data = json.load(file)
    file.close()
    file = open("work-types.json", 'w', encoding="utf-8")
    data.append(
        {
            'name': name[0],
            'start_temp': start_temp[0],
            'end_temp': end_temp[0],
            'fallout': fallout[0]
        }
    )
    json.dump(data, file, ensure_ascii=False)
    file.close()
    name = []
    start_temp = []
    end_temp = []
    fallout = []
def add_work(message):
    name.append(message.text)
    bot.send_message(message.from_user.id, text='Напишите минимальный порог температуры работы!')
    bot.register_next_step_handler(message, add_start)
def add_start(message):
    start_temp.append(message.text)
    bot.send_message(message.from_user.id, text='Напишите максимальный порог температуры работы!')
    bot.register_next_step_handler(message, add_end)
def add_end(message):
    end_temp.append(message.text)
    add_fallout(message)

def add_fallout(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Да', callback_data='True')
    button2 = types.InlineKeyboardButton(text='Нет',
                                         callback_data='False')
    keyboard.add(button1, button2)
    bot.send_message(message.from_user.id, text='Возможны ли осадки при проведение данных работ?', reply_markup=keyboard)


def add_worker(message):
    worker.append(message.text)
    bot.send_message(message.from_user.id, text='Введите должность сотрудника!')
    bot.register_next_step_handler(message, add_post)
def add_post(message):
    post.append(message.text)
    bot.send_message(message.from_user.id, text='Введите ссылку на телеграмм сотрудника!')
    bot.register_next_step_handler(message, add_tg)
def add_tg(message):
    global worker
    global post
    global tg
    global data
    tg.append(message.text)
    file = open("worker.json", 'r', encoding="utf-8")
    if len(file.readlines()) == 0:
        data = []
    else:
        file.seek(0)
        data = json.load(file)
    file.close()
    file = open("worker.json", 'w', encoding="utf-8")
    data.append(
        {
            'worker': worker[0],
            'post': post[0],
            'tg': tg[0]
        }
    )
    json.dump(data, file, ensure_ascii=False)
    text = ''
    text += 'Сотрудник добавлен!' + '\n' + 'Предоставляю вам информацию о том, что вы добавили!' + '\n' + 'Ф.И.О сотрудника: ' + worker[0] + '\n' + 'Должность: ' + post[0] + '\n' + 'Телеграмм сотрудника:' + tg[0]
    bot.send_message(message.from_user.id, text)
    file.close()
    worker = []
    post = []
    tg = []
def woork(message):
    file = open("work-types.json", 'r', encoding="utf-8")
    data = json.load(file)
    for i in range(len(data)):
        print(data[i]['name'])
    file.close()
def datee(message):
    global datt
    datt.append(message.text)
    grafik(message)
def grafik(call_data):
    global datt
    global worker1
    global workerr1
    global cvobod_time
    global cvobod_time1
    global cvobod_time2
    global zan_time
    cvobod_time1 = []
    cvobod_time2 = []
    cvobod_time = ""
    zan_time = []
    file = open("grafik.json",'r',encoding="utf-8")
    if len(file.readlines()) == 0:
        data = []
    else:
        file.seek(0)
        data = json.load(file)
    file.close()
    for i in range(8, 22):
        # print(data[worker1[0][datt[0]]])
        if datt[0] not in data[str(worker1[0])]:
            zan_time = zan_time
        elif str(i) in data[str(worker1[0])][datt[0]]:
            zan_time.append(str(i))
    for i in range(8,22):
        if str(i) not in zan_time:
            cvobod_time1.append(str(i) + ':00')
            cvobod_time2.append(str(i) + ':00')
            cvobod_time += str(i) + ":00" + "-" + str(i + 1) + ':00' + '\n'
    text = 'Список часов доступных для работы:' + '\n' + cvobod_time
    bot.send_message(call_data.chat.id, text=text)
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Добавить время с помощью кнопок', callback_data='Кнопки')
    button2 = types.InlineKeyboardButton(text="Добавить время вручную",
                                         callback_data='Вручную')
    # Добавляем кнопки для клавиатуры
    keyboard.add(button1, button2)
    # Отправляем ответное сообщение
    bot.send_message(call_data.chat.id, text='Выберите каким способом вы будете выбирать время?!', reply_markup=keyboard)
    # file = open("grafik.json", 'r', encoding="utf-8")
    # if len(file.readlines()) == 0:
    #     data = []
    # else:
    #     file.seek(0)
    #     data = json.load(file)
    # file.close()
    # file = open("grafik.json", 'w', encoding="utf-8")
    # has_date = False
    # for i in range(len(data)):
    #     if data[i]['date'] == datt[0]:
    #         worker1 = worker1[0]
    #         workerr1 = workerr1[0]
    #         data[i]['work'] = worker1
    #         data[i]['worker'] = workerr1
    #         has_date = True
    #         break
    # if not has_date:
    #     data.append(
    #         {
    #             'date': datt[0],
    #             'work': worker1[0],
    #             'worker': workerr1[0]
    #         }
    #     )
    # json.dump(data, file, ensure_ascii=False)
    # file.close()
def kon_time(call_data):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(cvobod_time2)):
        button = types.InlineKeyboardButton(text=cvobod_time1[i], callback_data='endtime_'+cvobod_time1[i])
        keyboard.add(button)
    bot.send_message(call_data.message.chat.id, text="Выберите время конца работы:", reply_markup=keyboard)
def otvetsv(call_data):
    keyboard = types.InlineKeyboardMarkup()
    file = open("worker.json", 'r', encoding="utf-8")
    data = json.load(file)
    for i in range(len(data)):
        button = types.InlineKeyboardButton(text=data[i]['worker'], callback_data=data[i]['worker'])
        workerr.append(data[i]['worker'])
        keyboard.add(button)
    file.close()
    bot.send_message(call_data.from_user.id, text='Выберите ответственного за проведение данного вида работ!', reply_markup=keyboard)
def naach(message):
    global nach_rabot
    global datt
    global worker1
    nach_rabot.append(message.text)
    if nach_rabot[0] in cvobod_time1:
        bot.send_message(message.from_user.id, text="Выберите время конца работы:(Например,23:00)")
        bot.register_next_step_handler(message, kooon)
    else:
        bot.send_message(message.from_user.id, text="Этого времени нет или время уже занято в этом время!")
        nach_rabot = []
        datt = []
        worker1 = []
def kooon(message):
    global kon_rabot
    global nach_rabot
    global datt
    global worker1
    kon_rabot.append(message.text)
    if kon_rabot[0] in cvobod_time1 and kon_rabot != nach_rabot[0]:
        otvetsv(message)
    else:
        bot.send_message(message.from_user.id, text="Этого времени нет или время уже занято в этом время!")
        nach_rabot = []
        datt = []
        worker1 = []
        kon_rabot = []
def izm_graf(message):
    global worker1
    global datt
    global nach_rabot
    global kon_rabot
    global workerr1
    global worker11
    text = 'Предоставляю информацию о ваших изменениях:' + '\n' + 'Вид проводимых работ: ' + worker1[0] + '\n' + "Работа: " + worker11[0] +"\n" + 'Дата: ' + datt[0] + '\n' + 'Время работ: ' + nach_rabot[0] + '-' + kon_rabot[0]+ '\n' + 'Ответственный сотрудник: ' + workerr1[0]
    bot.send_message(message.from_user.id, text)

    file = open("grafik.json", 'r', encoding="utf-8")
    grafik = json.load(file)
    file.close()
    file = open("grafik.json", 'w', encoding="utf-8")
    nach_hour = int(nach_rabot[0].split(':')[0])
    kon_hour = int(kon_rabot[0].split(':')[0])
    if datt[0] not in grafik[worker1[0]]:
        grafik[worker1[0]][datt[0]] = {}
    for hour in range(nach_hour, kon_hour + 1):
        grafik[worker1[0]][datt[0]][str(hour)] = [
            {
                "date": datt[0],
                "work": worker11[0],
                "worker": workerr1[0]
            }
        ]
    json.dump(grafik, file, ensure_ascii=False)
    file.close()
    worker1 = []
    datt = []
    nach_rabot = []
    kon_rabot = []
    workerr1 = []
    worker11 = []
def data_izm1(message):
    global worker1
    global data_izm1
    data_izm1.append(message.text)
    file = open("grafik.json", 'r', encoding="utf-8")
    grafik = json.load(file)
    vse.append(grafik[worker1[0]][data_izm1[0]])

# Получение текстовых сообщений от бота
@bot.message_handler(content_types=['text'])
# Функция для получения сообщений от пользователя
def get_message(message):
    # Если текст полученного сообщения = '/start'
    if message.text == '/start':
        file = open("admins.json", 'r', encoding="utf-8")
        data = json.load(file)
        file.close()
        if str(message.from_user.id) not in data.keys():
            bot.send_message(message.from_user.id, text='У вас нет доступа')
        else:
            bot.send_message(message.from_user.id, text='Вам открыт доступ')
            bot.set_my_commands(
                commands=[
                    # Добавление команды /start с описанием "Запуск бота"
                    types.BotCommand('/start', 'Запуск бота')
                ],
                scope=types.BotCommandScopeChat(message.chat.id)
            )
            # Создаем клаиватуру с категориями товаров
            keyboard = types.InlineKeyboardMarkup()
            # Создаем кнопки с категорией товара
            button1 = types.InlineKeyboardButton(text='Добавление вида работы', callback_data='Добавление работы')
            button2 = types.InlineKeyboardButton(text='Добавление сотрудников, ответственных за выполнение работ', callback_data='Сотрудники')
            button3 = types.InlineKeyboardButton(text='Редактирование графика проведения работ', callback_data='График')
            # Добавляем кнопки для клавиатуры
            keyboard.add(button1 , button2 , button3)
            # Отправляем ответное сообщение
            bot.send_message(message.from_user.id, text='Привет!', reply_markup=keyboard)
# Обработка нажатий на кнопки из бота
@bot.callback_query_handler(func=lambda call: True)
# Функция для работы с нажатием на кнопку
def callback_worker(call):
    global wr1
    global worker1
    global workkk
    global workerr
    global workerr1
    global name
    global start_temp
    global end_temp
    global fallout
    global perevod
    global vse_rabot_graf
    global worker11
    if call.data == 'Добавление работы':
        bot.send_message(call.from_user.id, text='Напишите название работы!')
        bot.register_next_step_handler(call.message, add_work)
    if call.data == 'Сотрудники':
        bot.send_message(call.from_user.id, text='Введите Ф.И.О сотрудника!')
        bot.register_next_step_handler(call.message, add_worker)
    if call.data == 'График':
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Добавление', callback_data='Добавление')
        button2 = types.InlineKeyboardButton(text='Перенести работу',
                                             callback_data='Перенести работу')
        keyboard.add(button1, button2)
        bot.send_message(call.from_user.id, text='Выберите действие!', reply_markup=keyboard)
    if call.data == 'Добавление':
        vse_rabot_graf = []
        keyboard = types.InlineKeyboardMarkup()
        file = open("grafik.json",'r', encoding="utf-8")
        data = json.load(file)
        vse_rabot_graf = list(data.keys())
        for i in range(len(vse_rabot_graf)):
            button = types.InlineKeyboardButton(text=vse_rabot_graf[i], callback_data=vse_rabot_graf[i])
            keyboard.add(button)
        file.close()
        bot.send_message(call.from_user.id, text='Выберите вид проводимых работ!', reply_markup=keyboard)
    if call.data =='Перенести работу':
        vse_rabot_graf = []
        keyboard = types.InlineKeyboardMarkup()
        file = open("grafik.json", 'r', encoding="utf-8")
        data = json.load(file)
        vse_rabot_graf = list(data.keys())
        for i in range(len(vse_rabot_graf)):
            button = types.InlineKeyboardButton(text=vse_rabot_graf[i], callback_data=vse_rabot_graf[i] + "|")
            keyboard.add(button)
        file.close()
        bot.send_message(call.from_user.id, text='Выберите вид проводимых работ!', reply_markup=keyboard)

        # 1. Сделать выбор вида работ
        # 2. Укажите дату, работу которой надо перенести
        # 3. Показать список работ (выбранная дата и список пронумерованный из: работник, работа, время) и предоставить кнопки с цифрами для выбора.
        # в callback записать: date|work|worker

    for i in range(len(vse_rabot_graf)):
        if call.data == vse_rabot_graf[i] + "|":
            worker1.append(vse_rabot_graf[i])
            bot.send_message(call.from_user.id, text='Выберите дату в формате yyyy-mm-dd(Например: 11:00).')
            bot.register_next_step_handler(call.message, data_izm1)
    for i in range(len(vse_rabot_graf)):
        if call.data == vse_rabot_graf[i]:
            worker1.append(vse_rabot_graf[i])
            workkk = []
            keyboard = types.InlineKeyboardMarkup()
            file = open("work-types.json", 'r', encoding="utf-8")
            data = json.load(file)
            for i in range(len(data)):
                button = types.InlineKeyboardButton(text=data[i]['name'], callback_data=data[i]['name'])
                workkk.append(data[i]['name'])
                keyboard.add(button)
            file.close()
            bot.send_message(call.from_user.id, text='Выберите работу!', reply_markup=keyboard)
    for i in range(len(workkk)):
        if call.data == workkk[i]:
            worker11.append(workkk[i])
            bot.send_message(call.from_user.id, text='Укажите дату проведения работ в формате yyyy-mm-dd!(Например: 2024-01-23)')
            bot.register_next_step_handler(call.message, datee)
    for i in range(len(workerr)):
        if call.data == workerr[i]:
            workerr1.append(workerr[i])
            izm_graf(call)
            break
    if call.data == 'True':
        fallout.append('True')
        if fallout[0] == 'True':
            perevod = 'Да'
        text = ''
        text += "Работа добавлена!" + '\n' + 'Предоставляю вам информацию о том, что вы добавили!'+ '\n' + "Работа:" + name[0] + '\n' + "Минимальная температура: " + start_temp[0] +'\n' + "Максимальная температура: " + end_temp[0] +'\n'+ "Возможны ли осадки: " + perevod
        bot.send_message(call.from_user.id, text)
        perevod = []
        add_works()
    if call.data == 'False':
        fallout.append('False')
        if fallout[0] == 'False':
            perevod = 'Нет'
        text = ''
        text += "Работа добавлена!" + '\n' + 'Предоставляю вам информацию о том, что вы добавили!'+ '\n' + "Работа:" + name[0] + '\n' + "Минимальная температура: " + start_temp[0] +'\n' + "Максимальная температура: " + end_temp[0] +'\n'+ "Возможны ли осадки: " + perevod
        bot.send_message(call.from_user.id, text)
        perevod = []
        add_works()
    if call.data == 'Кнопки':
        keyboard = types.InlineKeyboardMarkup()
        for i in range(len(cvobod_time1)):
            button = types.InlineKeyboardButton(text=cvobod_time1[i], callback_data=cvobod_time1[i])
            keyboard.add(button)
        bot.send_message(call.from_user.id,text="Выберите время начала работы:",reply_markup=keyboard)

    if call.data.startswith('endtime'):
        time = call.data.split('_')[1]
        for i in range(len(cvobod_time1)):
            if time == cvobod_time1[i]:
                kon_rabot.append(time)
                break
        otvetsv(call)
    for i in range(len(cvobod_time1)):
        if call.data == cvobod_time1[i]:
            nach_rabot.append(cvobod_time1[i])
            kon_time(call)
            break
    if call.data == 'Вручную':
        bot.send_message(call.from_user.id, text="Выберите время начала работы:(Например,11:00)")
        bot.register_next_step_handler(call.message, naach)
bot.polling(non_stop=True, interval=0)