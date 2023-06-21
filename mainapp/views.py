from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from urllib.parse import quote
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from urllib.parse import urlencode
from django.utils import timezone
import urllib.parse
import urllib.request
import json, sys, http.client, subprocess
from .calculate import calculate_attraction_order
from .models import Atrakcja, AtrakcjeHistoria
from .forms import planowanie, UserRegForm


def logout_view(request):
    logout(request)
    return redirect('frontpage')

def frontpage(request):
    return render(request, 'mainapp/frontpage.html')

def kontakt(request):
    return render(request, 'mainapp/kontakt.html')

def profile(request):
    return render(request, 'mainapp/profile.html')
      
def logowanie(request):
    if request.user.is_authenticated:
        return redirect('frontpage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'mainapp/frontpage.html')
            return render(request, 'mainapp/logowanie.html')
        else:
            url_register = reverse('register')  # generowanie adresu URL rejestracji
            return render(request, 'mainapp/logowanie.html', {'url_register': url_register})

def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('captcha'):
                user = form.save(commit=False)
                email = form.cleaned_data.get('e_mail')
                user.email = email
                user.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(profile)
            else:
                form.add_error('captcha', 'Invalid Captcha. Please try again.')
    else:
        form = UserRegForm()
    return render(request, 'mainapp/register.html', {'form': form})


def subskrypcja(request):
    return render(request, 'mainapp/subskrypcja.html')

def planowanie_view(request):
    if request.method == 'POST':
        form = planowanie(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            redirect_url = f'/searchpage/?param1={form_data["miasto"]}&param2={form_data["ulica"]}&param3={form_data["data_od"]}&param4={form_data["data_do"]}&kategorie={",".join(form_data["KATEGORIE_CHOICES"])}'
            return redirect(redirect_url)
    else:
        form = planowanie()
        return render(request, 'mainapp/plan.html', {'form': form})

def searchresults(request):
    if 'sortowanie' in request.POST:
        form = planowanie(request.POST)
        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')
        param3 = request.GET.get('param1')
        param4 = request.GET.get('param2')
        redirect_url = f'/searchpage/?param1={form_data["miasto"]}&param2={form_data["ulica"]}&param3={form_data["data_od"]}&param4={form_data["data_do"]}&kategorie={",".join(form_data["KATEGORIE_CHOICES"])}'
        return redirect(redirect_url)
    elif 'wyszukiwanie' in request.POST:
        # Obsługa przycisku "wyszukaj"
        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')
        selected_attractions = request.POST.getlist('atrakcje')
        params = {'param1': param1, 'param2': param2, 'attractions': ",".join(selected_attractions)}
        encoded_params = urlencode(params)
        redirect_url = f'/resultspage/?{encoded_params}'
        return redirect(redirect_url)
    else:
        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')
        param3 = request.GET.get('param3')
        param4 = request.GET.get('param4')
        kategorie_param = request.GET.get('kategorie')
        kategorie = kategorie_param.split(',')
        form = planowanie(initial={'miasto': param1, 'ulica': param2, 'data_od': param3, 'data_do': param4})
        data_od = datetime.strptime(param3, '%Y-%m-%d').date()
        data_do = datetime.strptime(param4, '%Y-%m-%d').date()
        atrakcja_lista = Atrakcja.objects.filter((Q(data_od__gt=data_od) | Q(data_do__lt=data_do)) & Q(miasto=param1) & (Q(kategoria_1__in=kategorie) | Q(kategoria_2__in=kategorie) | Q(kategoria_3__in=kategorie)))
        context = {'atrakcja_lista': atrakcja_lista, 'form': form, 'attractions': atrakcja_lista}
        return render(request, 'mainapp/searchpage.html', context)


def resultsView(request):
    param1 = request.GET.get('param1')
    param2 = request.GET.get('param2')
    address = f"{param2}, {param1}"
    encoded_address = quote(address)
    attractions = request.GET.get('attractions', '').split(',')
    ordered_attractions = calculate_attraction_order(param1, param2, attractions)
    attraction_coords = []
    for attraction_name in ordered_attractions:
        attraction = Atrakcja.objects.get(nazwa_atrakcji=attraction_name)
        attraction_coords.append((attraction.latitude, attraction.longitude))
    destination_lat, destination_lng = attraction_coords[-1]
    map_url = "https://www.google.com/maps/dir/?api=1"
    map_url += f"&origin={param2},{param1}"
    map_url += f"&destination={destination_lat},{destination_lng}"
    waypoints = "|".join([f"{coords[0]},{coords[1]}" for coords in attraction_coords[:-1]])
    map_url += f"&waypoints={waypoints}"
    if request.user.is_authenticated:
        uzytkownik = request.user
        atrakcje_str = ','.join(ordered_attractions)  # Konwersja listy na tekst
        historia = AtrakcjeHistoria(uzytkownik=uzytkownik, nazwa_atrakcji=atrakcje_str, data_zapisu=timezone.now())
        historia.save()

    context = {'attractions': ordered_attractions, 'map_url': map_url}
    return render(request, 'mainapp/resultspage.html', context)