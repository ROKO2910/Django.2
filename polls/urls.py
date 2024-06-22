from django.urls import path
from .views import login_view

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("rickymorty/", views.rickymorty, name="testapirick"),
    path('calculadora/', views.calculadora, name='calculadora'),  
    path('rickylista/', views.rickylista, name='numrick'),
    #path('agregar-cliente/', views.agregar_cliente, name='cliente_form'),
    #path('',views.mostrar_cliente, name='lista_clientes'),
    path('login/', views.login_view, name='login'),
    ]