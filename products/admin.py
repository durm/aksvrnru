#-*- coding: utf-8 -*-

from django.contrib import admin
from products.models import *
from products.views import proc
import threading

def proc_list(modeladmin, request, queryset):
    for obj in queryset :
        threading.Thread(target=proc, args=(request, obj)).start()
        #proc(request, obj)

proc_list.short_description = "Распарсить выделенные прайсы"

class PriceAdmin(admin.ModelAdmin):

    list_display = ('name','created_at','is_processed','result')

    def get_form(self, request, obj=None, **kwargs):

        if obj is None :
            self.fields = ['name', 'desc', 'file']
            self.readonly_fields = []
        else:

            self.fields = []
            self.readonly_fields = []

            if obj.is_processed :
                processed_fields = ['name', 'desc', 'is_processed', 'processed_by', 'processed_at', 'result', 'result_desc']
                self.fields += processed_fields
                self.readonly_fields += processed_fields
            else:
                self.fields += ['name', 'desc', 'file', 'created_by', 'created_at', 'updated_by', 'updated_at']
                self.readonly_fields += ['created_by', 'created_at', 'updated_by', 'updated_at']

        return super(PriceAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):

        if not hasattr(obj, 'created_by') or (hasattr(obj, 'created_by') and obj.created_by is None) :

            obj.created_by = request.user
            obj.processed_by = request.user
            obj.updated_by = request.user

        obj.save()

    actions = [proc_list]

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_filter = ('by_order', 'is_new', 'is_special_price')
    search_fields = ['name']

    fields = ['name', 'desc', 'image', 'rubrics', 'trade_price', 'retail_price', 'recommend_price',
        'amount', 'external_link', 'by_order', 'is_new', 'is_special_price',
        'created_at', 'created_by' , 'updated_at' , 'updated_by']

    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):

        if not hasattr(obj, 'created_by') or (hasattr(obj, 'created_by') and obj.created_by is None) :

            obj.created_by = request.user
            obj.updated_by = request.user

        obj.save()

    actions = [proc_list]

admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric)
