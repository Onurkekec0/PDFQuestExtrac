from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AnaSayfa),
    path('ExamplesPDF',views.ExamplesPDF,name='ExamplesPDF'),
    path('sorular', views.sorular, name='sorular'),
    path('ilerle/',views.ilerlemeli_form,name='ilerle'),
    path('loading', views.loading_view, name='loading'),
    path('cevaplar', views.cevaplar, name='cevaplar'),

]
