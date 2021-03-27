#from bokeh.models import Scatter
import logging

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
# from django.http import  HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import Metering, Customer, Customerrec, Note

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import AuthUserForm, RegisterUserForm,CustomCheckbox
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
import pyodbc

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.mail import send_mail
#import secrets
import uuid
import os
from .forms import account_check
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView

# import numpy as np
# import pandas as pd
# import matplotlib
# import matplotlib.pyplot as plt
# matplotlib.style.use('ggplot')

#from bokeh.resources import INLINE
#import plotly.plotly as py
#import plotly.graph_objs as go
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#from  plotly.offline.offline import _plot_html

#from bokeh.util.string import encode_utf8
from django.contrib.auth import get_user_model
User = get_user_model()




password = {
    'FERM1':'1',
    'FERM2':'2',
    'FERM3':'3',
}

#http://127.0.0.1:8000/add/?login=FERM1&pasw=1&name=Buryonka&t=38&h=25&co2=7&ch4=31&n2o=17
#http://127.0.0.1:8000/add/?login=FERM2&pasw=2&name=Vestka&t=38&h=25&co2=2&ch4=21&n2o=11

# Create your views here.

#def test(request):
#    return HttpResponse("<h3>ТЕСТОВАЯ СТРАНИЦА ИСКУССТВЕННОГО ИНТЕЛЛЕКТА</h3>")

def start(request):
    print('start')
    X = []
    Y = []
    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated")
        print(request.user.is_authenticated)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)
        customer = a.customer_set.order_by('id')[:]
        for cus in customer:
            X.append(cus.account)
            Y.append(cus.bank)
        #print(X)
        #print(Y)
    else:
        print("User.is_not_authenticated")
        print(request.user.is_authenticated)
        X.append("0")
        Y.append(" ")

    if len(X) ==0:
        X.append("0")

    return render(request, 'ai/start.html', {'Acc': X[-1]})

def page1(request):
    return render(request, 'ai/page1.html')

def page2(request):
    return render(request, 'ai/page2.html')

def add(request):
    import os
    import sqlite3
    import urllib  # URL functions
    from time import strftime

    import urllib.request  # URL functions

    #now = datetime.datetime.now()
    now = timezone.now()
    nameandpaswcorrect = False
    cowlog = open('cow.log', 'a')
    try:
        login = request.GET.get('login')
        pasw = request.GET.get('pasw')
        t = request.GET.get('t')
        h = request.GET.get('h')
        pcname='pcname'

        name = request.GET.get('name')
        co2 = request.GET.get('co2')
        ch4 = request.GET.get('ch4')
        n2o = request.GET.get('n2o')
        mt = "Пояснения "
        data = 't = ' + str(t) + ' h = ' + str(h) + ' CO2 = ' + str(co2) + ' CH4 = ' + str(ch4) + ' n2o = ' + str(n2o)

        #if t > 25:


        if login in password:
            if password[login] == pasw:
                nameandpaswcorrect = True

        if nameandpaswcorrect == True:
                a = 'YES_'
                logging.info('user: ' + login)
                if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                    cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                        'REMOTE_ADDR'] + ' / '  + pcname + ' / ' +
                                data + ' / ' + '\n')
                else:
                    cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                        'HTTP_X_FORWARDED_FOR'] + ' / ' +  pcname + ' / ' +
                                "data" + ' / ' + '\n')
                    # if behind a proxy
        else:
                a = 'Wrong user credentials!_'
                logging.warning('user ' + login + ': Wrong user credentials!')
                if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                    cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                        'REMOTE_ADDR'] + ' / ' + pcname + ' / ' +
                                data + ' / ' + ': Wrong user credentials!' + '\n')
                else:
                    cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                        'HTTP_X_FORWARDED_FOR'] + ' / ' + pcname + ' / ' +
                                data + ' / ' + ': Wrong user credentials!' + '\n')
                    # if behind a proxy

    except ValueError:
            logging.warning('user ' + login + ': Wrong user name_' + '\n')
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                    'REMOTE_ADDR'] + ' / ' + pcname + ' / ' +
                            data + ' / ' + ': Wrong user name!' + '\n')
            else:
                cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                    'HTTP_X_FORWARDED_FOR'] + ' / ' + pcname + ' / ' +
                            data + ' / ' + ': Wrong user name!' + '\n')

    m = Metering(meter_title = name, meter_text = mt, meter_temperature = t, meter_humidity = h, meter_CO2 = co2,
                 meter_CH4 = ch4, meter_N2O = n2o, meter_datetime = now )
    m.save()
    #return render(request, 'ai/add.html', {'metering': m})
    return HttpResponseRedirect(reverse('ai:starter', args = (m.meter_title,)))


def show(request):
    q =  Metering.objects.filter(meter_title ="Mumuka")
    #q = Metering.objects.filter(meter_humidity="13")
    #q = Metering.objects.filter(meter_datetime ="2020-02-25")
    z = {'metter_of_buryonka': q}
    return render(request, 'ai/show.html', z)

def graph1(request):
    try:
        #q =  Metering.objects.get(meter_title ="Mumuka")
        q = Metering.objects.filter(meter_title="Mumuka")
        #Yarushka
    except:
        raise Http404("Нет запрашиваемых данных")

    latest_data_list = q.order_by('-meter_datetime')[:3]
    #p = figure(title="Данные датчиков", x_axis_label='время в кварталах', y_axis_label='вероятность дефолта')
    #x1 =  latest_data_list.meter_datetime
    x1 =[1,2,3]
    #y1 = latest_data_list.Metering.meter_temperature
    y1 = [2, 4, 8]
    #y2 = latest_data_list.meter_humidity
    y2 = [10, 4, 1]
    #p.line(x1, y1, legend_label="y1", line_width=2, color='red')
    #p.line(x1, y2, line_width=2, color='green')
    # grab the static resources
    #js_resources = INLINE.render_js()
    #css_resources = INLINE.render_css()
    #script, div = components(p)
    #html = render(         "graph1.html",p)
    #return encode_utf8(html)
    #return html
    z = {'metter_of_buryonka': latest_data_list}

    return render(request, 'ai/graph1.html', z)

def graph2(request):
    pass

def addcom(request, metering_id):
    latest_comments_list = []
    try:
       q = Metering.objects.filter(id = metering_id)
    except:
       raise Http404("Нет запрашиваемых данных")
       #latest_comments_list = ["Нет запрашиваемых данных"]
       #latest_comments_list = append("Нет запрашиваемых данных")
    #latest_data_list = q.order_by('-meter_datetime')[:4]
    #try:
    #     latest_comments_list = q.note_set.order_by('-id')[:10]
    #except:
    #      raise Http404("Нет комментариев к измерению")

    #return render(request, 'ai/addcom.html', {'metter_of_buryonka': q, 'latest_comments_list': latest_comments_list})
    return render(request, 'ai/form1.html',{'metter_of_buryonka': q, 'latest_comments_list': latest_comments_list, 'name':'name'})


