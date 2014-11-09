#-*- coding: utf-8 -*-

from django.contrib import admin
from vendors.models import Vendor
from django import forms

class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        exclude = ['created_by', 'updated_by','created_at', 'updated_at','amount']

class VendorAdmin(admin.ModelAdmin):
    form = VendorForm

admin.site.register(Vendor, VendorAdmin)
