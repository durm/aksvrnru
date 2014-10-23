#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from pricelog.models import Price
from aksvrnru.views import error
from utils.views import get_context
from aksvrnru.utils import *
from aksvrnru.views import *
from pricelog.tasks import proc
import threading

def upload_price(request):
    if request.user.is_authenticated() and request.user.is_staff :
        return render_to_response("pricelog/upload_price.html", {}, get_context(request))
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить прайс!")

def do_upload_price(request):
    if request.user.is_authenticated() and request.user.is_staff :
        f = request.FILES['price']

        tmpname = get_tempfile()

        with open(tmpname, 'w') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        price = Price(name=tmpname, result="process")
        price.save()

        proc(price)

        #threading.Thread(target=proc, args=(price))        

        return message(request, u"В обработке!", u"Обработка прайса ожидает своей очереди!")
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить прайс!")

   
