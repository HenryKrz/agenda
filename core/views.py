from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime, timedelta

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
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual) # maior que
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def json_lista_eventos(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        local = request.POST.get('local')
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.local = local
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            #Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao, local=local)
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario, local=local)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
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
