#-*- coding: utf-8 -*-

from django.contrib import admin
from rubrics.models import Rubric
from django import forms

class RubricForm(forms.ModelForm):

    class Meta:
        model = Rubric
        exclude = ['created_by', 'updated_by','created_at', 'updated_at']

class RubricAdmin(admin.ModelAdmin):
    list_filter = ('is_published', 'skip')
    form = RubricForm

admin.site.register(Rubric, RubricAdmin)
