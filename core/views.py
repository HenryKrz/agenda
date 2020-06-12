from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here


# def index(request):
#  return redirect('/agenda')

def login_user(request):
    return render(request, 'login.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        local = request.POST.get('local')
        Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario, local=local)
    return redirect('/')


@login_required(login_url='/login/')
def local(request, titulo_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(titulo=titulo_evento, usuario=usuario)
        local = evento.local
        if local is not None:
            return HttpResponse(local)
        else:
            return HttpResponse('Sem local definido')
    except ObjectDoesNotExist:
        return HttpResponse('Evento inexistente')
