 #-*- cdoing: utf-8 -*-

from django.shortcuts import redirect, render_to_response

def error(request, title, content):
    return render_to_response("base/error.html", {'title':title, 'content':content})