def starter(request, meter_title):
#def starter(request):
   # Acc = account_check(request)
    try:
       #q = Metering.objects.filter(meter_title="Yarushka")
       #q = Metering.objects.filter(meter_title="Mumuka")
       q = Metering.objects.filter(meter_title=meter_title)
        #Yarushka
    except:
       raise Http404("Нет запрашиваемых данных")
    y3 = []

    for data in q:
        y3.append(data.meter_humidity)
    len_all = len(y3)

    latest_data_list = q.order_by('-meter_datetime')[:1000]
    z = {'metter_of_buryonka': latest_data_list}

    #x1 = [1, 10, 35, 27]
    #y1 = [0, -1, -0.5, 0.2]

    #x1 = latest_data_list.meter_datetime
    #y1 = latest_data_list.Metering.meter_temperature
    x0 = []
    y1 = []
    y2 = []
    y4 = []
    #d = []
    #format = '%b %d %Y %I:%M%p' # Формат
    format = '%H:%M' # Формат
    for data in latest_data_list:
        #d=str(datetime.date(data.meter_datetime))
        x0.append(data.meter_datetime)
        y1.append(data.meter_temperature)
        y2.append(data.meter_humidity)
        y4.append(data.meter_CO2)
        #n.append(data.meter_humidity)

    name_cow = data.meter_title
    print(name_cow)


    if name_cow =='Yarushka':
        nabobj_name = 'Объект 1'
        gas_name = 'LPG'
    elif name_cow =='Mumuka':
        nabobj_name = 'Объект 2'
        gas_name = 'CO2'
    elif name_cow =='Buryonka':
        nabobj_name = 'Объект 4'
        gas_name = 'Smoke gas'
    elif name_cow =='Vestka':
        nabobj_name = 'Объект 5'
        gas_name = 'CH4'
    else:
        nabobj_name = 'Объект NoName'
        gas_name = 'UnKnown gas'

    x1 = range(len(y1))
    print(len(y1))
    #for el in x0:
     #   d.append(el)
    #Формируем список с обратной последовательностью
    y10 = y1[::-1]
    y20 = y2[::-1]
    y40 = y4[::-1]
    x10 = x0[::-1]
    #последние элементы списков
    date_last = x10[-1]
    y1_last = y10[-1]
    y2_last = y20[-1]
    y4_last = y40[-1]

    date_first = x10[0]
    y1_first = y10[0]
    y2_first = y20[0]

    # y2 = latest_data_list.meter_humidity
    #plot = figure()
    #plot.circle(x1, y1, size=5, color="blue")
    #plot.circle(x1, y2, size=5, color="red")
    plot = figure(
    plot_width=900,
    tools = "pan, box_zoom, reset, save",
    x_axis_label='номер измерения', y_axis_label='температура, влажность'
    )

    plot.line (x1, y10, legend_label = "температура, С", line_color="red")
    #plot.line(x1, y2, legend="влажность, %", line_color="blue", line_dash="4 4")
    plot.line(x1, y20, legend_label = "влажность, %", line_color="blue")
    plot.line(x1, y40, legend_label = "концентрация, ppm", line_color="green")

    name_dop_osi = 'концентрация ' + gas_name+ ', ppm'
    #script, div = components(plot)
    script, div = components(myplot_2(request, x1, y10, y20, y40, 'температура, °С', 'влажность, %', name_dop_osi))
    #print(div)



    return render(request, 'ai/starter.html', {'script': script, 'div' : div, 'metter_of_buryonka': latest_data_list, 'len_all': len_all,
                                               'date_last': date_last,
                                               'date_first': date_first,
                                               't_last':y1_last,
                                               'h_last':y2_last,
                                               'CO2_last':y4_last,
                                               'data': data,
                                               'nabobj_name' : nabobj_name,
                                                'gas_name': gas_name,
                                               # 'Acc': Acc
                                               })


def leave_comment2(request, metering_id):
    try:
        a = Metering.objects.get(id=metering_id)
    except:
        raise Http404("Статья не найдена!")
    a.note_set.create(author_name = request.POST['name'], comment_text = request.POST['text'])

    return HttpResponseRedirect(reverse('ai:addcom', args = (a.id,)))

#def detal2(request , metering_id):
    #    try:
    #        a = Metering.objects.get(id = metering_id)
    #except:
    #    raise Http404("Статья не найдена!")

    #latest_comments_list = a.note_set.order_by('-id')[:10]

    #return render(request, 'ai/addcom.html', {'metering': a, 'latest_comments_list': latest_comments_list})

def index2(request):
    #latest_metering_list = Metering.objects.order_by('-meter_datetime')[:4]
    latest_metering_list = Metering.objects.all()
    return render(request, 'ai/list2.html', {'latest_metering_list': latest_metering_list})

def nabobj(request):
    cow_metering_list = Metering.objects.all()
    X=[]
    for cow in cow_metering_list:
        X.append(cow.meter_title)
    XM = set(X)
    y = sorted(list(XM))
    return render(request, 'ai/nabobj.html', {'cow_metering_list': y})

def cows(request, meter_title):
    return HttpResponseRedirect(reverse('ai:starter', args=(meter_title,)))

def pdstart(request):
    print('pdstart_qqq')
    X = []
    Y = []
    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated")
        print(request.user.is_authenticated )
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)
        #a = Customer.objects.get(id=request.user.id)

        #m = Customer(phone = '+7(495)7777777',email = "alex@bmail.org", account = 100, user_id = request.user.id)
        #m.save()

        #Cus = Customer.objects.filter(id = request.user.id)
        customer = a.customer_set.order_by('id')[:]

        for cus in customer:
            X.append(cus.account)
            Y.append(cus.bank)

        #print(X)
        #print(Y)

    else:
        print("User.is_not_authenticated")
        print(request.user.is_authenticated )
        X.append("0")
        Y.append(" ")

    if len(X) ==0:
        X.append("0")
    return render(request, 'ai/pdstart.html',{'Acc': X[-1]})




