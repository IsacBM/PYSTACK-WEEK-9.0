from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha e confimar senha não coincidem')
            return redirect('/usuario/cadastro')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuario já existe!')
            return redirect('/usuario/cadastro')
        
        try:
            User.objects.create_user(
                username=username,
                password=senha
            )
            return redirect('/usuario/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do servidor')
            return redirect('/usuario/cadastro')
        
    
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username = username, password = senha)
        
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!' )
            return redirect('/flashcard/novo_flashcard/')
        else:
            messages.add_message(request, constants.ERROR, 'Username ou senha incorretos. Tente novamente!')
            return redirect('/usuario/logar/')
    
    
def logout(request):
    auth.logout(request)
    return redirect('/usuario/logar')
    