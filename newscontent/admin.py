from django.contrib import admin
from .models import Section, New, Rate


class NewAdmin(admin.ModelAdmin):
    list_display = ['title', 'like', 'date', 'section']


class RateAdmin(admin.ModelAdmin):
    list_display = ['valute', 'value_rur']


admin.site.register(Section)
admin.site.register(New, NewAdmin)
admin.site.register(Rate, RateAdmin)
