from django.shortcuts import render, redirect
from django.http import HttpResponse
from OM.models import User
import requests
import json
import os

# Create your views here.

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('islogin'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return wrapper

def login(request):
    # if request.session.has_key('islogin'):
    #     return redirect('/openstacks')
    # else:
    if 'username' in request.COOKIES and 'password' in request.COOKIES:
        username = request.COOKIES['username']
        password = request.COOKIES['password']
    else:
        username = ''
        password = ''
    return render(request, 'OM/login.html', {'username': username, 'password': password})

def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    user = User.objects.get(id=1)
    if username == user.uname and password == user.upassword:
        response = redirect('/openstacks')
        if remember == 'on':
            response.set_cookie('username', username, max_age=7*24*3600)
            response.set_cookie('password', password, max_age=7*24*3600)
        request.session['islogin'] = True
        return response
    else:
        return redirect('/login')

@login_required
def openstackStatus(request):
    data = {
	    "auth":{
			"passwordCredentials":
		    {
			"username": "admin",
			"password": "123456"
		    },
		"tenantName": "admin"
	        }
        }
    r_token = requests.post('http://172.16.53.249:5000/v2.0/tokens', data=json.dumps(data))
    token = r_token.json()['access']['token']['id']
    r_service = requests.get('http://controller:8774/v2.1/os-services', headers={'X-Auth-Token': token})
    nova_services = r_service.json()['services']
    # for s in nova_services:
    #     contentNova = {
    #         "Id": s['id'],
    #         "Binary": s['binary'],
    #         "Host": s['host'],
    #         "Zone": s['zone'],
    #         "Status": s['status'],
    #         "State": s['state'],
    #         "Updated_at": s['updated_at'],
    #         "Disabled_reason": s['disabled_reason']
    #     }
    return render(request, 'OM/status.html', {'contentNova': nova_services})
