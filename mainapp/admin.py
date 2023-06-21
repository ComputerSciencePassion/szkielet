from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Atrakcja, AtrakcjeHistoria
from django.contrib.auth.models import Group

class AtrakcjeHistoriaAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'nazwa_atrakcji', 'data_zapisu')
    list_filter = ('uzytkownik__username',)  # Dodajemy filtr dla nazwy użytkownika

admin.site.unregister(Group)
admin.site.register(Atrakcja)
admin.site.register(AtrakcjeHistoria, AtrakcjeHistoriaAdmin)