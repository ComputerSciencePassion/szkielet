from django.db import models
from django.forms import TextInput
from django.forms import DateInput
from django.core.exceptions import ValidationError
from django.conf import settings
from urllib.parse import quote
import http.client
import json
from django.contrib.auth.models import User

def positive_integer_validator(value):
    if value < 0:
        raise ValidationError("Value cannot be negative.")

class Atrakcja(models.Model):
    nazwa_atrakcji = models.CharField(max_length=250)
    opis_atrakcji = models.CharField(max_length=250)
    adres = models.CharField(max_length=100)
    miasto = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6, blank=True)
    nazwa_placowki = models.CharField(max_length=100)
    data_od = models.DateField(blank=True)
    data_do = models.DateField(blank=True)
    godzina_otwarcia = models.TimeField(verbose_name='godzina otwarcia', help_text='Wpisz czas w godzinach')
    godzina_zamknięcia = models.TimeField(verbose_name='godzina zamknięcia', help_text='Wpisz czas w godzinach')
    sredni_czas_zwiedzania = models.DecimalField(help_text='Wpisz czas w godzianch',validators=[positive_integer_validator], decimal_places=2, max_digits=3)
    cena_normalna= models.DecimalField(max_digits=6, decimal_places=2,validators=[positive_integer_validator],default=0)
    cena_ulgowa= models.DecimalField(max_digits=6, decimal_places=2,blank=True,help_text="cena dla studentów oraz uczniów do 26 roku zycia",validators=[positive_integer_validator],null=True,default=0)
    cena_dla_emerytów= models.DecimalField(max_digits=6, decimal_places=2,blank=True,validators=[positive_integer_validator],null=True,default=0)
    latitude = models.CharField(null=True, blank=True, max_length=100)
    longitude = models.CharField(null=True, blank=True, max_length=100)
    KATEGORIE_CHOICES = [
        ('muzeum', 'Muzeum'),
        ('galeria_sztuki', 'Galeria sztuki'),
        ('park_narodowy', 'Park narodowy'),
        ('wzgorze_i_gora', 'Wzgórze i góra'),
        ('park_rozrywki', 'Park rozrywki'),
        ('zabytek', 'Zabytek'),
        ('katedra_i_kosciol', 'Katedra i kościół'),
        ('zamek_i_palac', 'Zamek i pałac'),
        ('skansen', 'Skansen'),
        ('akwarium_i_oceanarium', 'Akwarium i oceanarium'),
        ('ogrod_botaniczny', 'Ogród botaniczny'),
        ('centrum_nauki_i_techniki', 'Centrum nauki i techniki'),
        ('muzeum_naukowe', 'Muzeum naukowe'),
        ('planetarium', 'Planetarium'),
        ('obserwatorium', 'Obserwatorium'),
        ('teatr', 'Teatr'),
        ('opera', 'Opera'),
        ('kino', 'Kino'),
        ('klub_nocny', 'Klub nocny'),
        ('targowisko_i_bazar', 'Targowisko i bazar'),
        ('festiwal_muzyczny_i_artystyczny', 'Festiwal muzyczny i artystyczny'),
        ('wystawa_sztuki_i_fotografii', 'Wystawa sztuki i fotografii'),
        ('park_tematyczny', 'Park tematyczny'),
        ('miejsce_historyczne_i_archeologiczne', 'Miejsce historyczne i archeologiczne'),
        ('sklep_i_centrum_handlowe', 'Sklep i centrum handlowe'),
        ('spa_i_centrum_wellness', 'Spa i centrum wellness'),
        ('pole_golfowe', 'Pole golfowe'),
        ('jaskinia_i_kopalnia', 'Jaskinia i kopalnia'),
        ('wodospad', 'Wodospad'),
        ('jezioro', 'Jezioro'),
        ('plaza_i_kapielisko', 'Plaża i kąpielisko'),
        ('port_i_przystan', 'Port i przystań'),
        ('stadion_i_arena_sportowa', 'Stadion i arena sportowa'),
        ('pole_sportowe_i_kort_tenisowy', 'Pole sportowe i kort tenisowy'),
        ('pieszy_i_rowerowy_szlak_turystyczny', 'Pieszy i rowerowy szlak turystyczny'),
        ('kajakarstwo_i_wioslowanie', 'Kajakarstwo i wiosłowanie'),
        ('nurkowanie_i_snorkeling', 'Nurkowanie i snorkeling'),
        ('Wycieczka_łodzią_i_statkiem','Wycieczka łodzią i statkiem'),
        ('Wspinaczka_górska_i_wspinaczka_skałkowa','Wspinaczka górska i wspinaczka skałkowa'),
        ('Jazda_konna_i_wycieczka_konna','Jazda konna i wycieczka konna'),
        ('Safari_i_zwiedzanie_dzikiej_przyrody','Safari i zwiedzanie dzikiej przyrody')
    ]
    kategoria_1 = models.CharField(max_length=40, choices=KATEGORIE_CHOICES, default='-', help_text="Enter the text for my field here.", blank=True)
    kategoria_2 = models.CharField(max_length=40, choices=KATEGORIE_CHOICES, default='-', help_text="Enter the text for my field here.", blank=True)
    kategoria_3 = models.CharField(max_length=40, choices=KATEGORIE_CHOICES, default='-', help_text="Enter the text for my field here.", blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            address = f"{self.adres}, {self.miasto}, {self.zip_code}"
            encoded_address = quote(address)
            conn = http.client.HTTPSConnection("maps.googleapis.com")
            conn.request("GET", f"/maps/api/geocode/json?address={encoded_address}&key=AIzaSyDUj5pTuHqBU3LdNXJIXlM2Gzb2IofPVAM")
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            data = json.loads(data)
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                self.latitude = str(location['lat'])
                self.longitude = str(location['lng'])
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nazwa_atrakcji

class AtrakcjeHistoria(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    nazwa_atrakcji = models.CharField(max_length=255)
    data_zapisu = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Atrakcje dla {self.uzytkownik.username} #{self.id}"