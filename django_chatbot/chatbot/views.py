from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from groq import Groq

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone

client = Groq(api_key='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', )


def ask_groq(message):
    chat_completion = client.chat.completions.create(
    messages=[
        # {
        #     "role": "system",
        #     "content":"You are a helpful assistant. You reply within 5 lines answers"
        # },
        {
            "role": "user",
            "content": message,
        }
    ],
    model="llama3-8b-8192",
    )
    # answer=chat_completion.choices[0].message.content.strip()
    answer=chat_completion.choices[0].message.content.strip()
    return answer
 



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method =='POST':
        message = request.POST.get('message')
        response = ask_groq(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
     
    return render(request, 'chatbot.html')




def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message}) 
    return render(request, 'register.html')