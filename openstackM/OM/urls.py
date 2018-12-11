from django.conf.urls import url
from OM import views

urlpatterns = [
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'^openstacks$', views.openstackStatus),
]