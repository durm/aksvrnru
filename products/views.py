#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response
from products.models import Rubric
from pages.views import get_context
from django.contrib.auth import authenticate
from aksvrnru.views import error
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

def rubrics_hierarchy(request):
    rubrics = Rubric.objects.filter(parent__isnull=True)
    return render_to_response('hierarchy/hierarchy.html', {"rubrics":rubrics}, get_context(request))

def login_page(request):
    if request.user.is_authenticated() :
        return error(request, "Ошибка", "Пользователь авторизован как %s." % str(request.user.username))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response("pages/login_page.html", c)

def login_proc(request):
    user = authenticate(username=request.POST.get("login"), password=request.POST.get("passwd"))
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(reverse('me'))
        else:
            return error(request, "Ошибка авторизации", "Учетная запись не активна.")
    else:
        return error(request, "Ошибка авторизации", "Неверные логин или пароль.")

def me(request):
    if request.user.is_authenticated() :
        return render_to_response("pages/me.html", get_context(request))
    else:
        return redirect(reverse('login_page'))
        