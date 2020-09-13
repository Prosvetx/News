from django.contrib import admin
from .models import Section, New


class NewAdmin(admin.ModelAdmin):
    list_display = ['title','like', 'date']


admin.site.register(Section)
admin.site.register(New, NewAdmin)
