#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from pricelog.models import Price
from aksvrnru.views import error
from utils.views import get_context

def upload_price(request):
    if not request.user.is_superuser :
        return error(
            request, 
            u"Ошибка", 
            u"Только суперпользователь может распарсить прайс"
        )
    else:
        return render_to_response("pricelog/upload_price.html", context_instance = get_context(request))

 def upload_price(request):
    if request.user.is_authenticated() and request.user.is_staff :
        return render_to_response("products/upload_price.html", {}, get_context(request))
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить прайс!")

def do_upload_price(request):
    if request.user.is_authenticated() and request.user.is_staff :
        f = request.FILES['price']
        price = Price.objects.create(name=f.name, file=f)
        price.save()
        
        proc.delay(request.user.id, price.id)
        
        return message(request, u"В обработке!", u"Обработка прайса ожидает своей очереди!")
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить прайс!")

   
