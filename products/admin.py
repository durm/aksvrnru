#-*- coding: utf-8 -*-

from django.contrib import admin
from products.models import Product
from django.contrib.admin.widgets import FilteredSelectMultiple
from previews.models import Preview
from django import forms

class ProductForm(forms.ModelForm):

    previews = forms.ModelMultipleChoiceField(queryset=Preview.objects.all(), widget=FilteredSelectMultiple(u"Картинки", is_stacked=False))

    class Meta:
        model = Product
        exclude = ['created_by', 'updated_by','created_at', 'updated_at','amount']

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_vendor',
        'short_desc',
        'available_for_trade',
        'trade_price',
        'available_for_retail',
        'retail_price'
    )

    list_filter = (
        'is_published', 
        'is_valid', 
        'is_special_price', 
        'is_new', 
        'trade_by_order',
        'is_recommend_price', 
        'available_for_retail',
        'available_for_trade',
    )
    
    search_fields = (
        'name', 'short_desc', 'vendor__name'
    )
    
    def get_vendor(self, obj):
        return obj.vendor.name
    get_vendor.short_description = u'Производитель'
    get_vendor.admin_order_field = 'vendor__name'
    
    form = ProductForm

admin.site.register(Product, ProductAdmin)
