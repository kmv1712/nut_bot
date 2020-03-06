import requests
import random
import json
import os

from flask import Flask
from flask import request
from flask import jsonify

# from flask_sslify import SSLify


app = Flask(__name__)
# sslify = SSLify(app)

TOKEN=''
URL = 'https://api.telegram.org/bot{0}/'.format(TOKEN)

TEXT_INSTRUCTIONS = '''
Здравствуйте, это телеграмм бот \n
для заказа сухофруктов.\n
\n
Чтобы сделать заказ:\n

1) Введите команду /list\n

2) Выбираете номер сухофрукта\n
   из списка.\n
 \n
Например: Курага с номером 26\n
и умножаете на 200 грамм:\n
26*200\n
если вам нужен например еще\n
Чернослив (36) 100 грамм\n
то пишите:\n
+ 36*100\n
3) В конце через пробел укажите\n
   место куда доставить товар.\n
   (Доставка только по г.Екатеринбург)\n
  \n 
4) В итоге вы отправите сообщение:\n
1*200+2*100 Ленина 32, кв.40 \n
\n
или 
\n
1*200+2*100 Ленина 32 подъезд №1\n
\n
5) После вы получите сообщение\n 
\n
    Вы заказали:\n
    Курага 200 гр Цена: 100 руб.\n
    Чернослив 100 гр Цена: 100 руб.\n 
    Общая сумма заказа: 200 руб.\n
    \n
    Будет выполнена доставка по адресу:\n
    Ленина 32 подъезд №1\n
    \n
    Оформить заказ?Да/Нет\n
    \n
6) При выборе Да получите сообщение\n
\n
    Как вы хотите оплатить товар?\n
    (Выберите соответствующую цифру)\n
    1.Оплатить онлайн\n
    2.Наличными курьеру\n
    3.Банковсой картой курьеру\n
    \n
7) При выборе 2 или 3 получите\n 
сообщение\n
\n
 Ваш заказ принят. № 321\n
 Спасибо за заказ!\n
'''

TEXT_PAYMENT_METHOD = '''
Как вы хотите оплатить товар?\n
(Выберите соответствующую цифру)\n
1 Оплатить онлайн\n
2 Наличными курьеру\n
3 Банковсой картой курьеру\n
\n'''

TOTAL_PRICE_ADDRESS = '''
Общая сумма заказа: {0} руб.\n
\n
Будет выполнена доставка по адресу:\n
{1}\n
\n
Оформить заказ?Да/Нет'''

NOMENCLTURE_WITH_PRICE = '''
Цены за в рублях за 100 грамм🌰!\n
1) Орех кедровый(очищенный) \n
2) Орех макадам 7,8\n
3) Орех грецкий (бабочка)650\n
4) Грецкий орех очищенный  530\n
5) Грецкий орех не очищенный 300\n
6) Фисташки Иран 1050\n
7) Фисташки натуральные 860\n
8) Миндаль Иран 750\n
9) Миндаль очищенный  700р\n 
10)Миндаль не очищений (Узбекистан)550\n
11)Миндаль в шоколаде 480р\n
12)Кешью очищенный 800р\n
13)Кокос кубик 640\n
14)Кешью в шоколаде 480р\n
15)Фундук очищенный 600\n
16)Фундук не очищенный 320\n
17)Фундук в шоколаде 500р\n
18)Орех пекан очищенный 1350\n
19)Орех бразильский 980\n
20)Арахис очищенный  140р\n
21)Арахис не очищенный 120р\n
22)Арахис соленный 180р \n
23)Арахис жарен. 160р\n
24)Арахис в кунжуте 180р\n
25)Курага для компота 160\n
26)Курага обычная 200р\n
27)Курага медовый 240\n
28)Курага пуговка 240\n
29)Курага лодка 220\n
30)Курага сахарная  250р\n
31)Курага турецкая  320р\n
32)Курага шоколадная 450р\n
33)Курага в шоколаде 400р\n
34)Урюк Таджикистан 260\n
35)Урюк турецкий 350р\n
36)Чернослив 150\n
37)Чернослив пуговка 170\n
38)Чернослив Молдова 240\n
39)Чернослив Молдова с косточки 205\n
40)Чернослив в банке 500гр 200р шт\n
41)Чернослив в шоколаде  400р \n
42)Чернослив президентский 380\n
43)Инжир 350р\n
44)Финики 110р\n
45)Финик золотой 160\n
46)Финик шоколадная 260\n
47)Финики каспиран 260\n
48)Финики Тунис 250р\n
'''

