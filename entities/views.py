from django.shortcuts import render
from entities.models import Entity

def upload_entity(request):
    return render("1")

def do_upload_entity(request):
    f = request.FILES['file']
    entity = Entity.objects.create(file=f)
    return render(str(entity))
