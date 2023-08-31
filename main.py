# -- Модули -- #
import telebot
from telebot import types
import sqlite3
from datetime import datetime,timedelta
import requests
import cfg
import certifi

# -- Делаем связь с токеном -- #
bot = telebot.TeleBot(cfg.bot_token,parse_mode='HTML')


# -- Создаем базу данных -- #
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Создание таблицы users, если она ещё не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER PRIMARY KEY,
        expiration_date DATETIME
    );
    ''')

    conn.commit()
    conn.close()

create_database()



# -- Добавляем подпиську -- #

def add_subscription(user_id, expiration_date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO subscriptions (user_id, expiration_date) VALUES (?, ?)",
                   (user_id, expiration_date))
    conn.commit()
    conn.close()

# -- Проверяем подписку -- #
def add_subscription(user_id, expiration_date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO subscriptions (user_id, expiration_date) VALUES (?, ?)",
                   (user_id, expiration_date))
    conn.commit()
    conn.close()

# Функция для проверки статуса подписки
def check_subscription_status(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT expiration_date FROM subscriptions WHERE user_id=?", (user_id,))
    subscription = cursor.fetchone()

    if subscription:
        expiration_date = subscription[0]
        date = datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S.%f')
        current_date = datetime.now()

        if current_date <= date:
            days_left = (date - current_date).days
            status = f"🔰 До конца подписки осталось {days_left} дней."
        else:
            status = "🔰 К сожалению, ваша подписка истекла."
    else:
        status = "🔰 У вас нет подписки!"

    conn.close()
    return status 

def check_subscription(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT expiration_date FROM subscriptions WHERE user_id=?", (user_id,))
    subscription = cursor.fetchone()
    conn.close()

    if subscription:
        expiration_date = subscription[0]
        date = datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S.%f')
        current_date = datetime.now()

        if current_date <= date:
            return True
        else:
            return False
    else:
        return False


@bot.message_handler(commands=['start'])
def start_cmd(message):
    register = check_user(message.chat.id)
    if register == False:
      markup = types.InlineKeyboardMarkup()
      continue_button = types.InlineKeyboardButton("✅ Продолжить", callback_data='continue')
      markup.add(continue_button)
      with open('had.jpg','rb') as had:
        bot.send_photo(message.chat.id,had,'<b>Привествую в BuddiesMailer!',parse_mode='HTML',reply_markup=markup)
    else:
        home(message)


@bot.message_handler(commands=['admin'])
def admin_cmd(message):
    if message.chat.id == cfg.admin_id:
        markup = types.InlineKeyboardMarkup()
        send_sub = types.InlineKeyboardButton("⚜ Выдать подписку", callback_data='send_sub')

       rassilka =
types.InlineKeyboardButton("⚜️ Рассылка", callback_data='rassilka')
       dump_base
types.InlineKeyboardButton("⚙️ Дамп БД",
callback_data='dumpbase')
        markup.add(send_sub)
        with open('had.jpg','rb') as had:
          bot.send_photo(chat_id=message.chat.id,photo=had,caption='<b>⚜ Админ-меню: </b>',reply_markup=markup)
    else:
        with open('had.jpg','rb') as had:
          bot.send_photo(chat_id=message.chat.id,photo=had,caption='<b>❌ Вы не являетесь администратором бота!</b>')

def home(message):
    if check_subscription(message.chat.id) == True:
      markup = types.InlineKeyboardMarkup(row_width=2)
      cabinet = types.InlineKeyboardButton("💻 Аккаунт", callback_data='cabinet')
      my_sub = types.InlineKeyboardButton("⚜ Подписка", callback_data='my_sub')
      send_mail = types.InlineKeyboardButton("📧 Отправить письмо", callback_data='send_mail')
      validaror_mail = 
types.InlineKeyboardButton("📪 Проверка почт", callback_data='valudaror_mail')
      markup.add(cabinet,my_sub,send_mail,valudaror_mail)
      with open('had.jpg','rb') as had:
        bot.send_photo(chat_id=message.chat.id,photo=had,caption='🏡 <b>Главное меню</b>',reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        cabinet = types.InlineKeyboardButton("💻 Аккаунт", callback_data='cabinet')
        my_sub = types.InlineKeyboardButton("⚜ Подписка", callback_data='my_sub')
        donate =
types.InlineKeyboardButton("💰 Пополнить баланс", callback_data='donate')
        markup.add(cabinet,my_sub,donate)
        with open('had.jpg','rb') as had:
          bot.send_photo(chat_id=message.chat.id,photo=had,caption='🏡 <b>Главное меню</b>',reply_markup=markup)


def check_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        return True 
    else:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

        return False

    conn.close()

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_button_click(call):
    user_id = call.message.chat.id
    if call.data == 'send_sub':
        bot.edit_message_caption(chat_id=user_id,message_id=call.message.id,caption='<b>⚜️ Укажите ID пользователя и кол-во дней через пробел:</b>')
        bot.register_next_step_handler(call.message,give_sub)
    elif call.data == 'my_sub':
        with open('had.jpg','rb') as had:
          bot.send_photo(user_id,had,check_subscription_status(user_id),reply_markup=del_markup)
    elif call.data == 'del':
        bot.delete_message(call.message.chat.id,call.message.id)

bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    elif call.data == 'cabinet':
        status = check_subscription_status(user_id)
        sub = 'Нет'
        if check_subscription(user_id) == True:
            sub = 'Да'
        bot.edit_message_caption(chat_id=user_id,message_id=call.message.id,reply_markup=back_markup,caption=f'🆔 Индификатор: {user_id}\n⚙️ Подписка: {sub}')
    elif call.data == 'back':
        home(call.message)
       
home(call.message)
        bot.delete_message(call.message.chat.id,call.message.id)
    elif call.data == 'send_mail':
        bot.edit_message_caption(chat_id=user_id,message_id=call.message.id,caption='<b>📥 Укажите отправителя письма: </b>')
        bot.register_next_step_handler(call.message,sm,call.message.id)


def sm(message,ms):
    if message.text:
        title = message.text
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>📥 Укажите получателя письма: </b>')
        bot.delete_message(message.chat.id,message.id)
        bot.register_next_step_handler(sender_email,recipient_emails,email_subject,pismo)
    else:
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>Я не вижу тут текст!</b>')


def sm1(message,title,ms):
    if message.text:
        text = message.text
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>📥 Укажите заголовок:</b>')
        bot.delete_message(message.chat.id,message.id)
        bot.register_next_step_handler(sender_email,recipient_emails,email_subject,pismo)
    else:
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>Я не вижу тут текст!</b>')


def sm2(message,title,text,ms):
    if message.text:
        otpr = message.text
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>📥 Укажите текст письма:</b>')
        bot.delete_message(message.chat.id,message.id)
        bot.register_next_step_handler(sender_email,recipient_emails,email_subject,pismo)
    else:
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>Я не вижу тут текст!</b>')


def sm3(otpr,ms,title,text):
    if message.text:
        to = message.text
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>📥 Отправляю сообщение...</b>')
        bot.delete_message(message.chat.id,message.id)
        send_mail(sender_email,recipient_emails,email_subject,pismo)
    else:
        bot.edit_message_caption(chat_id=message.chat.id,message_id=ms,caption='<b>❌ Только текстом.</b>')

def give_sub(message):
    if message.text:
        data = message.text.split(' ')
        expiration_date = datetime.now() + timedelta(days=int(data[1]))
        add_subscription(data[0],expiration_date)
        bot.edit_message_caption(chat_id=message.chat.id,message_id=message.id-1,caption=f'<b>✅ Пользователь {data[0]} получил {data[1]} дней подписки.</b>')
        bot.delete_message(chat_id=message.chat.id,message_id=message.id)
    else:
        pass


def send_mail(otpr,ms,title,text):
    email_text = message.text
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_text, 'plain'))

    try:
        with open(CONFIG_FILE, 'r') as file:
            config = file.read().splitlines()
            smtp_server = config[0]
            smtp_port = int(config[1])
            sender_email = config[2]
            sender_password = config[3]
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            sent_count = 0
            not_sent_count = 0
            error_message = ""

            start_time = datetime.datetime.now()

            for recipient_email in recipient_emails:
                try:
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    sent_count += 1
                except Exception as e:
                    not_sent_count += 1
                    error_message += f"✖️ Письмо не дошло на адрес(а):{recipient_email}: {str(e)}\n"

            end_time = datetime.datetime.now()
            total_time = end_time - start_time

            server.quit()

            if sent_count > 0:
                success_message = f"⚜️ Дошло писем: {sent_count}\n"
            else:
                success_message = ""

            if not_sent_count > 0:
                failure_message = f"🕸️ Не валидных почт: {not_sent_count}\n"
            else:
                failure_message = ""

            time_message = f"🕘 Время выполнения: {total_time}"

def valudaror_mail(message):
    emails = message.text.split(",")
    valid_emails = []
    invalid_emails = []

    for email in emails:
        if validate_email(email.strip()):
            valid_emails.append(email.strip())
        else:
            invalid_emails.append(email.strip())

    valid_count = len(valid_emails)
    invalid_count = len(invalid_emails)

    valid_emails_str = ", ".join(valid_emails)
    invalid_emails_str = ", ".join(invalid_emails)
    bot.send_message(message.chat.id, f"⚜️ Валидные: ({valid_count}): {valid_emails_str}\n✖️ Шлак: ({invalid_count}): {invalid_emails_str}")
    
    
if __name__ == '__main__':
    while True:
      try:
        send_log('<b>🔔 Бот запущен!</b>')
        bot.polling()
      except Exception as e:
          bot = telebot.TeleBot(cfg.bot_token,parse_mode='HTML')