NUMBER_AND_NAME_NOMENCLATURE = {
    '1': 'Орех кедровый 14 очищенный ',
    '2': 'Орех макадам 7,8',
    '3': 'Орех грецкий (бабочка) 650',
    '4': 'Грецкий орех очищенный  530',
    '5': 'Грецкий орех не очищенный 300',
    '6': 'Фисташки Иран 1050',
    '7': 'Фисташки натуральные 860',
    '8': 'Миндаль Иран 750',
    '9': 'Миндаль очищенный  700р',
    '10': 'Миндаль не очищений Узбекистан 550',
    '11': 'Миндаль в шоколаде 480р',
    '12': 'Кешью очищенный 800р',
    '13': 'Кокос кубик 640',
    '14': 'Кешью в шоколаде 480р',
    '15': 'Фундук очищенный 600',
    '16': 'Фундук не очищенный 320',
    '17': 'Фундук в шоколаде 500р',
    '18': 'Орех пекан очищенный 1350',
    '19': 'Орех бразильский 980',
    '20': 'Арахис очищенный  140р',
    '21': 'Арахис не очищенный 120р',
    '22': 'Арахис соленный 180р ',
    '23': 'Арахис жарен. 160р',
    '24': 'Арахис в кунжуте 180р',
    '25': 'Курага для компота 160',
    '26': 'Курага обычная 200р',
    '27': 'Курага медовый 240',
    '28': 'Курага пуговка 240',
    '29': 'Курага лодка 220',
    '30': 'Курага сахарная  250р',
    '31': 'Курага турецкая  320р',
    '32': 'Курага шоколадная 450р',
    '33': 'Курага в шоколаде 400р',
    '34': 'Урюк Таджикистан 260',
    '35': 'Урюк турецкий 350р',
    '36': 'Чернослив 150',
    '37': 'Чернослив пуговка 170',
    '38': 'Чернослив Молдова 240',
    '39': 'Чернослив Молдова с косточки 205',
    '40': 'Чернослив в банке 500гр 200р шт',
    '41': 'Чернослив в шоколаде  400р ',
    '42': 'Чернослив президентский 380',
    '43': 'Инжир 350р',
    '44': 'Финики 110р',
    '45': 'Финик золотой 160',
    '46': 'Финик шоколадная 260',
    '47': 'Финики каспиран 260',
    '48': 'Финики Тунис 250р'
}

NUMBER_AND_PRICE_NOMENCLATURE = {str(item): random.randint(1, 20) for item in range(1, 70)}


# {
# '1': 14,
# '2': 7.8,
# '3': 6.50,
# '4': 5.30,
# '5': 'Грецкий орех не очищенный 300',
# '6': 'Фисташки Иран 1050',
# '7': 'Фисташки натуральные 860',
# '8': 'Миндаль Иран 750',
# '9': 'Миндаль очищенный  700р',
# '10': 'Миндаль не очищений Узбекистан 550',
# '11': 'Миндаль в шоколаде 480р',
# '12': 'Кешью очищенный 800р',
# '13': 'Кокос кубик 640',
# '14': 'Кешью в шоколаде 480р',
# '15': 'Фундук очищенный 600',
# '16': 'Фундук не очищенный 320',
# '17': 'Фундук в шоколаде 500р',
# '18': 'Орех пекан очищенный 1350',
# '19': 'Орех бразильский 980',
# '20': 'Арахис очищенный  140р',
# '21': 'Арахис не очищенный 120р',
# '22': 'Арахис соленный 180р ',
# '23': 'Арахис жарен. 160р',
# '24': 'Арахис в кунжуте 180р',
# '25': 'Курага для компота 160',
# '26': 'Курага обычная 200р',
# '27': 'Курага медовый 240',
# '28': 'Курага пуговка 240',
# '29': 'Курага лодка 220',
# '30': 'Курага сахарная  250р',
# '31': 'Курага турецкая  320р',
# '32': 'Курага шоколадная 450р',
# '33': 'Курага в шоколаде 400р',
# '34': 'Урюк Таджикистан 260',
# '35': 'Урюк турецкий 350р',
# '36': 'Чернослив 150',
# '37': 'Чернослив пуговка 170',
# '38': 'Чернослив Молдова 240',
# '39': 'Чернослив Молдова с косточки 205',
# '40': 'Чернослив в банке 500гр 200р шт',
# '41': 'Чернослив в шоколаде  400р ',
# '42': 'Чернослив президентский 380',
# '43': 'Инжир 350р',
# '44': 'Финики 110р',
# '45': 'Финик золотой 160',
# '46': 'Финик шоколадная 260',
# '47': 'Финики каспиран 260',
# '48': 'Финики Тунис 250р'
# }


def write_json(chat_id, dict_info_about_user, filename='orders.json'):
    list_orders = []
    dict_orders = {}

    if os.path.exists('orders.json'):
        with open('orders.json', 'r') as f:
            dict_orders = json.loads(f.read())

    i = 0
    for i in range(1, 1000):
        if i in [item.get('number_order') for item in dict_orders.get(str(chat_id)) or []]:
            continue
        dict_info_about_user['number_order'] = i
        break

    list_orders.append(dict_info_about_user)
    dict_orders[str(chat_id)] = list_orders

    with open(filename, 'w') as f:
        f.write(json.dumps(dict_orders))

    return i


https_proxy = "https://136.243.47.220:3128"

proxy_dict = {
    "https": https_proxy
}


def send_message(chat_id, text=''):
    url = '{0}{1}'.format(URL, 'sendMessage')
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer, proxies=proxy_dict)
    return r.json()