def pdcalc(request):
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler  # Стандартизация данных
    import tensorflow
    #from tensorflow
    import keras
    import joblib
    import keras.backend as K
    from keras.utils.generic_utils import get_custom_objects
    import os.path

    regn = request.POST['name']
    print("regn = ")
    print(regn)

    #import pyodbc
    #import adodbapi

    #database = "MosReg.mdb"
    ##constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=D:\BASE_MDB\MosReg.mdb'
    ##constr = 'Provider=Microsoft.ace.oledb.12.0; Data Source=D:\BASE_MDB\MosReg.mdb'
    #constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s'
    #tablename = "Banks"

    # Подключаемся к базе данных.
    #conn = adodbapi.connect(constr)

    # Создаем курсор.
    #cur = conn.cursor()

    # Получаем все данные.
    #sql = "select * from Banks"
    #sql = "select * from %s" % tablename
    #cur.execute(sql)

    # Показываем результат.
    #result = cur.fetchall()
    #for item in result:
    #   print(item)

    # Завершаем подключение.
    #cur.close()
    #conn.close()

    bank= {
        '1' : 'UniCredit Bank',
        '170':'РН банк',
        '316': 'Home Credit&Finance Bank',
        '354': 'Gazprombank',
        '963': 'Совкомбанк',
        '1000': 'VTB Bank OAO',
        '1326': 'АЛЬФА-БАНК',
        '1481': 'Sberbank',
        '1978': 'МОСКОВСКИЙ КРЕДИТНЫЙ БАНК',
        '2272': 'Rosbank',
        '2268': 'ОАО МТС БАНК',
        '2306': 'Absolut Bank',
        '2748': 'Bank of Moscow',
        '3255': 'Банк ЗЕНИТ ОАО',
        '2210': 'Транскапиталбанк',
        '1920': 'Ланта-Банк',
        '2664': 'АКБ Славия (ЗАО)',
        '1614': 'ЗАУБЕР Банк',
        '436' : 'ОАО Банк Санкт-Петербург',
        '1439': 'Банк «Возрождение» (ОАО)',
        '2766': 'ОТП Банк',
        '3016': 'Нордеа Банк',
        '3328': 'Deutsche Bank',
        '3349': 'Russian Agricultural Bank',
        '1052': 'МТИ-банк',
        '3073': 'РГС банк',
        '3176': 'Балтинвестбанк',
        '1460': 'Восточный банк',
        '2209': 'Открытие',
        '1680': 'Сredit Agricole CIB',
        '2494': 'Credit Suisse',
        '2495': 'ING',
        '2557': 'Citibank',
        '2584': 'Кредит Урал Банк',
        '2629': 'JP Morgan',
        '2790': 'ЗАО РОСЭКСИМБАНК',
        '3292': 'Raiffeizenbank',
        '3311': 'Credit Europe Bank',
        '3333': 'Commerzbank Eurazia',
        '3337': 'ЗАО Мидзухо Корпорэйт Банк (Москва)',
        '3340': 'КБ МСП Банк',
        '3390': 'Натиксис Банк (ЗАО)',
        '3407': 'BNP Paribas',
        '3463': 'Ю Би Эс Банк',
        '3465': 'Эм-Ю-Эф-Джи Банк (Евразия)',
        '3470': 'Тойота Банк',
        '3490': 'Goldman Sachs',
        '2879': 'ОАО АКБ Авангард',
        '2707': 'КБ "ЛОКО-Банк" (ЗАО)',
        '2574': 'Банк РМП (ПАО)',
        '2440': 'Металлинвест',
        '2275': 'Уралсиб',
        '2846': 'Система',
        '2156': 'Нефтепромбанк',
        '2914': 'Арес-банк',
        '3124': 'НС–Банк',
        '2241': 'КИВИ Банк',
        '2929': 'ББР Банк',
        '665' : 'ГТ банк',
        '2590': 'АК БАРС',
        '2546': 'НОВИКОМБАНК',
        '3261': 'ВНЕШПРОМБАНК',
        '2271': 'КРАНБАНК',
        '1776': 'ОАО Банк Петрокоммерц',
        '1557': 'ВУЗ-банк',
        '1751': 'МОСКОВСКИЙ ОБЛАСТНОЙ БАНК',
        '2110': 'Пересвет',
        '2989': 'Фондсервисбанк',
        '2763': 'Инвестторгбанк',
        '2490': 'Генбанк',
        '912' : 'Московский Индустриальный банк',
        '1810': 'Азиатско-Тихоокеанский Банк',
        '3279': 'НБ ТРАСТ',
        '554' : 'Солидарность',
        '1581': 'БТА-Казань(ОАО)',
        '1673': 'Банк Майский',
        '2764': 'ТЭМБР-БАНК',
        '2960': 'Славянский кредит',
        '2222': 'Инвесткомбанк БЭЛКОМ',
        '3379': 'Мааксима',

    }

    Dat1 ={
        '0': '1/07/2010',
        '1': '1/10/2010',
        '2': '1/01/2011',
        '3': '1/04/2011',
        '4': '1/07/2011',
        '5': '1/10/2011',
        '6': '1/01/2012',
        '7': '1/04/2012',
        '8': '1/07/2012',
        '9': '1/10/2012',
        '10': '1/01/2013',
        '11': '1/04/2013',
        '12': '1/07/2013',
        '13': '1/10/2013',
        '14': '1/01/2014',
        '15': '1/04/2014',
        '16': '1/07/2014',
        '17': '1/10/2014',
        '18': '1/01/2015',
        '19': '1/04/2015',
        '20': '1/07/2015',
        '21': '1/10/2015',
        '22': '1/01/2016',
        '23': '1/04/2016',
        '24': '1/07/2016',
        '25': '1/10/2016',
        '26': '1/01/2017',
        '27': '1/04/2017',
        '28': '1/07/2017',
        '29': '1/10/2017',
        '30': '1/01/2018',
        '31': '1/04/2018',
        '32': '1/07/2018',
        '33': '1/10/2018',
        '34': '1/01/2019',
        '35': '1/04/2019',
        '36': '1/07/2019',
        '37': '1/10/2019',
        '38': '1/01/2020',
        '39': '1/04/2020',
        '40': '1/07/2020',
        '41': '1/10/2020',
        '42': '1/01/2021',
    }

    Dat2 = {

        '0': '1/01/2004',
        '1': '1/04/2004',
        '2': '1/07/2004',
        '3': '1/10/2004',
        '4': '1/01/2005',
        '5': '1/04/2005',
        '6': '1/07/2005',
        '7': '1/10/2005',
        '8': '1/01/2006',
        '9': '1/04/2006',
        '10': '1/07/2006',
        '11': '1/10/2006',
        '12': '1/01/2007',
        '13': '1/04/2007',
        '14': '1/07/2007',
        '15': '1/10/2007',
        '16': '1/01/2008',
        '17': '1/04/2008',
        '18': '1/07/2008',
        '19': '1/10/2008',
        '20': '1/01/2009',
        '21': '1/04/2009',
        '22': '1/07/2009',
        '23': '1/10/2009',
        '24': '1/01/2010',
        '25': '1/04/2010',

        '26': '1/07/2010',
        '27': '1/10/2010',
        '28': '1/01/2011',
        '29': '1/04/2011',
        '30': '1/07/2011',
        '31': '1/10/2011',
        '32': '1/01/2012',
        '33': '1/04/2012',
        '34': '1/07/2012',
        '35': '1/10/2012',
        '36': '1/01/2013',
        '37': '1/04/2013',
        '38': '1/07/2013',
        '39': '1/10/2013',
        '40': '1/01/2014',
        '41': '1/04/2014',
        '42': '1/07/2014',
        '43': '1/10/2014',
        '44': '1/01/2015',
        '45': '1/04/2015',
        '46': '1/07/2015',
        '47': '1/10/2015',
        '48': '1/01/2016',
        '49': '1/04/2016',
        '50': '1/07/2016',
        '51': '1/10/2016',
        '52': '1/01/2017',
        '53': '1/04/2017',
        '54': '1/07/2017',
        '55': '1/10/2017',
        '56': '1/01/2018',
        '57': '1/04/2018',
        '58': '1/07/2018',
        '59': '1/10/2018',
        '60': '1/01/2019',
        '61': '1/04/2019',
        '62': '1/07/2019',
        '63': '1/10/2019',
        '64': '1/01/2020',
        '65': '1/04/2020',
        '66': '1/07/2020',
        '67': '1/10/2020',
        '68': '1/01/2021',
        '69': '1/04/2021',
        '70': '1/07/2021',
        '71': '1/10/2021',
        '72': '1/01/2022',

    }

    name = serv(request, str(regn))
    #data = pd.read_csv("Train4-X42-b60-D38B.csv", sep=';')
    #data.describe()
    #y = data['43']
    #X = data.drop('43', axis=1)
    #X = X.apply(pd.to_numeric)
    #scaler = StandardScaler(copy=False).fit(X)
    #X_train = scaler.transform(X)
    #scaler_filename = "scaler_x42a.save"
    #joblib.dump(scaler, scaler_filename)

    #файл для шкалирования (стандартизации) нужно делать в этой процедуре (файл шкалирования из Jupyter Notebook не подходит
    #data = pd.read_csv("Train-XXX+47_D41B.csv", sep=';')
    #X = data
    #cols = ['3', '7', '8', '9', '13', '18', '19', '20', '21', '22', '23', '24', '25', '27', '29', '32', '33', '34',
    #        '38', '39', '40', '41', '42', '43', '44', '45', '46', '48']
    #X.drop(cols, axis=1, inplace=True)
    #X = X.apply(pd.to_numeric)
    #scaler = StandardScaler(copy=False).fit(X)
    #X_train = scaler.transform(X)
    #scaler_filename = "scaler_x20a.save"
    #joblib.dump(scaler, scaler_filename)

    now = timezone.now()
    print('pdcalc')
    X = []
    Y = []
    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated = ", request.user.is_authenticated)
        #print(request.user.is_authenticated)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)

        # Cus = Customer.objects.filter(id = request.user.id)
        customer = a.customer_set.order_by('id')[:]

        for cus in customer:
            X.append(cus.account)
            Y.append(cus.bank)

        #print(X)
        #print(Y)

        #name = bank[regn]

    else:
        print("User.is_not_authenticated")
        print(request.user.is_authenticated)
        X.append("0")
        Y.append(" ")

    if len(X) == 0:
        depositIsNull = True
    else:
        if X[-1] > 0:
            depositIsNull = False
        else:
            depositIsNull = True

    if depositIsNull == True:
        mes = 'Не достаточно средств на текущем счете - пополните депозит'
        return render(request, 'ai/deposit.html', mes = mes)
    else:
        mod = "model_X20_jpt22"
        #if regn in bank:
        #    name = bank[regn]
        #else:
        #    name = 'Название не определено'
        #print(name)


        # Пересоздаем ту же самую модель, включая веса и оптимизатор.
        def mean_pred2(y_true, y_pred):
            a = abs(y_true - y_pred)
            a = 1 - a
            return a

        get_custom_objects().update({"mean_pred": mean_pred2})
        print("mean_pred2...")

        model = keras.models.load_model(mod + '.h5', custom_objects={"mean_pred": mean_pred2})
        print("keras.models.load_model...")
        scaler_filename = "scaler_x20a.save"
        print(scaler_filename)
        scaler = joblib.load(scaler_filename)
        print("scaler = joblib.load...")
        txt = regn
        print("txt =")
        print(txt)
        #wayf='D:\TEMP2\CSV\X42\Testob-' + str(regn) + 'A42.csv'
        wayf = 'D:\TEMP2\CSV\Testob-' + str(regn) + 'A42.csv'
        check_file = os.path.exists(wayf)
        print(check_file)
        print(wayf)
        if not check_file:
            wayf = 'D:\TEMP2\CSV\Testob-' + str(regn) + 'A51.csv'
            check_file = os.path.exists(wayf)
            print(check_file)
            print(wayf)
            cols = ['3', '7', '8', '9', '13', '18', '19', '20', '21', '22', '23', '24', '25', '27', '29', '32', '33',
                    '34', '38', '39', '40', '41', '42', '43', '44', '45', '46', '48', '49', '50', '51']

            Dat = Dat2
        else:

            cols = ['3', '7', '8', '9', '13', '18', '19', '20', '21', '22', '23', '24', '25', '27', '29', '32', '33',
                    '34', '38', '39', '40', '41', '42', '43', '44', '45', '46']
            Dat = Dat1

        info = 'Ответ сети: Расчет не возможен - отсутствует отчетность банка ' + name + ' (лицензия №' + regn + ')'
        if not check_file:
            return render(request, 'ai/pdstart.html', {'Acc': X[-1], 'info' : info})

        data2 = pd.read_csv(wayf, sep=',')
        X_new1 = data2

        X_new1.drop(cols, axis=1, inplace=True)

        print('data2[:5]=')
        print(data2[:5])

        print('X_new1[1:5]=')
        print(X_new1[1:5])
        print('X_new1.shape[1] = ')
        print(X_new1.shape[1])

        if X_new1.shape[1] != 20:
            return render(request, 'ai/pdstart.html', {'Acc': X[-1], 'info' : info})

        X_new1 = X_new1.apply(pd.to_numeric)
        print('после pd.to_numeric X_new[1:5]=')
        print(X_new1[1:5])



        X_new = scaler.transform(X_new1)
        ChDat = X_new.shape[0]
        print('X_new[1]=')
        print(X_new[1])
        print('len(X_new[1]) = ')
        print(len(X_new[1]))



        # расчет предсказания
        predictions = model.predict(X_new)
        #ChDat = 41
        #ChDat = len(X_new[1])
        #определяем число строк в массиве X_new
        ChDat=X_new.shape[0]

        print("ChDat...")
        x = np.arange(0, ChDat, 1)
        print("x = ", x)

        #y1 = predictions
        tmp = predictions
        k = 0.000757014277148727
        vdd = (-np.log(tmp) / k) / 365

        print(" predictions...")
        # y1 - PD
        # y2 - PD(фильтр)
        # y3 - время до дефолта
        # y4 - время до дефолта(фильтр)
        # y5 - рейтинг(фильтр)
        # y6 - рейтинг прогноз
        # если время до дефолта ниже, чем время до дефолта (фильтр), то прогноз отрицательный
        # если время до дефолта выше, чем время до дефолта (фильтр), то прогноз положительный
        # если время до дефолта не сильно (не более 3 лет) отличается от время до дефолта (фильтр), то прогноз стабильный

        y1 = tmp.ravel()
        i = 0
        y3 = vdd.ravel()
        y2 = []
        y4 = []
        while i <= ChDat - 1:
            if i == 0:
                y2.append(y1[i])
                y4.append(y3[i])
            elif i == 1:
                y2.append((y1[i] + y1[i - 1]) / 2)
                y4.append((y3[i] + y3[i - 1]) / 2)
            elif i == 2:
                y2.append((y1[i] + y1[i - 1] + y1[i - 2]) / 3)
                y4.append((y3[i] + y3[i - 1] + y3[i - 2]) / 3)
            elif i == 3:
                y2.append((y1[i] + y1[i - 1] + y1[i - 2] + y1[i - 3]) / 4)
                y4.append((y3[i] + y3[i - 1] + y3[i - 2] + y3[i - 3]) / 4)
            else:
                y2.append((y1[i] + y1[i - 1] + y1[i - 2] + y1[i - 3] + y1[i - 4]) / 5)
                y4.append((y3[i] + y3[i - 1] + y3[i - 2] + y3[i - 3] + y3[i - 4]) / 5)
            # print(y2[i])
            i = i + 1

        i = 0
        y5 = []
        y6 = []
        while i <= ChDat - 1:
            if y4[i] >= 26:
                y5.append('AAA')
            elif y4[i] >= 25:
                y5.append('AAA-')
            elif y4[i] >= 24:
                y5.append('AA+')
            elif y4[i] >= 23:
                y5.append('AA')
            elif y4[i] >= 22:
                y5.append('AA-')
            elif y4[i] >= 21:
                y5.append('A+')
            elif y4[i] >= 20:
                y5.append('A')
            elif y4[i] >= 19:
                y5.append('A-')
            elif y4[i] >= 18:
                y5.append('BBB+')
            elif y4[i] >= 17:
                y5.append('BBB')
            elif y4[i] >= 16:
                y5.append('BBB-')
            elif y4[i] >= 15:
                y5.append('BB+')
            elif y4[i] >= 14:
                y5.append('BB')
            elif y4[i] >= 13:
                y5.append('BB-')
            elif y4[i] >= 12:
                y5.append('B+')
            elif y4[i] >= 11:
                y5.append('B')
            elif y4[i] >= 10:
                y5.append('B-')
            elif y4[i] >= 9:
                y5.append('CCC+')
            elif y4[i] >= 8:
                y5.append('CCC')
            elif y4[i] >= 7:
                y5.append('CCC-')
            elif y4[i] >= 6:
                y5.append('CC+')
            elif y4[i] >= 5:
                y5.append('CC')
            elif y4[i] >= 4:
                y5.append('CC-')
            elif y4[i] >= 3:
                y5.append('C+')
            elif y4[i] >= 2:
                y5.append('C')
            elif y4[i] >= 1:
                y5.append('C-')
            elif y4[i] >= 0:
                y5.append('D')
            else:
                y5.append('D')
            if y3[i] - y4[i] > 2:
                y6.append('положительный')
            if y3[i] - y4[i] < -2:
                y6.append('отрицательный')
            if abs(y3[i] - y4[i]) <=2:
                y6.append('стабильный')
            i = i + 1


        # уточнить критерий успешно произведенного расчета if i > 0:
        if i > 0:
            XX = X[-1]
            XX = XX - 1
            X[-1] = XX
            m = Customer(phone='+7(495)7777777', bank = name, account = XX, user_id=request.user.id, datetime=now)
            m.save()

        #y3 = []
        #y3.append(x[::-1])
        #y3.append(y1[::-1])
        #y3.append(y2[::-1])
        # Формируем список с обратной последовательностью
        y22 = y2[::-1]

        #расчетные данные data2 из csv - файла
        #cols = ['3', '7', '8', '9', '13', '18', '19', '20', '21', '22', '23', '24', '25', '27', '29', '32', '33', '34',
        #        '38', '39', '40', '41', '42', '43', '44', '45', '46']
        #data2 = data2.apply(pd.to_numeric)
        #print('data2 =')
        #print(data2)
        z1 = data2['1']
        z2 = data2['2']
        z4 = data2['4']
        z5 = data2['5']
        z6 = data2['6']
        z10 = data2['10']
        z11 = data2['11']
        z12 = data2['12']
        z14 = data2['14']
        z15 = data2['15']
        z16 = data2['16']
        z17 = data2['17']

        z26 = data2['26']
        z28 = data2['28']
        z30 = data2['30']
        z31 = data2['31']
        print('z31=')
        print(z31)
        z35 = data2['35']
        z36 = data2['36']
        z37 = data2['37']
        z47 = data2['47']


        print('len(x) = ', len(x))
        tab = []
        tab2 = []
        otchetnost_full = []
        for i in range (len(x)):
            #print('i =', i )
            #print('Dat =', Dat[str(i)])
            y1[i] = toFixed(y1[i], 10)
            y2[i] = toFixed(y2[i], 10)
            y4[i] = toFixed(y4[i], 1)
            z1[i] = float(toFixed(data2['1'][i],5)) #уровень просроченных процентов
            z2[i] = float(toFixed(data2['2'][i], 5)) #Общая срочная КА
            z4[i] = float(toFixed(data2['4'][i], 5)) #уровень риска активов
            z5[i] = float(toFixed(data2['5'][i], 5)) #уровень риска капитала
            z6[i] = float(toFixed(data2['6'][i], 5)) #время оборачиваемости кп
            z10[i] = float(toFixed(data2['10'][i], 5))#ЛАМ / Активы
            z11[i] = float(toFixed(data2['11'][i], 5)) #Прибыль / Активы
            z12[i] = float(toFixed(data2['12'][i], 5)) #Прибыль / Капитал
            z14[i] = float(toFixed(data2['14'][i], 5)) #Коэфф. замещения
            z15[i] = float(toFixed(data2['15'][i], 5)) #E_int
            z16[i] = float(toFixed(data2['16'][i], 5)) #H12
            z17[i] = float(toFixed(data2['17'][i], 5)) #E_pr / E_int

            z26[i] = float(toFixed(z26[i], 5))  # Норматив H7
            z28[i] = float(toFixed(z28[i], 5))  # Норматив H10_1
            z30[i] = float(toFixed(z30[i], 5))  #Средства граждан / активы
            z31[i] = float(toFixed(z31[i], 5)) #Доля активов в системе
            z35[i] = float(toFixed(z35[i], 5)) #фактор V1
            z36[i] = float(toFixed(z36[i], 5))  #фактор V2
            z37[i] = float(toFixed(z37[i], 5))  #фактор V3
            z47[i] = float(toFixed(z47[i], 5))  #доля МБК в активах

            if (z12[i] == 0 and z5[i] == 5) or (z2[i] == 0 and z4[i] == 0):

                otchetnost_full.append('false')
                print('otchetnost_full = false')
            else:
                otchetnost_full.append('true')

            print('z14 =')
            print(z14[i])

            # x-номер квартала
            row = [x[i], y1[i], y2[i], Dat[str(i)], y5[i], y6[i], y4[i],otchetnost_full[i]]
            tab.append(row)
            row = [
                    x[i], Dat[str(i)], z1[i], z2[i], z4[i], z5[i], z6[i], z10[i], z11[i], z12[i], z14[i], z15[i], z16[i], z17[i],
                    z26[i], z28[i], z30[i], z31[i], z35[i], z36[i], z37[i], z47[i]
                   ]
            tab2.append(row)


        pokaz = [
            '№ квартал',
            'Дата',
            'Уровень просроч. процентов',
            'Общая срочная кредитная активность',
            'Уровень риска активов',
            'Уровень риска капитала',
            'Время оборач. кред. портфеля',
            'ЛАМ/Активы',
            'Прибыль/Активы',
            'Прибыль/Капитал',
            'Коэфф. замещения',
            'Интегральная доходность, E_int ',
            'Норматив H12',
            'Относит. себест. E_pr/E_int',
            'Норматив H7',
            'Норматив H10_1',
            'Средства граждан / активы',
            'Доля активов в системе',
            'фактор V1',
            'фактор V2',
            'фактор V3',
            'доля МБК в активах',
        ]

        pokaz_shrot = [
            '№ квартал',
            'Дата',
            'Уровень просроч. проц.',
            'Общ. срочная кредит. активн.',
            'Уровень риска активов',
            'Уровень риска капитала',
            'Время оборач. кред. портфеля',
            'ЛАМ/Активы',
            'Прибыль/Активы',
            'Прибыль/Капитал',
            'Коэфф. замещения',
            'Интегр. доход-ть, E_int ',
            'Норматив H12',
            'Отн. себест. E_pr/E_int',
            'Норматив H7',
            'Норматив H10_1',
            'Ср-ва граждан / активы',
            'Доля активов в системе',
            'фактор V1',
            'фактор V2',
            'фактор V3',
            'доля МБК в активах',

        ]

        plot = figure(
            title = 'Вероятность дефолта банка '+ name,
            plot_width=900,
            tools="pan, box_zoom, reset, save",
            x_axis_label='номер квартала начиная с 1/07/2010', y_axis_label='Вероятность дефолта'
        )
        plot.line(x, y1, legend_label="вероятность дефолта", line_color="red")
        plot.line(x, y2, legend_label="вероятность дефолта фильтр", line_color="blue")
        script, div = components(plot)
        #-----------------график 2-----------------------------------------------------------------------------

        script2, div2 = components(myplot(request, x, y1, z14, pokaz[10], name))
        script3, div3 = components(myplot(request, x, y1, z15, pokaz[11], name))

        script4, div4 = components(myplot(request, x, y1, z1, pokaz[2], name))
        script5, div5 = components(myplot(request, x, y1, z2, pokaz[3], name))
        script6, div6 = components(myplot(request, x, y1, z4, pokaz[4], name))
        script7, div7 = components(myplot(request, x, y1, z5, pokaz[5], name))
        script8, div8 = components(myplot(request, x, y1, z6, pokaz[6], name))
        script9, div9 = components(myplot(request, x, y1, z10, pokaz[7], name))
        script10, div10 = components(myplot(request, x, y1, z11, pokaz[8], name))
        script11, div11 = components(myplot(request, x, y1, z12, pokaz[9], name))
        script12, div12 = components(myplot(request, x, y1, z16, pokaz[12], name))
        script13, div13 = components(myplot(request, x, y1, z17, pokaz[13], name))
        script14, div14 = components(myplot(request, x, y1, z26, pokaz[14], name))
        script15, div15 = components(myplot(request, x, y1, z28, pokaz[15], name))
        script16, div16 = components(myplot(request, x, y1, z30, pokaz[16], name))
        script17, div17 = components(myplot(request, x, y1, z31, pokaz[17], name))
        script18, div18 = components(myplot(request, x, y1, z35, pokaz[18], name))
        script19, div19 = components(myplot(request, x, y1, z36, pokaz[19], name))
        script20, div20 = components(myplot(request, x, y1, z37, pokaz[20], name))
        script21, div21 = components(myplot(request, x, y1, z47, pokaz[21], name))


        return render(request, 'ai/pdcalc.html', {'b_regn' : regn, 'b_name': name, 'x': x,
                                              'y1' : y1, 'y2':y2, 'y3': y3, 'y22': y22, 'Acc': X[-1], 'tab':tab, 'dat': Dat,
                                               'tab2':tab2, 'pokaz':pokaz, 'pokaz_shrot':pokaz_shrot,
                                                'script': script, 'div': div,
                                                'script2': script2, 'div2' : div2,
                                                'script3': script3, 'div3': div3,
                                                'script4': script4, 'div4': div4,
                                                'script5': script5, 'div5': div5,
                                                'script6': script6, 'div6': div6,
                                                'script7': script7, 'div7': div7,
                                                'script8': script8, 'div8': div8,
                                                'script9': script9, 'div9': div9,
                                                  'script10': script10, 'div10': div10,
                                                  'script11': script11, 'div11': div11,
                                                  'script12': script12, 'div12': div12,
                                                  'script13': script13, 'div13': div13,
                                                  'script14': script14, 'div14': div14,
                                                  'script15': script15, 'div15': div15,
                                                  'script16': script16, 'div16': div16,
                                                  'script17': script17, 'div17': div17,
                                                  'script18': script18, 'div18': div18,
                                                  'script19': script19, 'div19': div19,
                                                  'script20': script20, 'div20': div20,
                                                  'script21': script21, 'div21': div21,

                                                  })
