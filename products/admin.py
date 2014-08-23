#-*- coding: utf-8 -*-

from django.contrib import admin
from products.models import *
from products.tasks import proc
import threading

def not_set(obj, attrib):
    return not hasattr(obj, attrib) or (hasattr(obj, attrib) and getattr(obj, attrib) is None)


def proc_list(modeladmin, request, queryset):
    for obj in queryset :
        proc.delay(request, obj)

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

        if not_set(obj, "created_by") :
            obj.created_by = request.user

        obj.updated_by = request.user

        obj.save()

    actions = [proc_list]

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'vendor', 'short_desc', 'trade_price', 'retail_price')
    list_filter = ('by_order', 'is_new', 'is_special_price', 'is_recommend_price')
    search_fields = ['name']

    fields = ['name', 'vendor', 'short_desc', 'desc', 'image', 'rubrics', 'trade_price', 'retail_price', 'is_recommend_price',
        'external_link', 'by_order', 'is_new', 'is_special_price',
        'created_at', 'created_by' , 'updated_at' , 'updated_by']

    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):

        if not_set(obj, "created_by") :
            obj.created_by = request.user

        obj.updated_by = request.user
        obj.save()

class RubricAdmin(admin.ModelAdmin):

    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):

        if not_set(obj, "created_by") :
            obj.created_by = request.user

        obj.updated_by = request.user
        obj.save()

class VendorAdmin(admin.ModelAdmin):

    readonly_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):

        if not_set(obj, "created_by") :
            obj.created_by = request.user

        obj.updated_by = request.user
        obj.save()

admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Vendor, VendorAdmin)
