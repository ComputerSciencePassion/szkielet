from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('frontpage/', views.frontpage, name='frontpage'),
    path('admin/', admin.site.urls, name='admin'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('logowanie/', views.logowanie, name='logowanie'),
    path('plan/', views.planowanie_view, name='plan'),
    path('subskrypcja/', views.subskrypcja, name='subskrypcja'),
    path('searchpage/', views.searchresults, name='searchpage'),
    path('resultspage/', views.resultsView, name='resultspage'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile')
]