def myplot(request, x, y1, y2, name_y2, b_name):
        y2 = y2.ravel()
        plot = figure(
            title='Вероятность дефолта банка и '+name_y2 + ' банка ' + b_name,
            plot_width=1100,
            tools="pan, box_zoom, reset, save",
            x_axis_label='номер квартала начиная с 1/07/2010', y_axis_label='Вероятность дефолта'
        )
        plot.y_range = Range1d(start=0 - max(y1) * 0.1, end=max(y1) * 1.1)
        print('y2 = ')
        print(y2)
        if min(y2) < 0:
            plot.extra_y_ranges['temp'] = Range1d(start=min(y2) + min(y2) * 0.1, end=max(y2) - 0.1*min(y2))
        elif min(y2) == max(y2) == 0:
            plot.extra_y_ranges['temp'] = Range1d(start= -0.1, end=0.1)
        else:
            plot.extra_y_ranges['temp'] = Range1d(start= (min(y2)- max(y2) * 0.1), end = (max(y2)*1.1))

        plot.add_layout(LinearAxis(y_range_name='temp', axis_label=name_y2), 'right')

        plot.line(x, y1, legend_label="вероятность дефолта", line_color="red")
        plot.line(x, y2, legend_label=name_y2, line_color="blue", y_range_name='temp')
        #script2, div2 = components(plot)
        return plot


