from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    white_list = ['/login', '/login_check', '/contact', '/contact_handle']

    def process_request(self, request):
        if request.path in self.white_list:
            return None
        if not request.session.has_key('islogin'):
            return redirect('/login')


