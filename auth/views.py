from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def login(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        username = json_data['username']
        password = json_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return HttpResponse("authentication OK")
    else:
        return HttpResponse("ERROR auth/login")

@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect('/')

@csrf_exempt
def register(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        username = json_data['username']
        password = json_data['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            return HttpResponse("user already exists")
        else:
            if len(username) > 0 and len(password) > 0:
                User.objects.create_user(username=username, password=password)
                #return redirect('/')
                return HttpResponse("User " + username + " created")
            else:
                return HttpResponse("ADD username and password")
    else:
        HttpResponse("ERROR auth/register")

def error_view(request):
    resp_data = {}
    resp_data['result'] = 'failed'
    resp_data['errors'] = 'log in please'
    return HttpResponse(json.dumps(resp_data), content_type='application/json')