def myplot_2(request, x, y1, y2, y4, name_y1, name_y2, name_y4):
    plot = figure(
        title='Данные телеметрии: ' + name_y1 + ', ' + name_y2 + ', ' + name_y4,
        plot_width=900,
        tools="pan, box_zoom, reset, save",
        x_axis_label='номер изменения в выборке',
        y_axis_label='температура, С° | влажность, %'
    )

    #print('y2 = ')
    #print(y2)
    y1_min = min(y1)
    y2_min = min(y2)
    y1_max = max(y1)
    y2_max = max(y2)
    if y1_min < y2_min:
        y_min = y1_min
    else:
        y_min = y2_min

    if y1_max > y2_max:
        y_max = y1_max
    else:
        y_max = y2_max

    if min(y1) < 0:
        plot.y_range = Range1d(start=y_min + y_min * 0.1, end=y_max  - 0.1 * y_min)
    elif y_min == y_max == 0:
        plot.y_range = Range1d(start=-0.1, end=0.1)
    else:
        plot.y_range = Range1d(start = (y_min - y_max * 0.1), end = (y_max * 1.1))

    plot.extra_y_ranges['CO2'] = Range1d(start=min(y4) * 0.9, end=max(y4) * 1.1)

    plot.add_layout(LinearAxis(y_range_name='CO2', axis_label = name_y4), 'right')

    plot.line(x, y1, legend_label = name_y1, line_color="red")
    plot.line(x, y2, legend_label = name_y2, line_color="blue")
    plot.line(x, y4, legend_label = name_y4, line_color="green", y_range_name='CO2')
    # script2, div2 = components(plot)
    return plot


