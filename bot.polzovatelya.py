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

bot = telebot.TeleBot(token)

access_key = 'a205a92c-c6c2-4486-b4e6-d7e301c5e4b4'
headers = {
    'X-Yandex-Weather-Key': access_key
}
response = requests.get('https://api.weather.yandex.ru/v2/forecast?lat=57.9194&lon=59.965', headers=headers)
pogod = response.json()
times = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00','08:00', '09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00', '17:00','18:00','19:00','20:00','21:00','22:00','23:00']
# for i in range(7):
#     date = pogod['forecasts'][i]['date']
#     data.append(date)

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
    keyboard = types.InlineKeyboardMarkup()
    file = open("worker.json", 'r', encoding="utf-8")
    data = json.load(file)
    for i in range(len(data)):
        button = types.InlineKeyboardButton(text=data[i]['worker'], callback_data=data[i]['worker'])
        workerr.append(data[i]['worker'])
        keyboard.add(button)
    file.close()
    bot.send_message(message.from_user.id, text='Выберите ответственного за проведение данного вида работ!', reply_markup=keyboard)
def grafik():
    global datt
    global worker1
    global workerr1
    file = open("grafik.json", 'r', encoding="utf-8")
    if len(file.readlines()) == 0:
        data = []
    else:
        file.seek(0)
        data = json.load(file)
    file.close()
    file = open("grafik.json", 'w', encoding="utf-8")
    has_date = False
    for i in range(len(data)):
        if data[i]['date'] == datt[0]:
            worker1 = worker1[0]
            workerr1 = workerr1[0]
            data[i]['work'] = worker1
            data[i]['worker'] = workerr1
            has_date = True
            break
    if not has_date:
        data.append(
            {
                'date': datt[0],
                'work': worker1[0],
                'worker': workerr1[0]
            }
        )
    json.dump(data, file, ensure_ascii=False)
    file.close()
    datt = []
    worker1 = []
    workerr1 = []

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
    if call.data == 'Добавление работы':
        bot.send_message(call.from_user.id, text='Напишите название работы!')
        bot.register_next_step_handler(call.message, add_work)
    if call.data == 'Сотрудники':
        bot.send_message(call.from_user.id, text='Введите Ф.И.О сотрудника!')
        bot.register_next_step_handler(call.message, add_worker)
    if call.data == 'График':
        workkk = []
        keyboard = types.InlineKeyboardMarkup()
        file = open("work-types.json", 'r', encoding="utf-8")
        data = json.load(file)
        for i in range(len(data)):
            button = types.InlineKeyboardButton(text=data[i]['name'], callback_data=data[i]['name'])
            workkk.append(data[i]['name'])
            keyboard.add(button)
        file.close()
        bot.send_message(call.from_user.id, text='Выберите вид проводимых работ!', reply_markup=keyboard)
    for i in range(len(workkk)):
        if call.data == workkk[i]:
            worker1.append(workkk[i])
            bot.send_message(call.from_user.id, text='Укажите дату проведения работ в формате dd.mm.yyyy!(Например: 11.01.2024')
            bot.register_next_step_handler(call.message, datee)
    for i in range(len(workerr)):
        if call.data == workerr[i]:
            workerr1.append(workerr[i])
            grafik()
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
bot.polling(non_stop=True, interval=0)

