#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from previews.models import Preview
from aksvrnru.views import error
from utils.views import get_context
from aksvrnru.utils import *
from aksvrnru.views import *
import threading

def upload_zip(request):
    if request.user.is_authenticated() and request.user.is_staff :
        return render_to_response("previews/upload_zip.html", {}, get_context(request))
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить zip!")

def do_upload_zip(request):
    if request.user.is_authenticated() and request.user.is_staff :
        f = request.FILES['previews_zip']

        tmpname = get_tempfile()

        with open(tmpname, 'w') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        Preview.uploadFromZip(tmpname)

        #threading.Thread(target=proc, args=(price))        

        return message(request, u"В обработке!", u"Обработка zip ожидает своей очереди!")
    else:
        return error(request, u"Ошибка доступа", u"Только персонал может загрузить и распарсить zip!")