# удаление из БД
#  Metering.objects.filter(meter_datetime__day=21).delete()

class MyprojectLoginView(LoginView):
        template_name = 'ai/login.html'
        formclass = AuthUserForm
        success_url = reverse_lazy('ai:start')
        def get_success_url(self):
            return self.success_url


class RegisterUserView(CreateView):
        model = User
        template_name = 'ai/register_page.html'
        form_class = RegisterUserForm
        #success_url = reverse_lazy('ai:recstart_page')
        #success_url = reverse_lazy('ai:nabobj')
        success_url = reverse_lazy('ai:codegen_emailsend_page')
        success_msg = "Пользователь успешно зарегистрирован"

        def form_valid(self, form):
            form_valid = super().form_valid(form)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            aut_user = authenticate(username = username, password = password )
            login(self.request, aut_user)
            return form_valid

class MyprojectLogout(LogoutView):
    next_page = reverse_lazy('ai:start')


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def upDateAcc(request):
    print("upDateAcc")
    acc = account_check(request)
    howmatch = int(acc) + int(request.POST['name'])
    now = timezone.now()
    m = Customer(phone='+7(495)7777777', bank="пополнение баланса", account=howmatch, user_id=request.user.id, datetime=now)
    m.save()
    acc = account_check(request)
    return render(request, 'ai/pdstart.html', {'Acc': acc})

