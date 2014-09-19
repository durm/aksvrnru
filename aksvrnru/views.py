 #-*- cdoing: utf-8 -*-

from django.shortcuts import redirect, render_to_response

def message(request, title, content):
    return render_to_response("base/message.html", {'title':title, 'content':content})

def error(request, title, content):
    return message(request, title, content)