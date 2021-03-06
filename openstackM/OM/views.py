from django.shortcuts import render, redirect
from OM import models
from django.conf import settings
from django.http import HttpResponse
from OM.models import User
import subprocess
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
    userResult = User.objects.filter(uname=username, upassword=password)
    if (int(len(userResult)>0)):
        response = redirect('/list_status')
        if remember == 'on':
            response.set_cookie('username', username, max_age=7*24*3600)
            response.set_cookie('password', password, max_age=7*24*3600)
        request.session['islogin'] = True
        return response
    else:
        return redirect('/login')


def list_status(request):
    return render(request, 'OM/list_status.html')


def cloudip(request):
    return render(request, 'OM/cloudip.html')


def clouddashboard(request):
    cloudip = request.POST.get('cloudip')
    cloudip = "http://" + str(cloudip) + "/dashboard"
    print(cloudip)
    return render(request, 'OM/clouddashboard.html', {'cloudip': cloudip})


def contact(request):
    return render(request, 'OM/contact.html')


def contact_handle(request):
    comment = request.POST.get('comment')
    fname = request.POST.get('fname')
    save_path = "%s/%s.txt" % (settings.MESSAGE_ROOT, fname)
    with open(save_path, 'w') as f:
        f.write(comment)
    return redirect('/login')


def register(request):
    return render(request, 'OM/register.html')


def register_handle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User(uname=username, upassword=password)
    user.save()
    return redirect('/login')


def openstackStatus(request):
    httpd_status = subprocess.getoutput("systemctl status httpd | grep Active | awk '{print $2}'")
    httpd_s = "The http status is %s" % httpd_status
    use = subprocess.getoutput("df -h | grep -w / |awk '{print int($5)}'")
    use = "The use of / is {0}%".format(use)
    free_memory = subprocess.getoutput("free -h | grep Mem | awk '{print $4}'")
    free_m = "The free memory is %s" % free_memory
    mariadb_status = subprocess.getoutput("systemctl status mariadb.service | grep Active | awk '{print $2}'")
    mariadb_s = "The mariadb status is %s" % mariadb_status
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
    r1_service = requests.get('http://controller:8774/v2.1/os-services', headers={'X-Auth-Token': token})
    nova_services = r1_service.json()['services']
    r2_service = requests.get('http://controller:9696/v2.0/agents.json', headers={'X-Auth-Token': token})
    neutron_status = r2_service.json()['agents']

    content = {
        'httpd_s': httpd_s,
        'use': use,
        'free_m': free_m,
        'mariadb_s': mariadb_s,
        'contentNova': nova_services,
        'neutron': neutron_status
    }
    # content = {
    #     'contentNova': nova_services
    # }
    return render(request, 'OM/status.html', content)