def rascheti(request):

    import os
    import sqlite3
    import urllib  # URL functions
    from time import strftime

    bd = 'D:\WORK\Python\django-learn\mydjango\db.sqlite3'
    now = timezone.now()
    f = open('D:/TEMP3/tudent.txt', 'a')
    f.write('Отчет о действиях клиента ' + request.user.first_name +' '+ request.user.last_name +'\n')
    f.write('Дата и время формирования отчета: ' + str(now) + '\n')


    tdate = strftime("%d-%m")

    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    loc_stmt = 'SELECT account, bank, datetime, user_id from ai_customer WHERE user_id =' + str(request.user.id)
    cursor.execute(loc_stmt)
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        account = row[0]
        bank = row[1]
        datetime = row[2]
        user_id = row[3]
        f.write('user_id ='+ str(user_id) + ' счет: ' + str(account) + ' действие: ' + bank + ' on ' + datetime + '\n')


    #return render(request, 'ai/start.html', {'Acc': X[-1]})
    return render(request, 'ai/start.html')

def rascheti2(request):
    print("rascheti2")

    now = timezone.now()

    f = open('D:/TEMP3/tudent.txt', 'a')
    f.write('Отчет о действиях клиента ' + request.user.first_name + ' ' + request.user.last_name + '\n')
    f.write('Дата и время формирования отчета: ' + str(now) + '\n')

    X = []
    X.append("0")
    bank = []
    datetime = []
    user_id = []

    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated = ", request.user.is_authenticated)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)

        customer = a.customer_set.order_by('id')[:]
        tab = []
        for cus in customer:
            X.append(cus.account)
            bank.append(cus.bank)
            datetime.append(cus.datetime)
            user_id.append(cus.user_id)
            row = [cus.user_id, cus.bank, cus.account, cus.datetime]
            tab.append(row)
            f.write('user_id =' + str(cus.user_id) + ' счет: ' + str(cus.account) + ' действие: ' + cus.bank + ' on ' + str(cus.datetime) + '\n')
    f.close()
    if len(X) ==0:
        X.append("0")
    return render(request, 'ai/rascheti.html', {'Acc': X[-1], 'bank' : bank,'datetime':datetime,'user_id':user_id, 'tab': tab,
                                                'len_X': len(X), 'now' : now, 'first_name': request.user.first_name,
                                                'last_name': request.user.last_name})


def sendSMS(request):
    print('sendSMS begin')
    import urllib  # URL functions
    from time import strftime
    import urllib.request  # URL functions
    from urllib.parse import urlencode

    f = open('D:/TEMP3/sms.txt', 'a')
    tdate = strftime("%d-%m")

    sname =  'Igor'
    snumber = '+79037835429'
    message = (
                sname + ' There will be NO training tonight on the ' + tdate + ' Sorry for the late notice, I have sent a mail as well, just trying to reach everyone, please do not reply to this message as this is automated')

    username = 'YOUR_USERNAME'
    sender = 'WHO_IS_SENDING_THE_MAIL'
    hash = 'YOUR HASH YOU GET FROM YOUR ACCOUNT'

    numbers = (snumber)
    print('numbers = '+numbers)
    # Set flag to 1 to simulate sending, this saves your credits while you are testing your code. # To send real message set this flag to 0
    test_flag = 1

    # -----------------------------------
    # No need to edit anything below this line
    # -----------------------------------

    values = {'test': test_flag,
              'uname': username,
              'hash': hash,
              'message': message,
              'from': sender,
              'selectednums': numbers}

    url = 'http://www.txtlocal.com/sendsmspost.php'
    print('values = ')
    print( values)
    postdata = urlencode(values)
    print("postdata = ")
    print(postdata)
    #req = urllib.request.Request(url, postdata)
    #req = urllib.request.Request(url, postdata)
    req = url + postdata
    print('req = ')
    print(req)
    print('Attempting to send SMS to ' + sname + ' at ' + snumber + ' on ' + tdate)
    f.write('Attempting to send SMS to ' + sname + ' at ' + snumber + ' on ' + tdate + '\n')

    try:
        response = urllib.request.urlopen(req)
        response_url = response.geturl()
        if response_url == url:
            print('SMS sent!')
            sms_sux = 'SMS sent!'
            return render(request, 'ai/sms.html', {'response_url': response_url, "sms_sux": sms_sux})
    except urllib.request.URLError as e:
        print('Send failed!')
        print(e.reason)
        e_reason = e.reason
        sms_sux = 'Send failed!'

        return render(request, 'ai/sms.html',{'e_reason':e_reason, "sms_sux":sms_sux})

def offerta(request):
    return render(request, 'ai/offerta.html')

def fillrec(request):

    msg = ''
    un = user_name(request)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), un + '_tuden.txt')
    f = open(path, 'r')
    codeword_2 = f.read()
    f.close()

    #codeword_2 = 'c3be4580-0774-407d-b3fe-4f3ffd97c7b8'
    client_name = request.POST.get('client_name')
    client_name_full = request.POST.get('client_name_full')
    adres = request.POST.get('adres')

    inn = request.POST.get('inn')
    kpp = request.POST.get('kpp')
    ogrn = request.POST.get('ogrn')
    country = request.POST.get('country')
    codeword = request.POST.get('codeword')
    ul_fl = request.POST.get('ul_fl')
    print('ul_fl =')
    print(ul_fl)
    print('codeword_2 =')
    print(codeword_2)
    print('codeword =')
    print(codeword)

    now = timezone.now()
    #if len(inn) == 0:
        #inn = 'ИНН'

    if ul_fl == 'true':
        vid = 1
    else:
        vid = 0

    if ul_fl == 'true':

        mist_fild = []
        if len(client_name) == 0:
            mist_fild.append('true')
            msg += ' введите название организации /'
        else:
            mist_fild.append('false')

        if len(client_name_full) == 0:
            mist_fild.append('true')
            msg += ' введите полное название организации /'
        else:
            mist_fild.append('false')

        if len(adres) == 0:
            mist_fild.append('true')
            msg += ' введите адрес регистрации /'
        else:
            mist_fild.append('false')

        if len(inn) != 10 and len(inn) != 12:
            msg += ' введите ИНН организации /'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        if len(kpp) != 9:
            msg += ' введите КПП /'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        if len(ogrn) != 13 and len(ogrn) != 15:
            msg += ' введите ОГРН/ОГРНИП /'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        if len(country) == 0:
            mist_fild.append('true')
            msg += ' введите адрес регистрации /'
        else:
            mist_fild.append('false')

        if codeword != codeword_2:
            msg += ' введите кодовое слово'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        reg_fault = 'false'
        for i in mist_fild:
            if i == 'true':
                reg_fault = 'true'

        if reg_fault == 'true':
            msg_1 = 'Регистрация не завершена: '
            msg = msg_1 + msg
            return render(request, 'ai/recvizits.html', {'msg': msg, 'inn_2': inn, 'adres_2': adres,
                                                         'client_name_2': client_name,
                                                         'client_name_full_2': client_name_full,
                                                         'country_2': country, 'kpp_2': kpp,
                                                         'ogrn_2': ogrn, 'comment_2': codeword, 'vid_2': vid})
        else:
            msg_1 = 'Проверка введенных данных выполнена. '
            msg = msg_1 + msg


    else:
        if codeword != codeword_2:
            msg = 'Регистрация не завершена '
            msg += 'введите кодовое слово'
            return render(request, 'ai/recvizits.html', {'msg': msg, 'inn_2': inn, 'adres_2': adres,
                                                         'client_name_2': client_name,
                                                         'client_name_full_2': client_name_full,
                                                         'country_2': country, 'kpp_2': kpp,
                                                         'ogrn_2': ogrn, 'comment_2': codeword, 'vid_2': vid})

    m = Customerrec(client_name = client_name, adres = adres , inn=inn, user_id=request.user.id,
                    client_name_full = client_name_full, country =country, kpp = kpp, ogrn = ogrn,
                    comment = codeword, vid = vid, datetime = now)
    m.save()
    msg += 'Реквизиты занесены в базу данных.'

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), un + '_tuden.txt')
    os.remove(path)

    return render(request, 'ai/message.html',{'msg': msg})