def get_result_text(dict_info_about_user):
    """Получить текст с названием товара, введеныx пользователем грамм, ценой с учетом выбранных грамм. Итоговую цену.

    Args:
        dict_info_about_user(dict): Информация о пользователе, его заказе и адресе доставки.

    Returns:
        str
    """
    list_result_text = []
    for item in dict_info_about_user.get('ordered_nomenclatures') or []:
        list_result_text.append('{0} {1} грамм Цена:{2} руб\n'.format(item.get('name_nomenclature'),
                                                                      str(item.get('weight')),
                                                                      str(item.get('price'))))

    list_result_text.append(TOTAL_PRICE_ADDRESS.format(str(dict_info_about_user.get('total_price')),
                                                       str(dict_info_about_user.get('address'))))
    result = '\n'.join(list_result_text)
    return result


def get_dict_info_about_user(r):
    dict_info_user = {
        'first_name': r.get('message', {}).get('from', {}).get('first_name'),
        'last_name': r.get('message', {}).get('from', {}).get('last_name'),
        'id': r.get('message', {}).get('from', {}).get('id'),
        'date': r.get('message', {}).get('date'),
        'text': r.get('message', {}).get('text')
    }
    return dict_info_user


def get_dict_info_about_user_with_order_total_price(dict_info_about_user):
    address = ''
    order = ''
    message = (dict_info_about_user.get('text') or '')

    # Получим адресс и текст с 1*100+2*300
    for i, item in enumerate(message):
        if item.isalpha():
            order = message[0:i]
            address = message[i:len(message)]
            dict_info_about_user['address'] = address
            break

    order_without_spaces = message.replace(' ', '') if not order else order.replace(' ', '')

    list_part_order = order_without_spaces.split('+')

    ordered_nomenclatures = []
    total_price = 0
    for part_order in list_part_order or []:
        part_order = part_order.split('*')
        number_nomenclature = part_order[0]
        gramm = part_order[1]
        gramm_int = int(gramm)
        price = gramm_int * NUMBER_AND_PRICE_NOMENCLATURE.get(number_nomenclature)
        info_about_ordered_nomenclature = {
            'name_nomenclature': NUMBER_AND_NAME_NOMENCLATURE.get(number_nomenclature),
            'weight': gramm,
            'price': price
        }
        ordered_nomenclatures.append(info_about_ordered_nomenclature)
        total_price += price

    dict_info_about_user['ordered_nomenclatures'] = ordered_nomenclatures
    dict_info_about_user['total_price'] = total_price

    return dict_info_about_user


def write_json_del(chat_id):
    dict_orders = {}
    if not os.path.exists('orders.json'):
        return

    with open('orders.json', 'r') as f:
        dict_orders = json.loads(f.read())
        list_orders = dict_orders.get(str(chat_id))
        if not list_orders:
            return
        list_orders.pop()

    with open('orders.json', 'w') as f:
        f.write(json.dumps(dict_orders))


def write_json_add_payment_method(chat_id, message):
    dict_orders = {}
    if not os.path.exists('orders.json'):
        return

    with open('orders.json', 'r') as f:
        dict_orders = json.loads(f.read())
        list_orders = dict_orders.get(str(chat_id))
        if not list_orders:
            return
        message = message.replace(' ', '')
        try:
            message = int(message)
        except (TypeError, ValueError):
            message = 0
        list_orders[-1]['payment_method'] = message
        number_order = list_orders[-1].get('number_order')

    with open('orders.json', 'w') as f:
        f.write(json.dumps(dict_orders))

    return number_order


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if message == '/start':
            send_message(chat_id, text=TEXT_INSTRUCTIONS)
        elif message == '/list':
            send_message(chat_id, text=NOMENCLTURE_WITH_PRICE)
        elif '*' in message:
            dict_info_about_user = get_dict_info_about_user(r)
            dict_info_about_user = get_dict_info_about_user_with_order_total_price(dict_info_about_user)
            write_json(chat_id, dict_info_about_user)
            result_text = get_result_text(dict_info_about_user)
            send_message(chat_id, text=result_text)
        elif 'Да' == (message or '').replace(' ', ''):
            send_message(chat_id, text=TEXT_PAYMENT_METHOD)

        elif 'Нет' == (message or '').replace(' ', ''):
            write_json_del(chat_id)
            send_message(chat_id, text='''Ваш заказ не принят''')
        elif '1' == (message or '').replace(' ', ''):
            send_message(chat_id, text='''Приносим извинения, данный функционал пока не работает''')
        elif '2' == (message or '').replace(' ', ''):
            number_order = write_json_add_payment_method(chat_id, message)
            send_message(chat_id, text=('''Ваш заказ принят. № {0}\n Спасибо за заказ!\n''').format(number_order))
        elif '3' == (message or '').replace(' ', ''):
            number_order = write_json_add_payment_method(chat_id, message)
            send_message(chat_id, text=('''Ваш заказ принят. № {0}\n Спасибо за заказ!\n''').format(number_order))

    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
