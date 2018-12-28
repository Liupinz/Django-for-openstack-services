from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/login':
            return None
        user_info = request.session.has_key('islogin')
        if not user_info:
            return redirect('/login')