def recstart(request):
    return render(request, 'ai/recvizits.html')

def recstart2(request):
    return render(request, 'ai/recvizits2.html')

def deposit(request):
    print("deposit")
    acc = account_check(request)
    mes = ''
    return render(request, 'ai/deposit.html',{'Acc': acc, 'mes' : mes})

#def account_check(request):
    #    X = []
    #try:
    #   a = User.objects.get(id=request.user.id)
    #except:
    #    raise Http404("Пользователь отсутствует")
    #print("User.is_authenticated = ", request.user.is_authenticated)
    #print(request.user.id)
    #print(request.user.first_name)
    #print(request.user.last_name)
    #print(request.user.id)
    #customer = a.customer_set.order_by('id')[:]

    #for cus in customer:
    #    X.append(cus.account)

    #if len(X) ==0:
    #   X.append("0")

    #return (X[-1])

def serv_mdb(request):

     import adodbapi
     # import win32com

     database = 'D:/BASE_MDB/MosReg.mdb'

     #constr = 'provider=SQLOLEDB.1; Data Source=D:\BASE_MDB\MosReg.mdb'
     #constr = 'Provider=Microsoft.ace.oledb.12.0; Data Source=D:\BASE_MDB\MosReg.mdb'
     #constr = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb); DBQ = D:\BASE_MDB\MosReg.mdb')
     #constr = 'Provider=Microsoft.ace.oledb.12.0; Data Source=D:\BASE_MDB\MosReg.mdb'
     #constr = 'FILEDSN=' + 'D:\BASE_MDB\MosReg.mdb'
     #constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s'
     constr = 'Provider=Microsoft.ace.oledb.12.0; Data Source=D:/BASE_MDB/MosReg.mdb'

     #constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s' % database
     tablename = "Banks"

     # Подключаемся к базе данных.
     conn = adodbapi.connect(constr)
     #conn = pyodbc.connect(constr)
     #conn = mdb_connect(database)  # only absolute paths!
     # Создаем курсор.
     cur = conn.cursor()
    # Получаем все данные.
     sql = "select * from %s" % tablename
     # sql = "select * from %s" % tablename
     cur.execute(sql)

    # Показываем результат.
     result = cur.fetchall()
     for item in result:
        print(item)

        # Завершаем подключение.
     cur.close()
     conn.close()

     msg = 'данные из базы MDB получены'



     return render(request, 'ai/message.html', {'msg': msg})


def mdb_connect(db_file, user='admin', password='', old_driver=False):
         driver_ver = '*.mdb'
         if not old_driver:
             driver_ver += ', *.accdb'

         odbc_conn_str = ('DRIVER={Microsoft Access Driver (%s)}'
                          ';DBQ=%s;UID=%s;PWD=%s' %
                          (driver_ver, db_file, user, password))

         return pyodbc.connect(odbc_conn_str)

def serv(request, zapros):
    import pandas as pd

    print('zapros =')
    print(zapros)
    data = pd.read_csv("Banks2.csv", sep=';')
    regn = data['Regn']
    regnstr = []
    for r in regn:
        regnstr.append(str(r))
    bname = data['Name']
    banks = dict(zip(regnstr, bname))
    #print('banks = ')
    #print(banks)
    if zapros in banks:
        otvet = banks[zapros]
    else:
        otvet = 'NoName'

    msg = 'данные из файла csv получены'

    #return render(request, 'ai/message.html', {'msg': msg, 'regn':regn,'bname':bname,'banks':banks})
    return otvet





def mail(request):
    return render(request, 'ai/mail.html')


def success(request):
    email = request.POST.get('name', '')
    print('email=')
    print(email)
    data =    """
    Hello there!

    I wanted to personally write an email in order to welcome you to our platform.\
    We have worked day and night to ensure that you get the best service. I hope \
    that you will continue to use our service. We send out a newsletter once a \
    week. Make sure that you read it. It is usually very informative.
    
    Cheers!
    ~ Yasoob
    """
    print('data =')
    print(data)

    send_mail('Welcome!', data, "Yasoob",
              [email], fail_silently=False)
    msg = 'Сообщение отправлено по e-mail'

    return render(request, 'ai/success.html',{'msg':msg})


def send_codeword(request, codeword):
        email = user_email(request)
        print('email=')
        print(email)
        data = """
        Добрый день!
        
        Вы находитесь в процессе регистрации на сайте amelin-aga.com. Для завершения регистрации Вам понадобится следующее кодовое слово 
        """
        data += codeword

        data2 = """
        
        С уважением,
        Аналитическая группа Амелина 
                """
        data += data2

        print('data =')
        print(data)

        if email != 'no email':
                send_mail('Welcome!', data, "Yasoob",
                          [email], fail_silently=False)
        return email

def user_email(request):
    #по user.id получаем email из связанной с моделью Uesr БД Customerrec
    X = []
    try:
        a = User.objects.get(id=request.user.id)
    except:
        raise Http404("Пользователь отсутствует")
    print("User.is_authenticated = ", request.user.is_authenticated)
    print(request.user.id)
    print(request.user.first_name)
    print(request.user.last_name)
    print(request.user.id)
    #customer = a.customer_set.order_by('id')[:]

    #for cus in customer:
    X.append(a.email)

    print('a.email = ')
    print(a.email)

    if len(a.email) == 0:
        resp = 'no email'
    else:
        resp = a.email

    return resp

def codegen_emailsend(request):

    #codeword_2 = str(secrets.token_bytes(16))
    codeword_2 = str(uuid.uuid4())
    email = send_codeword(request, codeword_2)
    un = user_name(request)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), un + '_tuden.txt')
    f = open(path, 'a')
    f.write(codeword_2)
    f.close()


    if email == 'no email':
        msg = ' отсутствует email - нет возможности отправить Вам кодовое слово /'
    else:
        msg = ' Произведена отправка Вам кодового слова, необходимого для регистрации в системе /'


    return render(request, 'ai/recvizits.html')

def user_name(request):
    # по user.id получаем итя клиента (login) из модели Uesr
    try:
        a = User.objects.get(id=request.user.id)
    except:
        raise Http404("Пользователь отсутствует")

    print('a.username = ')
    print(a.username)

    if len(a.username) == 0:
        resp = 'no Name'
    else:
        resp = a.username

    return resp

#-------------CHANGE PASSWORD--------------------------
class MyPasswordChangeView(PasswordChangeView):
    template_name = 'ai/password_change_form.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:password_change_done')

    def get_success_url(self):
        return self.success_url


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'ai/password_change_done.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url

#-------------RESET PASSWORD--------------------------
class MyPasswordResetView(PasswordResetView):
    template_name = 'ai/password_reset_form.html'
    email_template_name = 'ai/password_reset_email.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:password_reset_done')

    def get_success_url(self):
        return self.success_url


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'ai/password_reset_done.html'

    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url


class MyPasswordResetConfirmView(PasswordResetConfirmView):
        template_name = 'ai/password_reset_confirm.html'
        # formclass = AuthUserForm
        success_url = reverse_lazy('ai:password_reset_complete')

        def get_success_url(self):
            return self.success_url


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'ai/password_reset_complete.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url

def remotecontrol(request):
    pass