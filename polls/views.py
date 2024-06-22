from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login

from .models import Choice, Question

import requests

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return True
            else:
                raise forms.ValidationError("La cuenta del usuario está inactiva.")
        else:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.login(request):
                return redirect('/')  # Redirigir a la página principal
            else:
                pass  # Mostrar un mensaje de error
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'polls/login.html')

#def agregar_cliente(request):
    
    
#def mostrar_cliente(request):
#    if request.method == 'GET':
#        personaje = request.GET.get('personaje', '')  

def rickymorty(request):
    api_url = 'https://rickandmortyapi.com/api/character/331'
    response = requests.get(api_url)
    data = []
    if response.status_code == 200:
        data = response.json()
        print(data)
    return render(request, 'polls/testapirick.html', {'data': data})


def calculadora(request):
    if request.method == 'POST':
        num1 = float(request.POST.get('num1', ''))
        num2 = float(request.POST.get('num2', ''))
        operacion = request.POST.get('operacion', '')

        if operacion == 'suma':
            resultado = num1 + num2
        elif operacion == 'resta':
            resultado = num1 - num2
        elif operacion == 'multiplicacion':
            resultado = num1 * num2
        elif operacion == 'division':
            if num2 != 0:
                resultado = num1 / num2
            else:
                resultado = 'Error: División por cero'
        else:
            resultado = 'Operación no válida'

        return render(request, 'polls/calculadora.html', {'resultado': resultado})

    return render(request, 'polls/calculadora.html')


def rickylista(request):
    if request.method == 'GET':
        personaje = request.GET.get('personaje', '')  
        if personaje:
            api_url = f'https://rickandmortyapi.com/api/character/{personaje}'
            response = requests.get(api_url)
            resultado = {}
            if response.status_code == 200:
                resultado = response.json()
            else:
                resultado = {'ERROR': 'Su personaje no existe :('}
            return render(request, 'polls/numrick.html', {'resultado': resultado})
        else:
            return render(request, 'polls/numrick.html', {'ERROR': 'Ingrese un número de personaje'})  
    return render(request, 'polls/numrick.html')

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Escoge una opción por favor",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))